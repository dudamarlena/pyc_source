# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/slack_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2295 bytes
from slackclient import SlackClient
from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException

class SlackHook(BaseHook):
    __doc__ = '\n       Interact with Slack, using slackclient library.\n    '

    def __init__(self, token=None, slack_conn_id=None):
        """
        Takes both Slack API token directly and connection that has Slack API token.

        If both supplied, Slack API token will be used.

        :param token: Slack API token
        :type token: str
        :param slack_conn_id: connection that has Slack API token in the password field
        :type slack_conn_id: str
        """
        self.token = self._SlackHook__get_token(token, slack_conn_id)

    def __get_token(self, token, slack_conn_id):
        if token is not None:
            return token
        if slack_conn_id is not None:
            conn = self.get_connection(slack_conn_id)
            if not getattr(conn, 'password', None):
                raise AirflowException('Missing token(password) in Slack connection')
            return conn.password
        raise AirflowException('Cannot get token: No valid Slack token nor slack_conn_id supplied.')

    def call(self, method, api_params):
        sc = SlackClient(self.token)
        rc = (sc.api_call)(method, **api_params)
        if not rc['ok']:
            msg = 'Slack API call failed ({})'.format(rc['error'])
            raise AirflowException(msg)