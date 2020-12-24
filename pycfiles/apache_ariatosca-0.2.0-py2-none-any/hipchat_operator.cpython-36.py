# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/hipchat_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5170 bytes
from builtins import str
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator
from airflow.exceptions import AirflowException
import requests, json

class HipChatAPIOperator(BaseOperator):
    """HipChatAPIOperator"""

    @apply_defaults
    def __init__(self, token, base_url='https://api.hipchat.com/v2', *args, **kwargs):
        (super(HipChatAPIOperator, self).__init__)(*args, **kwargs)
        self.token = token
        self.base_url = base_url
        self.method = None
        self.url = None
        self.body = None

    def prepare_request(self):
        """
        Used by the execute function. Set the request method, url, and body of HipChat's
        REST API call.
        Override in child class. Each HipChatAPI child operator is responsible for having
        a prepare_request method call which sets self.method, self.url, and self.body.
        """
        pass

    def execute(self, context):
        self.prepare_request()
        response = requests.request((self.method), (self.url),
          headers={'Content-Type':'application/json', 
         'Authorization':'Bearer %s' % self.token},
          data=(self.body))
        if response.status_code >= 400:
            self.log.error('HipChat API call failed: %s %s', response.status_code, response.reason)
            raise AirflowException('HipChat API call failed: %s %s' % (
             response.status_code, response.reason))


class HipChatAPISendRoomNotificationOperator(HipChatAPIOperator):
    """HipChatAPISendRoomNotificationOperator"""
    template_fields = ('token', 'room_id', 'message')
    ui_color = '#2980b9'

    @apply_defaults
    def __init__(self, room_id, message, *args, **kwargs):
        (super(HipChatAPISendRoomNotificationOperator, self).__init__)(*args, **kwargs)
        self.room_id = room_id
        self.message = message
        default_options = {'message_format':'html', 
         'color':'yellow', 
         'frm':'airflow', 
         'attach_to':None, 
         'notify':False, 
         'card':None}
        for prop, default in default_options.items():
            setattr(self, prop, kwargs.get(prop, default))

    def prepare_request(self):
        params = {'message':self.message, 
         'message_format':self.message_format, 
         'color':self.color, 
         'from':self.frm, 
         'attach_to':self.attach_to, 
         'notify':self.notify, 
         'card':self.card}
        self.method = 'POST'
        self.url = '%s/room/%s/notification' % (self.base_url, self.room_id)
        self.body = json.dumps(dict((str(k), str(v)) for k, v in params.items() if v))