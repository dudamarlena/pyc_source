# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/qubole_check_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 9033 bytes
from airflow.contrib.operators.qubole_operator import QuboleOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.qubole_check_hook import QuboleCheckHook
from airflow.operators.check_operator import CheckOperator, ValueCheckOperator
from airflow.exceptions import AirflowException

class QuboleCheckOperator(CheckOperator, QuboleOperator):
    __doc__ = '\n    Performs checks against Qubole Commands. ``QuboleCheckOperator`` expects\n    a command that will be executed on QDS.\n    By default, each value on first row of the result of this Qubole Command\n    is evaluated using python ``bool`` casting. If any of the\n    values return ``False``, the check is failed and errors out.\n\n    Note that Python bool casting evals the following as ``False``:\n\n    * ``False``\n    * ``0``\n    * Empty string (``""``)\n    * Empty list (``[]``)\n    * Empty dictionary or set (``{}``)\n\n    Given a query like ``SELECT COUNT(*) FROM foo``, it will fail only if\n    the count ``== 0``. You can craft much more complex query that could,\n    for instance, check that the table has the same number of rows as\n    the source table upstream, or that the count of today\'s partition is\n    greater than yesterday\'s partition, or that a set of metrics are less\n    than 3 standard deviation for the 7 day average.\n\n    This operator can be used as a data quality check in your pipeline, and\n    depending on where you put it in your DAG, you have the choice to\n    stop the critical path, preventing from\n    publishing dubious data, or on the side and receive email alerts\n    without stopping the progress of the DAG.\n\n    :param qubole_conn_id: Connection id which consists of qds auth_token\n    :type qubole_conn_id: str\n\n    kwargs:\n\n        Arguments specific to Qubole command can be referred from QuboleOperator docs.\n\n        :results_parser_callable: This is an optional parameter to\n            extend the flexibility of parsing the results of Qubole\n            command to the users. This is a python callable which\n            can hold the logic to parse list of rows returned by Qubole command.\n            By default, only the values on first row are used for performing checks.\n            This callable should return a list of records on\n            which the checks have to be performed.\n\n    .. note:: All fields in common with template fields of\n        QuboleOperator and CheckOperator are template-supported.\n\n    '
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
    __doc__ = '\n    Performs a simple value check using Qubole command.\n    By default, each value on the first row of this\n    Qubole command is compared with a pre-defined value.\n    The check fails and errors out if the output of the command\n    is not within the permissible limit of expected value.\n\n    :param qubole_conn_id: Connection id which consists of qds auth_token\n    :type qubole_conn_id: str\n\n    :param pass_value: Expected value of the query results.\n    :type pass_value: str or int or float\n\n    :param tolerance: Defines the permissible pass_value range, for example if\n        tolerance is 2, the Qubole command output can be anything between\n        -2*pass_value and 2*pass_value, without the operator erring out.\n\n    :type tolerance: int or float\n\n\n    kwargs:\n\n        Arguments specific to Qubole command can be referred from QuboleOperator docs.\n\n        :results_parser_callable: This is an optional parameter to\n            extend the flexibility of parsing the results of Qubole\n            command to the users. This is a python callable which\n            can hold the logic to parse list of rows returned by Qubole command.\n            By default, only the values on first row are used for performing checks.\n            This callable should return a list of records on\n            which the checks have to be performed.\n\n\n    .. note:: All fields in common with template fields of\n            QuboleOperator and ValueCheckOperator are template-supported.\n    '
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