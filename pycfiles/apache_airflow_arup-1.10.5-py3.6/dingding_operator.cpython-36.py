# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/dingding_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2873 bytes
from airflow.contrib.hooks.dingding_hook import DingdingHook
from airflow.operators.bash_operator import BaseOperator
from airflow.utils.decorators import apply_defaults

class DingdingOperator(BaseOperator):
    __doc__ = '\n    This operator allows you send Dingding message using Dingding custom bot.\n    Get Dingding token from conn_id.password. And prefer set domain to\n    conn_id.host, if not will use default ``https://oapi.dingtalk.com``.\n\n    For more detail message in\n    `Dingding custom bot <https://open-doc.dingtalk.com/microapp/serverapi2/qf2nxq>`_\n\n    :param dingding_conn_id: The name of the Dingding connection to use\n    :type dingding_conn_id: str\n    :param message_type: Message type you want to send to Dingding, support five type so far\n        including text, link, markdown, actionCard, feedCard\n    :type message_type: str\n    :param message: The message send to Dingding chat group\n    :type message: str or dict\n    :param at_mobiles: Remind specific users with this message\n    :type at_mobiles: list[str]\n    :param at_all: Remind all people in group or not. If True, will overwrite ``at_mobiles``\n    :type at_all: bool\n    '
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