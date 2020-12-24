# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/qubole_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 10313 bytes
from typing import Iterable
from airflow.models.baseoperator import BaseOperator, BaseOperatorLink
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.qubole_hook import QuboleHook, COMMAND_ARGS, HYPHEN_ARGS, flatten_list, POSITIONAL_ARGS

class QDSLink(BaseOperatorLink):
    name = 'Go to QDS'

    def get_link(self, operator, dttm):
        return operator.get_hook().get_extra_links(operator, dttm)


class QuboleOperator(BaseOperator):
    """QuboleOperator"""
    template_fields = ('query', 'script_location', 'sub_command', 'script', 'files',
                       'archives', 'program', 'cmdline', 'sql', 'where_clause', 'tags',
                       'extract_query', 'boundary_query', 'macros', 'name', 'parameters',
                       'dbtap_id', 'hive_table', 'db_table', 'split_column', 'note_id',
                       'db_update_keys', 'export_dir', 'partition_spec', 'qubole_conn_id',
                       'arguments', 'user_program_arguments', 'cluster_label')
    template_ext = ('.txt', )
    ui_color = '#3064A1'
    ui_fgcolor = '#fff'
    qubole_hook_allowed_args_list = ['command_type', 'qubole_conn_id', 'fetch_logs']
    operator_extra_links = (
     QDSLink(),)

    @apply_defaults
    def __init__(self, qubole_conn_id='qubole_default', *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.kwargs['qubole_conn_id'] = qubole_conn_id
        self.hook = None
        filtered_base_kwargs = self._get_filtered_args(kwargs)
        (super(QuboleOperator, self).__init__)(*args, **filtered_base_kwargs)
        if self.on_failure_callback is None:
            self.on_failure_callback = QuboleHook.handle_failure_retry
        if self.on_retry_callback is None:
            self.on_retry_callback = QuboleHook.handle_failure_retry

    def _get_filtered_args(self, all_kwargs):
        qubole_args = flatten_list(COMMAND_ARGS.values()) + HYPHEN_ARGS + flatten_list(POSITIONAL_ARGS.values()) + self.qubole_hook_allowed_args_list
        return {key:value for key, value in all_kwargs.items() if key not in qubole_args}

    def execute(self, context):
        return self.get_hook().execute(context)

    def on_kill(self, ti=None):
        if self.hook:
            self.hook.kill(ti)
        else:
            self.get_hook().kill(ti)

    def get_results(self, ti=None, fp=None, inline=True, delim=None, fetch=True):
        return self.get_hook().get_results(ti, fp, inline, delim, fetch)

    def get_log(self, ti):
        return self.get_hook().get_log(ti)

    def get_jobs_id(self, ti):
        return self.get_hook().get_jobs_id(ti)

    def get_hook(self):
        return QuboleHook(*self.args, **self.kwargs)

    def __getattribute__(self, name):
        if name in QuboleOperator.template_fields:
            if name in self.kwargs:
                return self.kwargs[name]
            else:
                return ''
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in QuboleOperator.template_fields:
            self.kwargs[name] = value
        else:
            object.__setattr__(self, name, value)