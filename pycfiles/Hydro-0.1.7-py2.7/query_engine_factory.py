# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/query_engine_factory.py
# Compiled at: 2015-08-06 10:11:40
__author__ = 'moshebasanchig'
from hydro.query_engine import QueryEngine
from connector_factory import ConnectorHandler

class QueryEngineFactory(object):
    conn_handler = None

    @classmethod
    def __get_conn_handler(cls):
        if cls.conn_handler is None:
            cls.conn_handler = ConnectorHandler()
        return cls.conn_handler

    @classmethod
    def get_query_engine(cls, engine_type, cache_engine_instance, execution_plan, logger):
        cls.__get_conn_handler().set_logger(logger)
        query_engine = QueryEngine(engine_type, cls.conn_handler, cache_engine_instance, execution_plan, logger)
        return query_engine