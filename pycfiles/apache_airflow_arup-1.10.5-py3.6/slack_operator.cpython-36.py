# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/slack_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5189 bytes
import json
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.slack_hook import SlackHook
from airflow.exceptions import AirflowException

class SlackAPIOperator(BaseOperator):
    __doc__ = '\n    Base Slack Operator\n    The SlackAPIPostOperator is derived from this operator.\n    In the future additional Slack API Operators will be derived from this class as well\n\n    :param slack_conn_id: Slack connection ID which its password is Slack API token\n    :type slack_conn_id: str\n    :param token: Slack API token (https://api.slack.com/web)\n    :type token: str\n    :param method: The Slack API Method to Call (https://api.slack.com/methods)\n    :type method: str\n    :param api_params: API Method call parameters (https://api.slack.com/methods)\n    :type api_params: dict\n    '

    @apply_defaults
    def __init__(self, slack_conn_id=None, token=None, method=None, api_params=None, *args, **kwargs):
        (super(SlackAPIOperator, self).__init__)(*args, **kwargs)
        if token is None:
            if slack_conn_id is None:
                raise AirflowException('No valid Slack token nor slack_conn_id supplied.')
        if token is not None:
            if slack_conn_id is not None:
                raise AirflowException('Cannot determine Slack credential when both token and slack_conn_id are supplied.')
        self.token = token
        self.slack_conn_id = slack_conn_id
        self.method = method
        self.api_params = api_params

    def construct_api_call_params(self):
        """
        Used by the execute function. Allows templating on the source fields
        of the api_call_params dict before construction

        Override in child classes.
        Each SlackAPIOperator child class is responsible for
        having a construct_api_call_params function
        which sets self.api_call_params with a dict of
        API call parameters (https://api.slack.com/methods)
        """
        pass

    def execute(self, **kwargs):
        """
        SlackAPIOperator calls will not fail even if the call is not unsuccessful.
        It should not prevent a DAG from completing in success
        """
        if not self.api_params:
            self.construct_api_call_params()
        slack = SlackHook(token=(self.token), slack_conn_id=(self.slack_conn_id))
        slack.call(self.method, self.api_params)


class SlackAPIPostOperator(SlackAPIOperator):
    __doc__ = '\n    Posts messages to a slack channel\n\n    :param channel: channel in which to post message on slack name (#general) or\n        ID (C12318391). (templated)\n    :type channel: str\n    :param username: Username that airflow will be posting to Slack as. (templated)\n    :type username: str\n    :param text: message to send to slack. (templated)\n    :type text: str\n    :param icon_url: url to icon used for this message\n    :type icon_url: str\n    :param attachments: extra formatting details. (templated)\n        - see https://api.slack.com/docs/attachments.\n    :type attachments: array of hashes\n    '
    template_fields = ('username', 'text', 'attachments', 'channel')
    ui_color = '#FFBA40'

    @apply_defaults
    def __init__(self, channel='#general', username='Airflow', text='No message has been set.\nHere is a cat video instead\nhttps://www.youtube.com/watch?v=J---aiyznGQ', icon_url='https://raw.githubusercontent.com/apache/airflow/master/airflow/www/static/pin_100.jpg', attachments=None, *args, **kwargs):
        self.method = 'chat.postMessage'
        self.channel = channel
        self.username = username
        self.text = text
        self.icon_url = icon_url
        self.attachments = attachments
        (super(SlackAPIPostOperator, self).__init__)(args, method=self.method, **kwargs)

    def construct_api_call_params(self):
        self.api_params = {'channel':self.channel, 
         'username':self.username, 
         'text':self.text, 
         'icon_url':self.icon_url, 
         'attachments':json.dumps(self.attachments)}