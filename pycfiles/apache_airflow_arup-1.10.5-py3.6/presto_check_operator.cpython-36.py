# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/presto_check_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4677 bytes
from airflow.hooks.presto_hook import PrestoHook
from airflow.operators.check_operator import CheckOperator, ValueCheckOperator, IntervalCheckOperator
from airflow.utils.decorators import apply_defaults

class PrestoCheckOperator(CheckOperator):
    __doc__ = '\n    Performs checks against Presto. The ``PrestoCheckOperator`` expects\n    a sql query that will return a single row. Each value on that\n    first row is evaluated using python ``bool`` casting. If any of the\n    values return ``False`` the check is failed and errors out.\n\n    Note that Python bool casting evals the following as ``False``:\n\n    * ``False``\n    * ``0``\n    * Empty string (``""``)\n    * Empty list (``[]``)\n    * Empty dictionary or set (``{}``)\n\n    Given a query like ``SELECT COUNT(*) FROM foo``, it will fail only if\n    the count ``== 0``. You can craft much more complex query that could,\n    for instance, check that the table has the same number of rows as\n    the source table upstream, or that the count of today\'s partition is\n    greater than yesterday\'s partition, or that a set of metrics are less\n    than 3 standard deviation for the 7 day average.\n\n    This operator can be used as a data quality check in your pipeline, and\n    depending on where you put it in your DAG, you have the choice to\n    stop the critical path, preventing from\n    publishing dubious data, or on the side and receive email alerts\n    without stopping the progress of the DAG.\n\n    :param sql: the sql to be executed\n    :type sql: str\n    :param presto_conn_id: reference to the Presto database\n    :type presto_conn_id: str\n    '

    @apply_defaults
    def __init__(self, sql, presto_conn_id='presto_default', *args, **kwargs):
        (super(PrestoCheckOperator, self).__init__)(args, sql=sql, **kwargs)
        self.presto_conn_id = presto_conn_id
        self.sql = sql

    def get_db_hook(self):
        return PrestoHook(presto_conn_id=(self.presto_conn_id))


class PrestoValueCheckOperator(ValueCheckOperator):
    __doc__ = '\n    Performs a simple value check using sql code.\n\n    :param sql: the sql to be executed\n    :type sql: str\n    :param presto_conn_id: reference to the Presto database\n    :type presto_conn_id: str\n    '

    @apply_defaults
    def __init__(self, sql, pass_value, tolerance=None, presto_conn_id='presto_default', *args, **kwargs):
        (super(PrestoValueCheckOperator, self).__init__)(args, sql=sql, pass_value=pass_value, tolerance=tolerance, **kwargs)
        self.presto_conn_id = presto_conn_id

    def get_db_hook(self):
        return PrestoHook(presto_conn_id=(self.presto_conn_id))


class PrestoIntervalCheckOperator(IntervalCheckOperator):
    __doc__ = '\n    Checks that the values of metrics given as SQL expressions are within\n    a certain tolerance of the ones from days_back before.\n\n    :param table: the table name\n    :type table: str\n    :param days_back: number of days between ds and the ds we want to check\n        against. Defaults to 7 days\n    :type days_back: int\n    :param metrics_threshold: a dictionary of ratios indexed by metrics\n    :type metrics_threshold: dict\n    :param presto_conn_id: reference to the Presto database\n    :type presto_conn_id: str\n    '

    @apply_defaults
    def __init__(self, table, metrics_thresholds, date_filter_column='ds', days_back=-7, presto_conn_id='presto_default', *args, **kwargs):
        (super(PrestoIntervalCheckOperator, self).__init__)(args, table=table, metrics_thresholds=metrics_thresholds, date_filter_column=date_filter_column, days_back=days_back, **kwargs)
        self.presto_conn_id = presto_conn_id

    def get_db_hook(self):
        return PrestoHook(presto_conn_id=(self.presto_conn_id))