# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/logservice/handlers/sqlalchemy_handler.py
# Compiled at: 2016-09-07 18:19:46
# Size of source mod 2**32: 1046 bytes
import logging, traceback, transaction
from ..models.log import Log
from ..models import get_engine, get_session_factory, get_tm_session
from pyramid.threadlocal import get_current_registry

class SQLAlchemyHandler(logging.Handler):

    @staticmethod
    def get_log_db_session():
        import transaction
        settings = get_current_registry().settings
        engine = get_engine(settings)
        session_factory = get_session_factory(engine)
        return get_tm_session(session_factory, transaction.manager)

    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = logging.Formatter('', exc).format(record)
        log = Log(logger=record.__dict__['name'], level=record.__dict__['levelname'], trace=trace, msg=record.__dict__['msg'])
        dbsession = self.get_log_db_session()
        dbsession.add(log)
        transaction.commit()