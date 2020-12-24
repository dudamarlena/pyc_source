# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/slack_webhook_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5317 bytes
import json
from airflow.hooks.http_hook import HttpHook
from airflow.exceptions import AirflowException

class SlackWebhookHook(HttpHook):
    __doc__ = '\n    This hook allows you to post messages to Slack using incoming webhooks.\n    Takes both Slack webhook token directly and connection that has Slack webhook token.\n    If both supplied, http_conn_id will be used as base_url,\n    and webhook_token will be taken as endpoint, the relative path of the url.\n\n    Each Slack webhook token can be pre-configured to use a specific channel, username and\n    icon. You can override these defaults in this hook.\n\n    :param http_conn_id: connection that has Slack webhook token in the extra field\n    :type http_conn_id: str\n    :param webhook_token: Slack webhook token\n    :type webhook_token: str\n    :param message: The message you want to send on Slack\n    :type message: str\n    :param attachments: The attachments to send on Slack. Should be a list of\n                        dictionaries representing Slack attachments.\n    :type attachments: list\n    :param channel: The channel the message should be posted to\n    :type channel: str\n    :param username: The username to post to slack with\n    :type username: str\n    :param icon_emoji: The emoji to use as icon for the user posting to Slack\n    :type icon_emoji: str\n    :param icon_url: The icon image URL string to use in place of the default icon.\n    :type icon_url: str\n    :param link_names: Whether or not to find and link channel and usernames in your\n                       message\n    :type link_names: bool\n    :param proxy: Proxy to use to make the Slack webhook call\n    :type proxy: str\n    '

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