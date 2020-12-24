# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/discord_webhook_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3847 bytes
from airflow.contrib.hooks.discord_webhook_hook import DiscordWebhookHook
from airflow.exceptions import AirflowException
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.utils.decorators import apply_defaults

class DiscordWebhookOperator(SimpleHttpOperator):
    __doc__ = '\n    This operator allows you to post messages to Discord using incoming webhooks.\n    Takes a Discord connection ID with a default relative webhook endpoint. The\n    default endpoint can be overridden using the webhook_endpoint parameter\n    (https://discordapp.com/developers/docs/resources/webhook).\n\n    Each Discord webhook can be pre-configured to use a specific username and\n    avatar_url. You can override these defaults in this operator.\n\n    :param http_conn_id: Http connection ID with host as "https://discord.com/api/" and\n                         default webhook endpoint in the extra field in the form of\n                         {"webhook_endpoint": "webhooks/{webhook.id}/{webhook.token}"}\n    :type http_conn_id: str\n    :param webhook_endpoint: Discord webhook endpoint in the form of\n                             "webhooks/{webhook.id}/{webhook.token}"\n    :type webhook_endpoint: str\n    :param message: The message you want to send to your Discord channel\n                    (max 2000 characters). (templated)\n    :type message: str\n    :param username: Override the default username of the webhook. (templated)\n    :type username: str\n    :param avatar_url: Override the default avatar of the webhook\n    :type avatar_url: str\n    :param tts: Is a text-to-speech message\n    :type tts: bool\n    :param proxy: Proxy to use to make the Discord webhook call\n    :type proxy: str\n    '
    template_fields = [
     'username', 'message']

    @apply_defaults
    def __init__(self, http_conn_id=None, webhook_endpoint=None, message='', username=None, avatar_url=None, tts=False, proxy=None, *args, **kwargs):
        (super(DiscordWebhookOperator, self).__init__)(args, endpoint=webhook_endpoint, **kwargs)
        if not http_conn_id:
            raise AirflowException('No valid Discord http_conn_id supplied.')
        self.http_conn_id = http_conn_id
        self.webhook_endpoint = webhook_endpoint
        self.message = message
        self.username = username
        self.avatar_url = avatar_url
        self.tts = tts
        self.proxy = proxy
        self.hook = None

    def execute(self, context):
        """
        Call the DiscordWebhookHook to post message
        """
        self.hook = DiscordWebhookHook(self.http_conn_id, self.webhook_endpoint, self.message, self.username, self.avatar_url, self.tts, self.proxy)
        self.hook.execute()