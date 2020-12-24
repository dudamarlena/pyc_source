# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/base_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3321 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os, random
from typing import Iterable
from airflow.models import Connection
from airflow.exceptions import AirflowException
from airflow.utils.db import provide_session
from airflow.utils.log.logging_mixin import LoggingMixin
CONN_ENV_PREFIX = 'AIRFLOW_CONN_'

class BaseHook(LoggingMixin):
    """BaseHook"""

    def __init__(self, source):
        pass

    @classmethod
    @provide_session
    def _get_connections_from_db(cls, conn_id, session=None):
        db = session.query(Connection).filter(Connection.conn_id == conn_id).all()
        session.expunge_all()
        if not db:
            raise AirflowException("The conn_id `{0}` isn't defined".format(conn_id))
        return db

    @classmethod
    def _get_connection_from_env(cls, conn_id):
        environment_uri = os.environ.get(CONN_ENV_PREFIX + conn_id.upper())
        conn = None
        if environment_uri:
            conn = Connection(conn_id=conn_id, uri=environment_uri)
        return conn

    @classmethod
    def get_connections(cls, conn_id):
        conn = cls._get_connection_from_env(conn_id)
        if conn:
            conns = [
             conn]
        else:
            conns = cls._get_connections_from_db(conn_id)
        return conns

    @classmethod
    def get_connection(cls, conn_id):
        conn = random.choice(list(cls.get_connections(conn_id)))
        if conn.host:
            log = LoggingMixin().log
            log.info('Using connection to: %s', conn.debug_info())
        return conn

    @classmethod
    def get_hook(cls, conn_id):
        connection = cls.get_connection(conn_id)
        return connection.get_hook()

    def get_conn(self):
        raise NotImplementedError()

    def get_records(self, sql):
        raise NotImplementedError()

    def get_pandas_df(self, sql):
        raise NotImplementedError()

    def run(self, sql):
        raise NotImplementedError()