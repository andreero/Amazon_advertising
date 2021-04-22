import json
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import date, timedelta
from functools import partial
from threading import Lock

from sqlalchemy.orm import sessionmaker

from amz.advertising_api import AdvertisingApi
from amz.config import AmazonConfig, MAX_POOL_WORKERS, MAX_REPORT_CREATION_RETRIES, REQUEST_TIMEOUTS_SECONDS
from amz.regions import region_codes
from amz.report_types import report_types


@dataclass
class Report:
    report_type: str
    report_date: date
    data: dict
    record_type: str
    interface_type: str


def create_api_connection(amazon_config: AmazonConfig, region):
    api_object = AdvertisingApi(
                client_id=amazon_config.AmzDeveloper_ClientID,
                client_secret=amazon_config.AmzDeveloper_ClientSecret,
                refresh_token=amazon_config.AmzAccount_API_Advert_RefreshToken,
                region=region)
    api_object.do_refresh_token()
    print(f'Connected to Amazon Advertising API in region "{region}"')
    return api_object


def get_dates_between(start_date, end_date):
    diff = end_date - start_date
    return [start_date + timedelta(i) for i in range(diff.days + 1)]


def get_valid_profile_ids(api_object, country_codes):
    valid_profiles = list()
    profiles_response = api_object.get_profiles()
    json_profiles = json.loads(profiles_response['response'])
    for profile in json_profiles:
        if profile['countryCode'].upper() in country_codes and profile['accountInfo']['type'] in ['seller', 'vendor']:
            valid_profiles.append(profile['profileId'])
    return valid_profiles


def request_report(api_object, report: Report, logger):
    if api_object.last_refreshed_access_token <= time.time()-30*60:  # Refresh token if it's more than 30 minutes old
        api_object.do_refresh_token()

    response = api_object.request_report(
        record_type=report.record_type,
        data=report.data,
        campaign_type=report.interface_type)
    if not response['success']:
        logger.warning(f'Bad report creation status for report {report.report_type} '
                       f'for date {report.report_date}, received response: {response}')
        return
    report_id = json.loads(response['response'])['reportId']
    for timeout in REQUEST_TIMEOUTS_SECONDS:
        if 'status' not in response['response']:
            logger.warning(f'No report creation status for report {report.report_type} for date {report.report_date}, '
                           f'received response: {response}')
            return
        status = json.loads(response['response'])['status']

        if status not in ['IN_PROGRESS', 'SUCCESS']:
            logger.warning(f'Bad report creation status for report {report.report_type} '
                           f'for date {report.report_date}, received response: {response}')
            return

        if status == 'SUCCESS':
            return report_id
        time.sleep(timeout)
        response = api_object.request_report(report_id=report_id)
    logger.warning(f'Report {report.report_type} for date {report.report_date} timed out, '
                   f'last received response was {response}')


def save_records_to_db(data_records, report_type, report_date, db_engine, logger, amazon_config):
    session_maker = sessionmaker()
    session = session_maker(bind=db_engine)
    try:
        for entry in data_records:
            record = report_types[report_type]['serializer'](entry)
            record.AmzAccount_ID_Internal = amazon_config.AmzAccount_ID_Internal
            record.AmzAccount_Group = amazon_config.AmzAccount_Group
            record.ReportDate = report_date
            session.merge(record)
        session.commit()
    except Exception:
        logger.exception(f'Uncaught exception while saving records for {report_type} for date {report_date}')
    logger.info(f'Saved {len(data_records)} records in report {report_type} for date {report_date} to database')
    print(f'Saved {len(data_records)} records in report {report_type} for date {report_date} to database')


def delete_previous_records_from_db(report_type, report_date, db_engine, logger, amazon_config):
    try:
        session_maker = sessionmaker()
        session = session_maker(bind=db_engine)
        model = report_types[report_type]['model']
        logger.debug(f'Deleting old records for {report_type} for date {report_date}')
        rows_deleted = session.query(model).filter(
            model.AmzAccount_ID_Internal == amazon_config.AmzAccount_ID_Internal,
            model.ReportDate == report_date.strftime('%Y%m%d')
        ).delete(synchronize_session=False)
        session.commit()
        logger.debug(f'Deleted {rows_deleted} old records for {report_type} for date {report_date}')
        print(f'Deleted {rows_deleted} old records for {report_type} for date {report_date}')
    except Exception:
        logger.exception(f'Uncaught exception while deleting old records for {report_type} for date {report_date}')


def process_report(report: Report, api_object, db_engine, db_lock, logger, amazon_config):
    logger.info(f'Requesting report type {report.report_type} for date {report.report_date}')
    print(f'Requesting report type {report.report_type} for date {report.report_date}')
    for retry_number in range(MAX_REPORT_CREATION_RETRIES):
        report_id = request_report(api_object=api_object, report=report, logger=logger)
        if report_id:
            response = api_object.get_report(report_id)
            data_records = response['response']
            logger.debug(f'Downloaded report {report.report_type} for '
                         f'date {report.report_date} with {len(data_records)} records')
            print(f'Downloaded report {report.report_type} for '
                  f'date {report.report_date} with {len(data_records)} records')
            with db_lock:
                delete_previous_records_from_db(report_type=report.report_type, report_date=report.report_date,
                                                db_engine=db_engine, logger=logger, amazon_config=amazon_config)
                logger.debug(f'Writing report {report.report_type} {report.report_date} to database')
                save_records_to_db(data_records=data_records, db_engine=db_engine, report_type=report.report_type,
                                   report_date=report.report_date, logger=logger, amazon_config=amazon_config)
            return
        else:
            logger.warning(f'Failed to download report {report.report_type} '
                           f'for date {report.report_date}, retry {retry_number+1}/{MAX_REPORT_CREATION_RETRIES}')
    else:
        logger.error(f'Failed to download report {report.report_type} '
                     f'for date {report.report_date} after max retries')


def create_report_queue(amazon_config):
    report_queue = list()
    report_dates = get_dates_between(amazon_config.ReportStartDate, amazon_config.ReportEndDate)
    for report_type in amazon_config.ReportType:
        for report_date in report_dates:
            data = {
                'reportDate': report_date.strftime('%Y%m%d'),
                'metrics': report_types[report_type]['metrics']
            }
            if 'campaignType' in report_types[report_type]:
                data['campaignType'] = report_types[report_type]['campaignType']
            if 'tactic' in report_types[report_type]:
                data['tactic'] = report_types[report_type]['tactic']
            if 'creativeType' in report_types[report_type]:
                data['creativeType'] = report_types[report_type]['creativeType']
            record_type = report_types[report_type]['record_type']
            interface_type = report_types[report_type]['interface_type']
            report = Report(
                report_type=report_type,
                report_date=report_date,
                data=data,
                record_type=record_type,
                interface_type=interface_type
            )
            report_queue.append(report)
    return report_queue


def process_report_queue(report_queue, api_object, db_engine, logger, amazon_config):
    with ThreadPoolExecutor(max_workers=MAX_POOL_WORKERS) as executor:
        db_lock = Lock()
        partial_function = partial(  # used because map takes only 1 argument, but I also need to pass api_object etc.
            process_report,
            api_object=api_object,
            db_engine=db_engine,
            db_lock=db_lock,
            logger=logger,
            amazon_config=amazon_config)
        executor.map(partial_function, report_queue)


def process_reports(db_engine, logger, amazon_config: AmazonConfig):
    regions = set([region_codes[country_code] for country_code in amazon_config.CountryCode])
    for region in regions:
        try:
            api_object = create_api_connection(amazon_config=amazon_config, region=region)
            logger.info(f'Connected to Amazon Advertising API in region "{region}"')
        except Exception:
            logger.exception('Could not connect to Amazon Advertising API')
            continue

        valid_profile_ids = get_valid_profile_ids(api_object=api_object, country_codes=amazon_config.CountryCode)
        for profile_id in valid_profile_ids:
            try:
                api_object.profile_id = profile_id
                logger.info(f'Using profile id {profile_id}.')
                print(f'Using profile id {profile_id}.')

                report_queue = create_report_queue(amazon_config=amazon_config)
                process_report_queue(
                    report_queue=report_queue,
                    api_object=api_object,
                    db_engine=db_engine,
                    logger=logger,
                    amazon_config=amazon_config,
                )

            except Exception:
                logger.exception('Uncaught exception while processing reports')
