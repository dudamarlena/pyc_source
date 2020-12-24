# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/hive_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5801 bytes
from __future__ import unicode_literals
import re
from airflow.hooks.hive_hooks import HiveCliHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.utils.operator_helpers import context_to_airflow_vars

class HiveOperator(BaseOperator):
    """HiveOperator"""
    template_fields = ('hql', 'schema', 'hive_cli_conn_id', 'mapred_queue', 'hiveconfs',
                       'mapred_job_name', 'mapred_queue_priority')
    template_ext = ('.hql', '.sql')
    ui_color = '#f0e4ec'

    @apply_defaults
    def __init__(self, hql, hive_cli_conn_id='hive_cli_default', schema='default', hiveconfs=None, hiveconf_jinja_translate=False, script_begin_tag=None, run_as_owner=False, mapred_queue=None, mapred_queue_priority=None, mapred_job_name=None, *args, **kwargs):
        (super(HiveOperator, self).__init__)(*args, **kwargs)
        self.hql = hql
        self.hive_cli_conn_id = hive_cli_conn_id
        self.schema = schema
        self.hiveconfs = hiveconfs or {}
        self.hiveconf_jinja_translate = hiveconf_jinja_translate
        self.script_begin_tag = script_begin_tag
        self.run_as = None
        if run_as_owner:
            self.run_as = self.dag.owner
        self.mapred_queue = mapred_queue
        self.mapred_queue_priority = mapred_queue_priority
        self.mapred_job_name = mapred_job_name
        self.hook = None

    def get_hook(self):
        return HiveCliHook(hive_cli_conn_id=(self.hive_cli_conn_id),
          run_as=(self.run_as),
          mapred_queue=(self.mapred_queue),
          mapred_queue_priority=(self.mapred_queue_priority),
          mapred_job_name=(self.mapred_job_name))

    def prepare_template(self):
        if self.hiveconf_jinja_translate:
            self.hql = re.sub('(\\$\\{(hiveconf:)?([ a-zA-Z0-9_]*)\\})', '{{ \\g<3> }}', self.hql)
        if self.script_begin_tag:
            if self.script_begin_tag in self.hql:
                self.hql = '\n'.join(self.hql.split(self.script_begin_tag)[1:])

    def execute(self, context):
        self.log.info('Executing: %s', self.hql)
        self.hook = self.get_hook()
        if not self.mapred_job_name:
            ti = context['ti']
            self.hook.mapred_job_name = 'Airflow HiveOperator task for {}.{}.{}.{}'.format(ti.hostname.split('.')[0], ti.dag_id, ti.task_id, ti.execution_date.isoformat())
        else:
            if self.hiveconf_jinja_translate:
                self.hiveconfs = context_to_airflow_vars(context)
            else:
                self.hiveconfs.update(context_to_airflow_vars(context))
        self.log.info('Passing HiveConf: %s', self.hiveconfs)
        self.hook.run_cli(hql=(self.hql), schema=(self.schema), hive_conf=(self.hiveconfs))

    def dry_run(self):
        self.hook = self.get_hook()
        self.hook.test_hql(hql=(self.hql))

    def on_kill(self):
        if self.hook:
            self.hook.kill()