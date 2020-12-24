# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/opsgenie_alert_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3202 bytes
import json, requests
from airflow.hooks.http_hook import HttpHook
from airflow import AirflowException

class OpsgenieAlertHook(HttpHook):
    __doc__ = "\n    This hook allows you to post alerts to Opsgenie.\n    Accepts a connection that has an Opsgenie API key as the connection's password.\n    This hook sets the domain to conn_id.host, and if not set will default\n    to ``https://api.opsgenie.com``.\n\n    Each Opsgenie API key can be pre-configured to a team integration.\n    You can override these defaults in this hook.\n\n    :param opsgenie_conn_id: The name of the Opsgenie connection to use\n    :type opsgenie_conn_id: str\n\n    "

    def __init__(self, opsgenie_conn_id='opsgenie_default', *args, **kwargs):
        (super(OpsgenieAlertHook, self).__init__)(args, http_conn_id=opsgenie_conn_id, **kwargs)

    def _get_api_key(self):
        """
        Get Opsgenie api_key for creating alert
        """
        conn = self.get_connection(self.http_conn_id)
        api_key = conn.password
        if not api_key:
            raise AirflowException('Opsgenie API Key is required for this hook, please check your conn_id configuration.')
        return api_key

    def get_conn(self, headers=None):
        """
        Overwrite HttpHook get_conn because this hook just needs base_url
        and headers, and does not need generic params

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        conn = self.get_connection(self.http_conn_id)
        self.base_url = conn.host if conn.host else 'https://api.opsgenie.com'
        session = requests.Session()
        if headers:
            session.headers.update(headers)
        return session

    def execute(self, payload={}):
        """
        Execute the Opsgenie Alert call

        :param payload: Opsgenie API Create Alert payload values
            See https://docs.opsgenie.com/docs/alert-api#section-create-alert
        :type payload: dict
        """
        api_key = self._get_api_key()
        return self.run(endpoint='v2/alerts', data=(json.dumps(payload)),
          headers={'Content-Type':'application/json', 
         'Authorization':'GenieKey %s' % api_key})