# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/slack_webhook_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5317 bytes
import json
from airflow.hooks.http_hook import HttpHook
from airflow.exceptions import AirflowException

class SlackWebhookHook(HttpHook):
    """SlackWebhookHook"""

    def __init__(self, http_conn_id=None, webhook_token=None, message='', attachments=None, channel=None, username=None, icon_emoji=None, icon_url=None, link_names=False, proxy=None, *args, **kwargs):
        (super(SlackWebhookHook, self).__init__)(args, http_conn_id=http_conn_id, **kwargs)
        self.webhook_token = self._get_token(webhook_token, http_conn_id)
        self.message = message
        self.attachments = attachments
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji
        self.icon_url = icon_url
        self.link_names = link_names
        self.proxy = proxy

    def _get_token(self, token, http_conn_id):
        """
        Given either a manually set token or a conn_id, return the webhook_token to use
        :param token: The manually provided token
        :type token: str
        :param http_conn_id: The conn_id provided
        :type http_conn_id: str
        :return: webhook_token (str) to use
        """
        if token:
            return token
        if http_conn_id:
            conn = self.get_connection(http_conn_id)
            extra = conn.extra_dejson
            return extra.get('webhook_token', '')
        raise AirflowException('Cannot get token: No valid Slack webhook token nor conn_id supplied')

    def _build_slack_message(self):
        """
        Construct the Slack message. All relevant parameters are combined here to a valid
        Slack json message
        :return: Slack message (str) to send
        """
        cmd = {}
        if self.channel:
            cmd['channel'] = self.channel
        if self.username:
            cmd['username'] = self.username
        if self.icon_emoji:
            cmd['icon_emoji'] = self.icon_emoji
        if self.icon_url:
            cmd['icon_url'] = self.icon_url
        if self.link_names:
            cmd['link_names'] = 1
        if self.attachments:
            cmd['attachments'] = self.attachments
        cmd['text'] = self.message
        return json.dumps(cmd)

    def execute(self):
        """
        Remote Popen (actually execute the slack webhook call)
        """
        proxies = {}
        if self.proxy:
            proxies = {'https': self.proxy}
        slack_message = self._build_slack_message()
        self.run(endpoint=(self.webhook_token), data=slack_message,
          headers={'Content-type': 'application/json'},
          extra_options={'proxies': proxies})