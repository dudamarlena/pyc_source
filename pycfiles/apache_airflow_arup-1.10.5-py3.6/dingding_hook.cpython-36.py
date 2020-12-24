# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/dingding_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5180 bytes
import json, requests
from airflow import AirflowException
from airflow.hooks.http_hook import HttpHook

class DingdingHook(HttpHook):
    __doc__ = '\n    This hook allows you send Dingding message using Dingding custom bot.\n    Get Dingding token from conn_id.password. And prefer set domain to\n    conn_id.host, if not will use default ``https://oapi.dingtalk.com``.\n\n    For more detail message in\n    `Dingding custom bot <https://open-doc.dingtalk.com/microapp/serverapi2/qf2nxq>`_\n\n    :param dingding_conn_id: The name of the Dingding connection to use\n    :type dingding_conn_id: str\n    :param message_type: Message type you want to send to Dingding, support five type so far\n        including text, link, markdown, actionCard, feedCard\n    :type message_type: str\n    :param message: The message send to Dingding chat group\n    :type message: str or dict\n    :param at_mobiles: Remind specific users with this message\n    :type at_mobiles: list[str]\n    :param at_all: Remind all people in group or not. If True, will overwrite ``at_mobiles``\n    :type at_all: bool\n    '

    def __init__(self, dingding_conn_id='dingding_default', message_type='text', message=None, at_mobiles=None, at_all=False, *args, **kwargs):
        (super(DingdingHook, self).__init__)(args, http_conn_id=dingding_conn_id, **kwargs)
        self.message_type = message_type
        self.message = message
        self.at_mobiles = at_mobiles
        self.at_all = at_all

    def _get_endpoint(self):
        """
        Get Dingding endpoint for sending message.
        """
        conn = self.get_connection(self.http_conn_id)
        token = conn.password
        if not token:
            raise AirflowException('Dingding token is requests but get nothing, check you conn_id configuration.')
        return 'robot/send?access_token={}'.format(token)

    def _build_message(self):
        """
        Build different type of Dingding message
        As most commonly used type, text message just need post message content
        rather than a dict like ``{'content': 'message'}``
        """
        if self.message_type in ('text', 'markdown'):
            data = {'msgtype': self.message_type, 
             self.message_type: {'content': self.message} if self.message_type == 'text' else self.message, 
             
             'at': {'atMobiles':self.at_mobiles, 
                    'isAtAll':self.at_all}}
        else:
            data = {'msgtype': self.message_type, 
             self.message_type: self.message}
        return json.dumps(data)

    def get_conn(self, headers=None):
        """
        Overwrite HttpHook get_conn because just need base_url and headers and
        not don't need generic params

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        conn = self.get_connection(self.http_conn_id)
        self.base_url = conn.host if conn.host else 'https://oapi.dingtalk.com'
        session = requests.Session()
        if headers:
            session.headers.update(headers)
        return session

    def send(self):
        """
        Send Dingding message
        """
        support_type = [
         'text', 'link', 'markdown', 'actionCard', 'feedCard']
        if self.message_type not in support_type:
            raise ValueError('DingdingWebhookHook only support {} so far, but receive {}'.format(support_type, self.message_type))
        data = self._build_message()
        self.log.info('Sending Dingding type %s message %s', self.message_type, data)
        resp = self.run(endpoint=(self._get_endpoint()), data=data,
          headers={'Content-Type': 'application/json'})
        if int(resp.json().get('errcode')) != 0:
            raise AirflowException('Send Dingding message failed, receive error message %s', resp.text)
        self.log.info('Success Send Dingding message')