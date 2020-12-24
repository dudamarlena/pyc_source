# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/druid_check_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3542 bytes
from airflow.exceptions import AirflowException
from airflow.hooks.druid_hook import DruidDbApiHook
from airflow.operators.check_operator import CheckOperator
from airflow.utils.decorators import apply_defaults

class DruidCheckOperator(CheckOperator):
    """DruidCheckOperator"""

    @apply_defaults
    def __init__(self, sql, druid_broker_conn_id='druid_broker_default', *args, **kwargs):
        (super(DruidCheckOperator, self).__init__)(args, sql=sql, **kwargs)
        self.druid_broker_conn_id = druid_broker_conn_id
        self.sql = sql

    def get_db_hook(self):
        """
        Return the druid db api hook.
        """
        return DruidDbApiHook(druid_broker_conn_id=(self.druid_broker_conn_id))

    def get_first(self, sql):
        """
        Executes the druid sql to druid broker and returns the first resulting row.

        :param sql: the sql statement to be executed (str)
        :type sql: str
        """
        with self.get_db_hook().get_conn() as (cur):
            cur.execute(sql)
            return cur.fetchone()

    def execute(self, context=None):
        self.log.info('Executing SQL check: %s', self.sql)
        record = self.get_first(self.sql)
        self.log.info('Record: %s', str(record))
        if not record:
            raise AirflowException('The query returned None')
        self.log.info('Success.')