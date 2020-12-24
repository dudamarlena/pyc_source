# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/presto_check_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4677 bytes
from airflow.hooks.presto_hook import PrestoHook
from airflow.operators.check_operator import CheckOperator, ValueCheckOperator, IntervalCheckOperator
from airflow.utils.decorators import apply_defaults

class PrestoCheckOperator(CheckOperator):
    """PrestoCheckOperator"""

    @apply_defaults
    def __init__(self, sql, presto_conn_id='presto_default', *args, **kwargs):
        (super(PrestoCheckOperator, self).__init__)(args, sql=sql, **kwargs)
        self.presto_conn_id = presto_conn_id
        self.sql = sql

    def get_db_hook(self):
        return PrestoHook(presto_conn_id=(self.presto_conn_id))


class PrestoValueCheckOperator(ValueCheckOperator):
    """PrestoValueCheckOperator"""

    @apply_defaults
    def __init__(self, sql, pass_value, tolerance=None, presto_conn_id='presto_default', *args, **kwargs):
        (super(PrestoValueCheckOperator, self).__init__)(args, sql=sql, pass_value=pass_value, tolerance=tolerance, **kwargs)
        self.presto_conn_id = presto_conn_id

    def get_db_hook(self):
        return PrestoHook(presto_conn_id=(self.presto_conn_id))


class PrestoIntervalCheckOperator(IntervalCheckOperator):
    """PrestoIntervalCheckOperator"""

    @apply_defaults
    def __init__(self, table, metrics_thresholds, date_filter_column='ds', days_back=-7, presto_conn_id='presto_default', *args, **kwargs):
        (super(PrestoIntervalCheckOperator, self).__init__)(args, table=table, metrics_thresholds=metrics_thresholds, date_filter_column=date_filter_column, days_back=days_back, **kwargs)
        self.presto_conn_id = presto_conn_id

    def get_db_hook(self):
        return PrestoHook(presto_conn_id=(self.presto_conn_id))