# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/pig_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2707 bytes
import re
from airflow.hooks.pig_hook import PigCliHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class PigOperator(BaseOperator):
    __doc__ = '\n    Executes pig script.\n\n    :param pig: the pig latin script to be executed. (templated)\n    :type pig: str\n    :param pig_cli_conn_id: reference to the Hive database\n    :type pig_cli_conn_id: str\n    :param pigparams_jinja_translate: when True, pig params-type templating\n        ${var} gets translated into jinja-type templating {{ var }}. Note that\n        you may want to use this along with the\n        ``DAG(user_defined_macros=myargs)`` parameter. View the DAG\n        object documentation for more details.\n    :type pigparams_jinja_translate: bool\n    :param pig_opts: pig options, such as: -x tez, -useHCatalog, ...\n    :type pig_opts: str\n    '
    template_fields = ('pig', )
    template_ext = ('.pig', '.piglatin')
    ui_color = '#f0e4ec'

    @apply_defaults
    def __init__(self, pig, pig_cli_conn_id='pig_cli_default', pigparams_jinja_translate=False, pig_opts=None, *args, **kwargs):
        (super(PigOperator, self).__init__)(*args, **kwargs)
        self.pigparams_jinja_translate = pigparams_jinja_translate
        self.pig = pig
        self.pig_cli_conn_id = pig_cli_conn_id
        self.pig_opts = pig_opts

    def get_hook(self):
        return PigCliHook(pig_cli_conn_id=(self.pig_cli_conn_id))

    def prepare_template(self):
        if self.pigparams_jinja_translate:
            self.pig = re.sub('(\\$([a-zA-Z_][a-zA-Z0-9_]*))', '{{ \\g<2> }}', self.pig)

    def execute(self, context):
        self.log.info('Executing: %s', self.pig)
        self.hook = self.get_hook()
        self.hook.run_cli(pig=(self.pig), pig_opts=(self.pig_opts))

    def on_kill(self):
        self.hook.kill()