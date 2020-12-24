# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/qubole_check_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 9033 bytes
from airflow.contrib.operators.qubole_operator import QuboleOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.qubole_check_hook import QuboleCheckHook
from airflow.operators.check_operator import CheckOperator, ValueCheckOperator
from airflow.exceptions import AirflowException

class QuboleCheckOperator(CheckOperator, QuboleOperator):
    """QuboleCheckOperator"""
    template_fields = QuboleOperator.template_fields + CheckOperator.template_fields
    template_ext = QuboleOperator.template_ext
    ui_fgcolor = '#000'

    @apply_defaults
    def __init__(self, qubole_conn_id='qubole_default', *args, **kwargs):
        sql = get_sql_from_qbol_cmd(kwargs)
        (super(QuboleCheckOperator, self).__init__)(args, qubole_conn_id=qubole_conn_id, sql=sql, **kwargs)
        self.on_failure_callback = QuboleCheckHook.handle_failure_retry
        self.on_retry_callback = QuboleCheckHook.handle_failure_retry

    def execute(self, context=None):
        try:
            self.hook = self.get_hook(context=context)
            super(QuboleCheckOperator, self).execute(context=context)
        except AirflowException as e:
            handle_airflow_exception(e, self.get_hook())

    def get_db_hook(self):
        return self.get_hook()

    def get_hook(self, context=None):
        if hasattr(self, 'hook'):
            if self.hook is not None:
                return self.hook
        return QuboleCheckHook(self.args, context=context, **self.kwargs)

    def __getattribute__(self, name):
        if name in QuboleCheckOperator.template_fields:
            if name in self.kwargs:
                return self.kwargs[name]
            else:
                return ''
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in QuboleCheckOperator.template_fields:
            self.kwargs[name] = value
        else:
            object.__setattr__(self, name, value)


class QuboleValueCheckOperator(ValueCheckOperator, QuboleOperator):
    """QuboleValueCheckOperator"""
    template_fields = QuboleOperator.template_fields + ValueCheckOperator.template_fields
    template_ext = QuboleOperator.template_ext
    ui_fgcolor = '#000'

    @apply_defaults
    def __init__(self, pass_value, tolerance=None, qubole_conn_id='qubole_default', *args, **kwargs):
        sql = get_sql_from_qbol_cmd(kwargs)
        (super(QuboleValueCheckOperator, self).__init__)(args, qubole_conn_id=qubole_conn_id, sql=sql, pass_value=pass_value, tolerance=tolerance, **kwargs)
        self.on_failure_callback = QuboleCheckHook.handle_failure_retry
        self.on_retry_callback = QuboleCheckHook.handle_failure_retry

    def execute(self, context=None):
        try:
            self.hook = self.get_hook(context=context)
            super(QuboleValueCheckOperator, self).execute(context=context)
        except AirflowException as e:
            handle_airflow_exception(e, self.get_hook())

    def get_db_hook(self):
        return self.get_hook()

    def get_hook(self, context=None):
        if hasattr(self, 'hook'):
            if self.hook is not None:
                return self.hook
        return QuboleCheckHook(self.args, context=context, **self.kwargs)

    def __getattribute__(self, name):
        if name in QuboleValueCheckOperator.template_fields:
            if name in self.kwargs:
                return self.kwargs[name]
            else:
                return ''
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in QuboleValueCheckOperator.template_fields:
            self.kwargs[name] = value
        else:
            object.__setattr__(self, name, value)


def get_sql_from_qbol_cmd(params):
    sql = ''
    if 'query' in params:
        sql = params['query']
    else:
        if 'sql' in params:
            sql = params['sql']
    return sql


def handle_airflow_exception(airflow_exception, hook):
    cmd = hook.cmd
    if cmd is not None:
        if cmd.is_success(cmd.status):
            qubole_command_results = hook.get_query_results()
            qubole_command_id = cmd.id
            exception_message = '\nQubole Command Id: {qubole_command_id}\nQubole Command Results:\n{qubole_command_results}'.format(qubole_command_id=qubole_command_id,
              qubole_command_results=qubole_command_results)
            raise AirflowException(str(airflow_exception) + exception_message)
    raise AirflowException(str(airflow_exception))