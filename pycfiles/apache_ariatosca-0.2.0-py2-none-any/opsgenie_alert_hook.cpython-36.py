# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/opsgenie_alert_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3202 bytes
import json, requests
from airflow.hooks.http_hook import HttpHook
from airflow import AirflowException

class OpsgenieAlertHook(HttpHook):
    """OpsgenieAlertHook"""

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