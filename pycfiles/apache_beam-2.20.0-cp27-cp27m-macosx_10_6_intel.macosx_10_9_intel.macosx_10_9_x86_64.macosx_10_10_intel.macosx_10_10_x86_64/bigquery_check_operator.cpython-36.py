# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/bigquery_check_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5858 bytes
from airflow.contrib.hooks.bigquery_hook import BigQueryHook
from airflow.operators.check_operator import CheckOperator, ValueCheckOperator, IntervalCheckOperator
from airflow.utils.decorators import apply_defaults

class BigQueryCheckOperator(CheckOperator):
    """BigQueryCheckOperator"""
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
    """BigQueryValueCheckOperator"""
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
    """BigQueryIntervalCheckOperator"""
    template_fields = ('table', )

    @apply_defaults
    def __init__(self, table, metrics_thresholds, date_filter_column='ds', days_back=-7, bigquery_conn_id='bigquery_default', use_legacy_sql=True, *args, **kwargs):
        (super(BigQueryIntervalCheckOperator, self).__init__)(args, table=table, metrics_thresholds=metrics_thresholds, date_filter_column=date_filter_column, days_back=days_back, **kwargs)
        self.bigquery_conn_id = bigquery_conn_id
        self.use_legacy_sql = use_legacy_sql

    def get_db_hook(self):
        return BigQueryHook(bigquery_conn_id=(self.bigquery_conn_id), use_legacy_sql=(self.use_legacy_sql))