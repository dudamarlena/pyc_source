# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/discord_webhook_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5376 bytes
import json, re
from airflow.hooks.http_hook import HttpHook
from airflow.exceptions import AirflowException

class DiscordWebhookHook(HttpHook):
    __doc__ = '\n    This hook allows you to post messages to Discord using incoming webhooks.\n    Takes a Discord connection ID with a default relative webhook endpoint. The\n    default endpoint can be overridden using the webhook_endpoint parameter\n    (https://discordapp.com/developers/docs/resources/webhook).\n\n    Each Discord webhook can be pre-configured to use a specific username and\n    avatar_url. You can override these defaults in this hook.\n\n    :param http_conn_id: Http connection ID with host as "https://discord.com/api/" and\n                         default webhook endpoint in the extra field in the form of\n                         {"webhook_endpoint": "webhooks/{webhook.id}/{webhook.token}"}\n    :type http_conn_id: str\n    :param webhook_endpoint: Discord webhook endpoint in the form of\n                             "webhooks/{webhook.id}/{webhook.token}"\n    :type webhook_endpoint: str\n    :param message: The message you want to send to your Discord channel\n                    (max 2000 characters)\n    :type message: str\n    :param username: Override the default username of the webhook\n    :type username: str\n    :param avatar_url: Override the default avatar of the webhook\n    :type avatar_url: str\n    :param tts: Is a text-to-speech message\n    :type tts: bool\n    :param proxy: Proxy to use to make the Discord webhook call\n    :type proxy: str\n    '

    def __init__(self, http_conn_id=None, webhook_endpoint=None, message='', username=None, avatar_url=None, tts=False, proxy=None, *args, **kwargs):
        (super(DiscordWebhookHook, self).__init__)(*args, **kwargs)
        self.http_conn_id = http_conn_id
        self.webhook_endpoint = self._get_webhook_endpoint(http_conn_id, webhook_endpoint)
        self.message = message
        self.username = username
        self.avatar_url = avatar_url
        self.tts = tts
        self.proxy = proxy

    def _get_webhook_endpoint(self, http_conn_id, webhook_endpoint):
        """
        Given a Discord http_conn_id, return the default webhook endpoint or override if a
        webhook_endpoint is manually supplied.

        :param http_conn_id: The provided connection ID
        :param webhook_endpoint: The manually provided webhook endpoint
        :return: Webhook endpoint (str) to use
        """
        if webhook_endpoint:
            endpoint = webhook_endpoint
        else:
            if http_conn_id:
                conn = self.get_connection(http_conn_id)
                extra = conn.extra_dejson
                endpoint = extra.get('webhook_endpoint', '')
            else:
                raise AirflowException('Cannot get webhook endpoint: No valid Discord webhook endpoint or http_conn_id supplied.')
        if not re.match('^webhooks/[0-9]+/[a-zA-Z0-9_-]+$', endpoint):
            raise AirflowException('Expected Discord webhook endpoint in the form of "webhooks/{webhook.id}/{webhook.token}".')
        return endpoint

    def _build_discord_payload(self):
        """
        Construct the Discord JSON payload. All relevant parameters are combined here
        to a valid Discord JSON payload.

        :return: Discord payload (str) to send
        """
        payload = {}
        if self.username:
            payload['username'] = self.username
        else:
            if self.avatar_url:
                payload['avatar_url'] = self.avatar_url
            payload['tts'] = self.tts
            if len(self.message) <= 2000:
                payload['content'] = self.message
            else:
                raise AirflowException('Discord message length must be 2000 or fewer characters.')
        return json.dumps(payload)

    def execute(self):
        """
        Execute the Discord webhook call
        """
        proxies = {}
        if self.proxy:
            proxies = {'https': self.proxy}
        discord_payload = self._build_discord_payload()
        self.run(endpoint=(self.webhook_endpoint), data=discord_payload,
          headers={'Content-type': 'application/json'},
          extra_options={'proxies': proxies})