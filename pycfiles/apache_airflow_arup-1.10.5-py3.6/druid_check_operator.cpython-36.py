# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/druid_check_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3542 bytes
from airflow.exceptions import AirflowException
from airflow.hooks.druid_hook import DruidDbApiHook
from airflow.operators.check_operator import CheckOperator
from airflow.utils.decorators import apply_defaults

class DruidCheckOperator(CheckOperator):
    __doc__ = '\n    Performs checks against Druid. The ``DruidCheckOperator`` expects\n    a sql query that will return a single row. Each value on that\n    first row is evaluated using python ``bool`` casting. If any of the\n    values return ``False`` the check is failed and errors out.\n\n    Note that Python bool casting evals the following as ``False``:\n\n    * ``False``\n    * ``0``\n    * Empty string (``""``)\n    * Empty list (``[]``)\n    * Empty dictionary or set (``{}``)\n\n    Given a query like ``SELECT COUNT(*) FROM foo``, it will fail only if\n    the count ``== 0``. You can craft much more complex query that could,\n    for instance, check that the table has the same number of rows as\n    the source table upstream, or that the count of today\'s partition is\n    greater than yesterday\'s partition, or that a set of metrics are less\n    than 3 standard deviation for the 7 day average.\n    This operator can be used as a data quality check in your pipeline, and\n    depending on where you put it in your DAG, you have the choice to\n    stop the critical path, preventing from\n    publishing dubious data, or on the side and receive email alerts\n    without stopping the progress of the DAG.\n\n    :param sql: the sql to be executed\n    :type sql: str\n    :param druid_broker_conn_id: reference to the druid broker\n    :type druid_broker_conn_id: str\n    '

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