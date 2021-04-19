from datetime import date, timedelta
from amz.config import AmazonConfig
from amz.advertising_api import AdvertisingApi

from amz.regions import region_codes
import time
import json
from sqlalchemy.orm import sessionmaker
from amz.report_types import report_types
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from functools import partial


@dataclass
class Report:
    report_type: str
    report_date: date
    data: dict
    record_type: str
    interface_type: str


def get_dates_between(start_date, end_date):
    diff = end_date - start_date
    return [start_date + timedelta(i) for i in range(diff.days + 1)]


def request_report(api_object, report: Report):
    if api_object.last_refreshed_access_token <= time.time()-30*60:  # Refresh token if it's more than 30 minutes old
        api_object.do_refresh_token()

    response = api_object.request_report(
        record_type=report.record_type,
        data=report.data,
        campaign_type=report.interface_type)
    report_id = json.loads(response['response'])['reportId']
    status = 'IN_PROGRESS'
    for timeout in [5, 15, 15, 30, 30]+[60]*10+[120]*10:
        if 'status' in response['response']:
            status = json.loads(response['response'])['status']
        if status == 'SUCCESS':
            return report_id
        time.sleep(timeout)
        response = api_object.request_report(report_id=report_id)


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
        logger.info(f'Deleting old records for {report_type} for date {report_date}.')
        rows_deleted = session.query(model).filter(
            model.AmzAccount_ID_Internal == amazon_config.AmzAccount_ID_Internal,
            model.ReportDate == report_date.strftime('%Y%m%d')
        ).delete(synchronize_session=False)
        session.commit()
        logger.debug(f'Deleted {rows_deleted} old records for {report_type} for date {report_date}.')
        print(f'Deleted {rows_deleted} old records for {report_type} for date {report_date}.')
    except Exception:
        logger.exception(f'Uncaught exception while deleting old records for {report_type} for date {report_date}.')


def get_valid_profile_ids(api_object, country_codes):
    valid_profiles = list()
    profiles_response = api_object.get_profiles()
    json_profiles = json.loads(profiles_response['response'])
    for profile in json_profiles:
        if profile['countryCode'].upper() in country_codes and profile['accountInfo']['type'] in ['seller', 'vendor']:
            valid_profiles.append(profile['profileId'])
    return valid_profiles


def create_api_connection(amazon_config: AmazonConfig, region):
    api_object = AdvertisingApi(
                client_id=amazon_config.AmzDeveloper_ClientID,
                client_secret=amazon_config.AmzDeveloper_ClientSecret,
                refresh_token=amazon_config.AmzAccount_API_Advert_RefreshToken,
                region=region)
    api_object.do_refresh_token()
    print(f'Connected to Amazon Advertising API in region "{region}"')
    return api_object


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


def process_report(report: Report, api_object, db_engine, logger, amazon_config):
    logger.info(f'Requesting report type {report.report_type} for date {report.report_date}')
    print(f'Requesting report type {report.report_type} for date {report.report_date}')
    report_id = request_report(api_object=api_object, report=report)
    if report_id:
        response = api_object.get_report(report_id)
        data_records = response['response']
        logger.debug(f'Downloaded report {report.report_type} for '
                     f'date {report.report_date} with {len(data_records)} records')
        print(f'Downloaded report {report.report_type} for '
              f'date {report.report_date} with {len(data_records)} records')
        delete_previous_records_from_db(report_type=report.report_type, report_date=report.report_date,
                                        db_engine=db_engine, logger=logger, amazon_config=amazon_config)
        logger.debug(f'Writing report {report.report_type} {report.report_date} to database')
        save_records_to_db(data_records=data_records, db_engine=db_engine, report_type=report.report_type,
                           report_date=report.report_date, logger=logger, amazon_config=amazon_config)
    else:
        logger.error('Failed to download report')


def process_report_queue(report_queue, api_object, db_engine, logger, amazon_config):
    with ThreadPoolExecutor(max_workers=3) as executor:
        partial_function = partial(  # used because map takes only 1 argument, but I also need to pass api_object etc.
            process_report,
            api_object=api_object,
            db_engine=db_engine,
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
