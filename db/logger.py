import logging
from datetime import datetime
from db.models import LogMessage
import traceback
from sqlalchemy.orm import sessionmaker


class LogDBHandler(logging.Handler):
    """ Modified logging handler that writes to provided database session """
    def __init__(self, session):
        super().__init__()
        self.setFormatter(logging.Formatter(
            '%(AmzAccount_Group)s - %(asctime)s - %(pathname)s - %(levelname)s - %(message)s'))
        self.session = session
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        self.format(record)
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        message = LogMessage(
            AmzAccount_Group=record.__dict__['AmzAccount_Group'],
            AmzAccount_ID_Internal=record.__dict__['AmzAccount_ID_Internal'],
            Timestamp=datetime.fromtimestamp(record.__dict__['created']),
            SenderModule=record.__dict__['pathname'],
            MessageType=record.__dict__['levelname'],
            MessageBody=record.__dict__['message'],
            Traceback=trace
        )
        self.session.add(message)
        self.session.commit()


def create_db_logger(db_engine, extra):
    """ Create and return modified logger that writes to provided database """
    Session = sessionmaker()
    session = Session(bind=db_engine)
    logger_db = logging.getLogger('LogDBHandler')
    logger_db.setLevel(logging.DEBUG)
    logger_db.addHandler(LogDBHandler(session))
    logger_db_with_extra = logging.LoggerAdapter(logger=logger_db, extra=extra)
    return logger_db_with_extra
