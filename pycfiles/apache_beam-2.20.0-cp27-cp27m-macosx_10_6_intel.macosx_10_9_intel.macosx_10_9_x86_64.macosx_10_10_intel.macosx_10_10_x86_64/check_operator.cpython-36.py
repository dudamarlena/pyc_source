# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/check_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 12344 bytes
from builtins import str, zip
from typing import Optional, Any, Iterable, Dict, SupportsAbs
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class CheckOperator(BaseOperator):
    """CheckOperator"""
    template_fields = ('sql', )
    template_ext = ('.hql', '.sql')
    ui_color = '#fff7e6'

    @apply_defaults
    def __init__(self, sql, conn_id=None, *args, **kwargs):
        (super(CheckOperator, self).__init__)(*args, **kwargs)
        self.conn_id = conn_id
        self.sql = sql

    def execute(self, context=None):
        self.log.info('Executing SQL check: %s', self.sql)
        records = self.get_db_hook().get_first(self.sql)
        self.log.info('Record: %s', records)
        if not records:
            raise AirflowException('The query returned None')
        else:
            if not all([bool(r) for r in records]):
                raise AirflowException('Test failed.\nQuery:\n{query}\nResults:\n{records!s}'.format(query=(self.sql),
                  records=records))
        self.log.info('Success.')

    def get_db_hook(self):
        return BaseHook.get_hook(conn_id=(self.conn_id))


def _convert_to_float_if_possible(s):
    """
    A small helper function to convert a string to a numeric value
    if appropriate

    :param s: the string to be converted
    :type s: str
    """
    try:
        ret = float(s)
    except (ValueError, TypeError):
        ret = s

    return ret


class ValueCheckOperator(BaseOperator):
    """ValueCheckOperator"""
    __mapper_args__ = {'polymorphic_identity': 'ValueCheckOperator'}
    template_fields = ('sql', 'pass_value')
    template_ext = ('.hql', '.sql')
    ui_color = '#fff7e6'

    @apply_defaults
    def __init__(self, sql, pass_value, tolerance=None, conn_id=None, *args, **kwargs):
        (super(ValueCheckOperator, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.conn_id = conn_id
        self.pass_value = str(pass_value)
        tol = _convert_to_float_if_possible(tolerance)
        self.tol = tol if isinstance(tol, float) else None
        self.has_tolerance = self.tol is not None

    def execute(self, context=None):
        self.log.info('Executing SQL check: %s', self.sql)
        records = self.get_db_hook().get_first(self.sql)
        if not records:
            raise AirflowException('The query returned None')
        else:
            pass_value_conv = _convert_to_float_if_possible(self.pass_value)
            is_numeric_value_check = isinstance(pass_value_conv, float)
            tolerance_pct_str = str(self.tol * 100) + '%' if self.has_tolerance else None
            error_msg = 'Test failed.\nPass value:{pass_value_conv}\nTolerance:{tolerance_pct_str}\nQuery:\n{sql}\nResults:\n{records!s}'.format(pass_value_conv=pass_value_conv,
              tolerance_pct_str=tolerance_pct_str,
              sql=(self.sql),
              records=records)
            if not is_numeric_value_check:
                tests = self._get_string_matches(records, pass_value_conv)
            else:
                if is_numeric_value_check:
                    try:
                        numeric_records = self._to_float(records)
                    except (ValueError, TypeError):
                        raise AirflowException('Converting a result to float failed.\n{}'.format(error_msg))

                    tests = self._get_numeric_matches(numeric_records, pass_value_conv)
                else:
                    tests = []
        if not all(tests):
            raise AirflowException(error_msg)

    def _to_float(self, records):
        return [float(record) for record in records]

    def _get_string_matches(self, records, pass_value_conv):
        return [str(record) == pass_value_conv for record in records]

    def _get_numeric_matches(self, numeric_records, numeric_pass_value_conv):
        if self.has_tolerance:
            return [numeric_pass_value_conv * (1 - self.tol) <= record <= numeric_pass_value_conv * (1 + self.tol) for record in numeric_records]
        else:
            return [record == numeric_pass_value_conv for record in numeric_records]

    def get_db_hook(self):
        return BaseHook.get_hook(conn_id=(self.conn_id))


class IntervalCheckOperator(BaseOperator):
    """IntervalCheckOperator"""
    __mapper_args__ = {'polymorphic_identity': 'IntervalCheckOperator'}
    template_fields = ('sql1', 'sql2')
    template_ext = ('.hql', '.sql')
    ui_color = '#fff7e6'
    ratio_formulas = {'max_over_min':lambda cur, ref: float(max(cur, ref)) / min(cur, ref), 
     'relative_diff':lambda cur, ref: float(abs(cur - ref)) / ref}

    @apply_defaults
    def __init__(self, table, metrics_thresholds, date_filter_column='ds', days_back=-7, ratio_formula='max_over_min', ignore_zero=True, conn_id=None, *args, **kwargs):
        (super(IntervalCheckOperator, self).__init__)(*args, **kwargs)
        if ratio_formula not in self.ratio_formulas:
            msg_template = 'Invalid diff_method: {diff_method}. Supported diff methods are: {diff_methods}'
            raise AirflowException(msg_template.format(diff_method=ratio_formula, diff_methods=(self.ratio_formulas)))
        self.ratio_formula = ratio_formula
        self.ignore_zero = ignore_zero
        self.table = table
        self.metrics_thresholds = metrics_thresholds
        self.metrics_sorted = sorted(metrics_thresholds.keys())
        self.date_filter_column = date_filter_column
        self.days_back = -abs(days_back)
        self.conn_id = conn_id
        sqlexp = ', '.join(self.metrics_sorted)
        sqlt = 'SELECT {sqlexp} FROM {table} WHERE {date_filter_column}='.format(sqlexp=sqlexp,
          table=table,
          date_filter_column=date_filter_column)
        self.sql1 = sqlt + "'{{ ds }}'"
        self.sql2 = sqlt + "'{{ macros.ds_add(ds, " + str(self.days_back) + ") }}'"

    def execute(self, context=None):
        hook = self.get_db_hook()
        self.log.info('Using ratio formula: %s', self.ratio_formula)
        self.log.info('Executing SQL check: %s', self.sql2)
        row2 = hook.get_first(self.sql2)
        self.log.info('Executing SQL check: %s', self.sql1)
        row1 = hook.get_first(self.sql1)
        if not row2:
            raise AirflowException('The query {} returned None'.format(self.sql2))
        if not row1:
            raise AirflowException('The query {} returned None'.format(self.sql1))
        current = dict(zip(self.metrics_sorted, row1))
        reference = dict(zip(self.metrics_sorted, row2))
        ratios = {}
        test_results = {}
        for m in self.metrics_sorted:
            cur = current[m]
            ref = reference[m]
            threshold = self.metrics_thresholds[m]
            if cur == 0 or ref == 0:
                ratios[m] = None
                test_results[m] = self.ignore_zero
            else:
                ratios[m] = self.ratio_formulas[self.ratio_formula](current[m], reference[m])
                test_results[m] = ratios[m] < threshold
            self.log.info('Current metric for %s: %s\nPast metric for %s: %s\nRatio for %s: %s\nThreshold: %s\n', m, cur, m, ref, m, ratios[m], threshold)

        if not all(test_results.values()):
            failed_tests = [it[0] for it in test_results.items() if not it[1]]
            j = len(failed_tests)
            n = len(self.metrics_sorted)
            self.log.warning('The following %s tests out of %s failed:', j, n)
            for k in failed_tests:
                self.log.warning("'%s' check failed. %s is above %s", k, ratios[k], self.metrics_thresholds[k])

            raise AirflowException('The following tests have failed:\n {0}'.format(', '.join(sorted(failed_tests))))
        self.log.info('All tests have passed')

    def get_db_hook(self):
        return BaseHook.get_hook(conn_id=(self.conn_id))