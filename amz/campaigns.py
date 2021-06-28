from sqlalchemy.orm import sessionmaker
from db.serializers import create_sp_campaign
from amz.config import REQUEST_TIMEOUTS_SECONDS
import time
import json


def save_campaigns_to_db(campaigns, db_engine, logger, amazon_config):
    session_maker = sessionmaker()
    session = session_maker(bind=db_engine)
    try:
        for entry in campaigns:
            record = create_sp_campaign(entry)
            record.AmzAccount_ID_Internal = amazon_config.AmzAccount_ID_Internal
            record.AmzAccount_Group = amazon_config.AmzAccount_Group
            session.merge(record)
        session.commit()
    except Exception:
        logger.exception(f'Uncaught exception while saving campaigns list')
    logger.info(f'Saved {len(campaigns)} campaigns to database')
    print(f'Saved {len(campaigns)} campaigns to database')


def process_campaigns(api_object, db_engine, logger, amazon_config):
    logger.info(f'Requesting campaigns list')
    print(f'Requesting campaigns list')
    for timeout in REQUEST_TIMEOUTS_SECONDS:
        response = api_object.list_campaigns()
        if response['success']:
            campaigns = json.loads(response['response'])
            logger.debug(f'Downloaded the campaigns list with {len(campaigns)} records')
            print(f'Downloaded the campaigns list with {len(campaigns)} records')
            save_campaigns_to_db(campaigns=campaigns, db_engine=db_engine, logger=logger, amazon_config=amazon_config)
            return
        else:
            time.sleep(timeout)
    else:
        logger.error(f'Failed to download campaigns list after max retries')
