# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/slack_webhook_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4173 bytes
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.slack_webhook_hook import SlackWebhookHook

class SlackWebhookOperator(SimpleHttpOperator):
    __doc__ = '\n    This operator allows you to post messages to Slack using incoming webhooks.\n    Takes both Slack webhook token directly and connection that has Slack webhook token.\n    If both supplied, http_conn_id will be used as base_url,\n    and webhook_token will be taken as endpoint, the relative path of the url.\n\n    Each Slack webhook token can be pre-configured to use a specific channel, username and\n    icon. You can override these defaults in this hook.\n\n    :param http_conn_id: connection that has Slack webhook token in the extra field\n    :type http_conn_id: str\n    :param webhook_token: Slack webhook token\n    :type webhook_token: str\n    :param message: The message you want to send on Slack\n    :type message: str\n    :param attachments: The attachments to send on Slack. Should be a list of\n                        dictionaries representing Slack attachments.\n    :type attachments: list\n    :param channel: The channel the message should be posted to\n    :type channel: str\n    :param username: The username to post to slack with\n    :type username: str\n    :param icon_emoji: The emoji to use as icon for the user posting to Slack\n    :type icon_emoji: str\n    :param icon_url: The icon image URL string to use in place of the default icon.\n    :type icon_url: str\n    :param link_names: Whether or not to find and link channel and usernames in your\n                       message\n    :type link_names: bool\n    :param proxy: Proxy to use to make the Slack webhook call\n    :type proxy: str\n    '
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