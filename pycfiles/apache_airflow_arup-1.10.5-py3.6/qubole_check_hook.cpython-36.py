# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/qubole_check_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3783 bytes
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.contrib.hooks.qubole_hook import QuboleHook
from airflow.exceptions import AirflowException
from qds_sdk.commands import Command
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

COL_DELIM = '\t'
ROW_DELIM = '\r\n'

def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def isbool(value):
    try:
        if value.lower() in ('true', 'false'):
            return True
    except ValueError:
        return False


def parse_first_row(row_list):
    record_list = []
    first_row = row_list[0] if row_list else ''
    for col_value in first_row.split(COL_DELIM):
        if isint(col_value):
            col_value = int(col_value)
        else:
            if isfloat(col_value):
                col_value = float(col_value)
            else:
                if isbool(col_value):
                    col_value = col_value.lower() == 'true'
        record_list.append(col_value)

    return record_list


class QuboleCheckHook(QuboleHook):

    def __init__(self, context, *args, **kwargs):
        (super(QuboleCheckHook, self).__init__)(*args, **kwargs)
        self.results_parser_callable = parse_first_row
        if 'results_parser_callable' in kwargs:
            if kwargs['results_parser_callable'] is not None:
                if not callable(kwargs['results_parser_callable']):
                    raise AirflowException('`results_parser_callable` param must be callable')
                self.results_parser_callable = kwargs['results_parser_callable']
        self.context = context

    @staticmethod
    def handle_failure_retry(context):
        ti = context['ti']
        cmd_id = ti.xcom_pull(key='qbol_cmd_id', task_ids=(ti.task_id))
        if cmd_id is not None:
            cmd = Command.find(cmd_id)
            if cmd is not None:
                if cmd.status == 'running':
                    log = LoggingMixin().log
                    log.info('Cancelling the Qubole Command Id: %s', cmd_id)
                    cmd.cancel()

    def get_first(self, sql):
        self.execute(context=(self.context))
        query_result = self.get_query_results()
        row_list = list(filter(None, query_result.split(ROW_DELIM)))
        record_list = self.results_parser_callable(row_list)
        return record_list

    def get_query_results(self):
        log = LoggingMixin().log
        if self.cmd is not None:
            cmd_id = self.cmd.id
            log.info('command id: ' + str(cmd_id))
            query_result_buffer = StringIO()
            self.cmd.get_results(fp=query_result_buffer, inline=True, delim=COL_DELIM)
            query_result = query_result_buffer.getvalue()
            query_result_buffer.close()
            return query_result
        log.info('Qubole command not found')