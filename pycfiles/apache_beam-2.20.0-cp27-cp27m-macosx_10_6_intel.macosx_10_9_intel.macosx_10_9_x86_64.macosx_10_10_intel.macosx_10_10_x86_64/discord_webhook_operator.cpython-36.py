# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/discord_webhook_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3847 bytes
from airflow.contrib.hooks.discord_webhook_hook import DiscordWebhookHook
from airflow.exceptions import AirflowException
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.utils.decorators import apply_defaults

class DiscordWebhookOperator(SimpleHttpOperator):
    """DiscordWebhookOperator"""
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