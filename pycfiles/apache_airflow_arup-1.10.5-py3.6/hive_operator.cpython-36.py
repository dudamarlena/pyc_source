# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Executes hql code or hive script in a specific Hive database.\n\n    :param hql: the hql to be executed. Note that you may also use\n        a relative path from the dag file of a (template) hive\n        script. (templated)\n    :type hql: str\n    :param hive_cli_conn_id: reference to the Hive database. (templated)\n    :type hive_cli_conn_id: str\n    :param hiveconfs: if defined, these key value pairs will be passed\n        to hive as ``-hiveconf "key"="value"``\n    :type hiveconfs: dict\n    :param hiveconf_jinja_translate: when True, hiveconf-type templating\n        ${var} gets translated into jinja-type templating {{ var }} and\n        ${hiveconf:var} gets translated into jinja-type templating {{ var }}.\n        Note that you may want to use this along with the\n        ``DAG(user_defined_macros=myargs)`` parameter. View the DAG\n        object documentation for more details.\n    :type hiveconf_jinja_translate: bool\n    :param script_begin_tag: If defined, the operator will get rid of the\n        part of the script before the first occurrence of `script_begin_tag`\n    :type script_begin_tag: str\n    :param mapred_queue: queue used by the Hadoop CapacityScheduler. (templated)\n    :type  mapred_queue: str\n    :param mapred_queue_priority: priority within CapacityScheduler queue.\n        Possible settings include: VERY_HIGH, HIGH, NORMAL, LOW, VERY_LOW\n    :type  mapred_queue_priority: str\n    :param mapred_job_name: This name will appear in the jobtracker.\n        This can make monitoring easier.\n    :type  mapred_job_name: str\n    '
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