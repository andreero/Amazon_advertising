from sqlalchemy import create_engine

from amz.config import AmazonConfig
from config import config_spreadsheet_id
from db.config import DBConfig
from db.logger import create_db_logger
from db.models import Base
from google_sheets.layouts import amazon_layout, db_layout
from google_sheets.reader import read_config_dicts_from_sheet

from amz.report_requester import process_reports


def main():
    amazon_config_dicts = read_config_dicts_from_sheet(spreadsheet_id=config_spreadsheet_id, layout=amazon_layout)
    db_config_dict = read_config_dicts_from_sheet(spreadsheet_id=config_spreadsheet_id, layout=db_layout)[0]

    db_config = DBConfig.from_dict(db_config_dict)
    engine = create_engine(db_config.connection_string)
    Base.metadata.create_all(engine)
    db_logger = create_db_logger(engine, extra={
            'AmzAccount_Group': None,
            'AmzAccount_ID_Internal': None,
        })
    db_logger.info('Script started')

    for amazon_config_dict in amazon_config_dicts:
        try:
            amazon_config = AmazonConfig.from_dict(amazon_config_dict)
            db_logger.extra = {
                'AmzAccount_Group': amazon_config.AmzAccount_Group,
                'AmzAccount_ID_Internal': amazon_config.AmzAccount_ID_Internal,
            }
        except Exception:
            db_logger.exception('Failed to initialize from amazon config %s',
                                amazon_config_dict.get('AmzAccount_ID_Internal'))
        else:
            db_logger.info('Processing reports using amazon config %s', amazon_config.AmzAccount_ID_Internal)
            process_reports(db_engine=engine, logger=db_logger, amazon_config=amazon_config)


if __name__ == '__main__':
    main()
