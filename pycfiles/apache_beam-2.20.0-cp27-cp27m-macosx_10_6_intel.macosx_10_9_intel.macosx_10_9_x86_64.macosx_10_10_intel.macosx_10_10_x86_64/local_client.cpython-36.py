# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/client/local_client.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2211 bytes
__doc__ = 'Local client API'
from airflow.api.client import api_client
from airflow.api.common.experimental import pool
from airflow.api.common.experimental import trigger_dag
from airflow.api.common.experimental import delete_dag

class Client(api_client.Client):
    """Client"""

    def trigger_dag(self, dag_id, run_id=None, conf=None, execution_date=None):
        dag_run = trigger_dag.trigger_dag(dag_id=dag_id, run_id=run_id,
          conf=conf,
          execution_date=execution_date)
        return 'Created {}'.format(dag_run)

    def delete_dag(self, dag_id):
        count = delete_dag.delete_dag(dag_id)
        return 'Removed {} record(s)'.format(count)

    def get_pool(self, name):
        the_pool = pool.get_pool(name=name)
        return (
         the_pool.pool, the_pool.slots, the_pool.description)

    def get_pools(self):
        return [(p.pool, p.slots, p.description) for p in pool.get_pools()]

    def create_pool(self, name, slots, description):
        the_pool = pool.create_pool(name=name, slots=slots, description=description)
        return (
         the_pool.pool, the_pool.slots, the_pool.description)

    def delete_pool(self, name):
        the_pool = pool.delete_pool(name=name)
        return (
         the_pool.pool, the_pool.slots, the_pool.description)