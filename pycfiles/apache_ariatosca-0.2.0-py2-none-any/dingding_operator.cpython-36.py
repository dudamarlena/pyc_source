# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/dingding_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2873 bytes
from airflow.contrib.hooks.dingding_hook import DingdingHook
from airflow.operators.bash_operator import BaseOperator
from airflow.utils.decorators import apply_defaults

class DingdingOperator(BaseOperator):
    """DingdingOperator"""
    template_fields = ('message', )
    ui_color = '#4ea4d4'

    @apply_defaults
    def __init__(self, dingding_conn_id='dingding_default', message_type='text', message=None, at_mobiles=None, at_all=False, *args, **kwargs):
        (super(DingdingOperator, self).__init__)(*args, **kwargs)
        self.dingding_conn_id = dingding_conn_id
        self.message_type = message_type
        self.message = message
        self.at_mobiles = at_mobiles
        self.at_all = at_all

    def execute(self, context):
        self.log.info('Sending Dingding message.')
        hook = DingdingHook(self.dingding_conn_id, self.message_type, self.message, self.at_mobiles, self.at_all)
        hook.send()