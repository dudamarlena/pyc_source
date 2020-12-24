# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/druid_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6130 bytes
from __future__ import print_function
import requests, time
from pydruid.db import connect
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.hooks.dbapi_hook import DbApiHook

class DruidHook(BaseHook):
    __doc__ = '\n    Connection to Druid overlord for ingestion\n\n    :param druid_ingest_conn_id: The connection id to the Druid overlord machine\n                                 which accepts index jobs\n    :type druid_ingest_conn_id: str\n    :param timeout: The interval between polling\n                    the Druid job for the status of the ingestion job.\n                    Must be greater than or equal to 1\n    :type timeout: int\n    :param max_ingestion_time: The maximum ingestion time before assuming the job failed\n    :type max_ingestion_time: int\n    '

    def __init__(self, druid_ingest_conn_id='druid_ingest_default', timeout=1, max_ingestion_time=None):
        self.druid_ingest_conn_id = druid_ingest_conn_id
        self.timeout = timeout
        self.max_ingestion_time = max_ingestion_time
        self.header = {'content-type': 'application/json'}
        if self.timeout < 1:
            raise ValueError('Druid timeout should be equal or greater than 1')

    def get_conn_url(self):
        conn = self.get_connection(self.druid_ingest_conn_id)
        host = conn.host
        port = conn.port
        conn_type = 'http' if not conn.conn_type else conn.conn_type
        endpoint = conn.extra_dejson.get('endpoint', '')
        return '{conn_type}://{host}:{port}/{endpoint}'.format(conn_type=conn_type,
          host=host,
          port=port,
          endpoint=endpoint)

    def submit_indexing_job(self, json_index_spec):
        url = self.get_conn_url()
        self.log.info('Druid ingestion spec: %s', json_index_spec)
        req_index = requests.post(url, json=json_index_spec, headers=(self.header))
        if req_index.status_code != 200:
            raise AirflowException('Did not get 200 when submitting the Druid job to {}'.format(url))
        req_json = req_index.json()
        druid_task_id = req_json['task']
        self.log.info('Druid indexing task-id: %s', druid_task_id)
        running = True
        sec = 0
        while running:
            req_status = requests.get('{0}/{1}/status'.format(url, druid_task_id))
            self.log.info('Job still running for %s seconds...', sec)
            if self.max_ingestion_time:
                if sec > self.max_ingestion_time:
                    requests.post('{0}/{1}/shutdown'.format(url, druid_task_id))
                    raise AirflowException('Druid ingestion took more than %s seconds', self.max_ingestion_time)
            time.sleep(self.timeout)
            sec = sec + self.timeout
            status = req_status.json()['status']['status']
            if status == 'RUNNING':
                running = True
            else:
                if status == 'SUCCESS':
                    running = False
                else:
                    if status == 'FAILED':
                        raise AirflowException('Druid indexing job failed, check console for more info')
                    else:
                        raise AirflowException('Could not get status of the job, got %s', status)

        self.log.info('Successful index')


class DruidDbApiHook(DbApiHook):
    __doc__ = '\n    Interact with Druid broker\n\n    This hook is purely for users to query druid broker.\n    For ingestion, please use druidHook.\n    '
    conn_name_attr = 'druid_broker_conn_id'
    default_conn_name = 'druid_broker_default'
    supports_autocommit = False

    def __init__(self, *args, **kwargs):
        (super(DruidDbApiHook, self).__init__)(*args, **kwargs)

    def get_conn(self):
        """
        Establish a connection to druid broker.
        """
        conn = self.get_connection(self.druid_broker_conn_id)
        druid_broker_conn = connect(host=(conn.host),
          port=(conn.port),
          path=(conn.extra_dejson.get('endpoint', '/druid/v2/sql')),
          scheme=(conn.extra_dejson.get('schema', 'http')))
        self.log.info('Get the connection to druid broker on %s', conn.host)
        return druid_broker_conn

    def get_uri(self):
        """
        Get the connection uri for druid broker.

        e.g: druid://localhost:8082/druid/v2/sql/
        """
        conn = self.get_connection(getattr(self, self.conn_name_attr))
        host = conn.host
        if conn.port is not None:
            host += ':{port}'.format(port=(conn.port))
        conn_type = 'druid' if not conn.conn_type else conn.conn_type
        endpoint = conn.extra_dejson.get('endpoint', 'druid/v2/sql')
        return '{conn_type}://{host}/{endpoint}'.format(conn_type=conn_type,
          host=host,
          endpoint=endpoint)

    def set_autocommit(self, conn, autocommit):
        raise NotImplementedError()

    def get_pandas_df(self, sql, parameters=None):
        raise NotImplementedError()

    def insert_rows(self, table, rows, target_fields=None, commit_every=1000):
        raise NotImplementedError()