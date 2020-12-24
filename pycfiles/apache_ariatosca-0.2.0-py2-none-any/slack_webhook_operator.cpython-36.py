# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/slack_webhook_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4173 bytes
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.slack_webhook_hook import SlackWebhookHook

class SlackWebhookOperator(SimpleHttpOperator):
    """SlackWebhookOperator"""
    template_fields = [
     'webhook_token', 'message', 'attachments', 'channel',
     'username', 'proxy']

    @apply_defaults
    def __init__(self, http_conn_id=None, webhook_token=None, message='', attachments=None, channel=None, username=None, icon_emoji=None, icon_url=None, link_names=False, proxy=None, *args, **kwargs):
        (super(SlackWebhookOperator, self).__init__)(args, endpoint=webhook_token, **kwargs)
        self.http_conn_id = http_conn_id
        self.webhook_token = webhook_token
        self.message = message
        self.attachments = attachments
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji
        self.icon_url = icon_url
        self.link_names = link_names
        self.proxy = proxy
        self.hook = None

    def execute(self, context):
        """
        Call the SlackWebhookHook to post the provided Slack message
        """
        self.hook = SlackWebhookHook(self.http_conn_id, self.webhook_token, self.message, self.attachments, self.channel, self.username, self.icon_emoji, self.icon_url, self.link_names, self.proxy)
        self.hook.execute()