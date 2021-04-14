from datetime import timedelta
from amz.config import AmazonConfig
from amz.advertising_api import AdvertisingApi
from amz.metrics import ASINS_KEYWORDS_METRICS, ASINS_TARGETS_METRICS, KEYWORDS_METRICS, \
    PRODUCT_ADS_METRICS, SPONSORED_BRANDS_METRICS, SPONSORED_DISPLAY_METRICS
from amz.regions import region_codes
import time
import json
from sqlalchemy.orm import sessionmaker
from db.serializers import create_sp_asins_keywords, create_sp_asins_targets, create_sp_keywords, \
    create_sp_product_ads, create_sponsored_brand, create_sponsored_display

report_types = {
    'SponsoredProductsAsinsKeywords': {
        'campaignType': 'sponsoredProducts',
        'interface_type': 'sp',
        'record_type': 'asins',
        'serializer': create_sp_asins_keywords,
        'metrics': ','.join(ASINS_KEYWORDS_METRICS),
    },
    'SponsoredProductsAsinsTargets': {
        'campaignType': 'sponsoredProducts',
        'interface_type': 'sp',
        'record_type': 'asins',
        'serializer': create_sp_asins_targets,
        'metrics': ','.join(ASINS_TARGETS_METRICS),
    },
    'SponsoredProductsKeywords': {
        'interface_type': 'sp',
        'record_type': 'keywords',
        'serializer': create_sp_keywords,
        'metrics': ','.join(KEYWORDS_METRICS),
    },
    'SponsoredProductsProductAds': {
        'interface_type': 'sp',
        'record_type': 'productAds',
        'serializer': create_sp_product_ads,
        'metrics': ','.join(PRODUCT_ADS_METRICS),
    },
    'SponsoredBrands': {
        'interface_type': 'hsa',
        'record_type': 'keywords',
        'serializer': create_sponsored_brand,
        'metrics': ','.join(SPONSORED_BRANDS_METRICS),
    },
    'SponsoredDisplay': {
        'interface_type': 'sd',
        'record_type': 'productAds',
        'tactic': 'T00020',
        'serializer': create_sponsored_display,
        'metrics': ','.join(SPONSORED_DISPLAY_METRICS),
    }
}


def get_dates_between(start_date, end_date):
    diff = end_date - start_date
    return [start_date + timedelta(i) for i in range(diff.days + 1)]


def request_report(api_object, report_type, report_date):
    if api_object.last_refreshed_access_token <= time.time()-30*60:  # Refresh token if it's more than 30 minutes old
        api_object.do_refresh_token()

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

    response = api_object.request_report(record_type=record_type, data=data, campaign_type=interface_type)
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
    for entry in data_records:
        try:
            record = report_types[report_type]['serializer'](entry)
            record.AmzAccount_ID_Internal = amazon_config.AmzAccount_ID_Internal
            record.AmzAccount_Group = amazon_config.AmzAccount_Group
            record.ReportDate = report_date
            session.merge(record)
            session.commit()
        except Exception:
            logger.exception('Uncaught exception while processing report: %s', entry)
    logger.info('Saved %s records in report to database', len(data_records))


def process_report_type(api_object: AdvertisingApi, db_engine, logger, report_type, amazon_config):
    report_dates = get_dates_between(amazon_config.ReportStartDate, amazon_config.ReportEndDate)
    for report_date in report_dates:
        logger.info(f'Requesting report type {report_type} for date {report_date.strftime("%Y%m%d")}')
        print(f'Requesting report type {report_type} for date {report_date.strftime("%Y%m%d")}')
        report_id = request_report(api_object, report_type, report_date)
        if report_id:
            response = api_object.get_report(report_id)
            data_records = response['response']
            logger.debug(f'Downloaded report with {len(data_records)} records')
            print(f'Downloaded report with {len(data_records)} records')
            logger.debug(f'Writing report records to database')
            save_records_to_db(data_records=data_records, db_engine=db_engine, report_type=report_type,
                               report_date=report_date, logger=logger, amazon_config=amazon_config)
        else:
            logger.error('Failed to download report')


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

                for report_type in amazon_config.ReportType:
                    process_report_type(
                        api_object=api_object,
                        db_engine=db_engine,
                        logger=logger,
                        report_type=report_type,
                        amazon_config=amazon_config,
                    )
            except Exception:
                logger.exception('Uncaught exception while processing reports')
