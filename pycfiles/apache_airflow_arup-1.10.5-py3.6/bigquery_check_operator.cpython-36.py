# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_check_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5858 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.operators.check_operator import CheckOperator, ValueCheckOperator, IntervalCheckOperator
from airflow.utils.decorators import apply_defaults

class BigQueryCheckOperator(CheckOperator):
    __doc__ = '\n    Performs checks against BigQuery. The ``BigQueryCheckOperator`` expects\n    a sql query that will return a single row. Each value on that\n    first row is evaluated using python ``bool`` casting. If any of the\n    values return ``False`` the check is failed and errors out.\n\n    Note that Python bool casting evals the following as ``False``:\n\n    * ``False``\n    * ``0``\n    * Empty string (``""``)\n    * Empty list (``[]``)\n    * Empty dictionary or set (``{}``)\n\n    Given a query like ``SELECT COUNT(*) FROM foo``, it will fail only if\n    the count ``== 0``. You can craft much more complex query that could,\n    for instance, check that the table has the same number of rows as\n    the source table upstream, or that the count of today\'s partition is\n    greater than yesterday\'s partition, or that a set of metrics are less\n    than 3 standard deviation for the 7 day average.\n\n    This operator can be used as a data quality check in your pipeline, and\n    depending on where you put it in your DAG, you have the choice to\n    stop the critical path, preventing from\n    publishing dubious data, or on the side and receive email alerts\n    without stopping the progress of the DAG.\n\n    :param sql: the sql to be executed\n    :type sql: str\n    :param bigquery_conn_id: reference to the BigQuery database\n    :type bigquery_conn_id: str\n    :param use_legacy_sql: Whether to use legacy SQL (true)\n        or standard SQL (false).\n    :type use_legacy_sql: bool\n    '
    template_fields = ('sql', )
    template_ext = ('.sql', )

    @apply_defaults
    def __init__(self, sql, bigquery_conn_id='bigquery_default', use_legacy_sql=True, *args, **kwargs):
        (super(BigQueryCheckOperator, self).__init__)(args, sql=sql, **kwargs)
        self.bigquery_conn_id = bigquery_conn_id
        self.sql = sql
        self.use_legacy_sql = use_legacy_sql

    def get_db_hook(self):
        return BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), use_legacy_sql=(self.use_legacy_sql))


class BigQueryValueCheckOperator(ValueCheckOperator):
    __doc__ = '\n    Performs a simple value check using sql code.\n\n    :param sql: the sql to be executed\n    :type sql: str\n    :param use_legacy_sql: Whether to use legacy SQL (true)\n        or standard SQL (false).\n    :type use_legacy_sql: bool\n    '
    template_fields = ('sql', 'pass_value')
    template_ext = ('.sql', )

    @apply_defaults
    def __init__(self, sql, pass_value, tolerance=None, bigquery_conn_id='bigquery_default', use_legacy_sql=True, *args, **kwargs):
        (super(BigQueryValueCheckOperator, self).__init__)(args, sql=sql, pass_value=pass_value, tolerance=tolerance, **kwargs)
        self.bigquery_conn_id = bigquery_conn_id
        self.use_legacy_sql = use_legacy_sql

    def get_db_hook(self):
        return BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), use_legacy_sql=(self.use_legacy_sql))


class BigQueryIntervalCheckOperator(IntervalCheckOperator):
    __doc__ = "\n    Checks that the values of metrics given as SQL expressions are within\n    a certain tolerance of the ones from days_back before.\n\n    This method constructs a query like so ::\n\n        SELECT {metrics_threshold_dict_key} FROM {table}\n        WHERE {date_filter_column}=<date>\n\n    :param table: the table name\n    :type table: str\n    :param days_back: number of days between ds and the ds we want to check\n        against. Defaults to 7 days\n    :type days_back: int\n    :param metrics_threshold: a dictionary of ratios indexed by metrics, for\n        example 'COUNT(*)': 1.5 would require a 50 percent or less difference\n        between the current day, and the prior days_back.\n    :type metrics_threshold: dict\n    :param use_legacy_sql: Whether to use legacy SQL (true)\n        or standard SQL (false).\n    :type use_legacy_sql: bool\n    "
    template_fields = ('table', )

    @apply_defaults
    def __init__(self, table, metrics_thresholds, date_filter_column='ds', days_back=-7, bigquery_conn_id='bigquery_default', use_legacy_sql=True, *args, **kwargs):
        (super(BigQueryIntervalCheckOperator, self).__init__)(args, table=table, metrics_thresholds=metrics_thresholds, date_filter_column=date_filter_column, days_back=days_back, **kwargs)
        self.bigquery_conn_id = bigquery_conn_id
        self.use_legacy_sql = use_legacy_sql

    def get_db_hook(self):
        return BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), use_legacy_sql=(self.use_legacy_sql))