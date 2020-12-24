# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/slack_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5189 bytes
import json
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.slack_hook import SlackHook
from airflow.exceptions import AirflowException

class SlackAPIOperator(BaseOperator):
    """SlackAPIOperator"""

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
    """SlackAPIPostOperator"""
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