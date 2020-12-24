# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/hipchat_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5170 bytes
from builtins import str
from airflow.utils.decorators import apply_defaults
from airflow.models import BaseOperator
from airflow.exceptions import AirflowException
import requests, json

class HipChatAPIOperator(BaseOperator):
    __doc__ = "\n    Base HipChat Operator.\n    All derived HipChat operators reference from HipChat's official REST API documentation\n    at https://www.hipchat.com/docs/apiv2. Before using any HipChat API operators you need\n    to get an authentication token at https://www.hipchat.com/docs/apiv2/auth.\n    In the future additional HipChat operators will be derived from this class as well.\n\n    :param token: HipChat REST API authentication token\n    :type token: str\n    :param base_url: HipChat REST API base url.\n    :type base_url: str\n    "

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
    __doc__ = "\n    Send notification to a specific HipChat room.\n    More info: https://www.hipchat.com/docs/apiv2/method/send_room_notification\n\n    :param room_id: Room in which to send notification on HipChat. (templated)\n    :type room_id: str\n    :param message: The message body. (templated)\n    :type message: str\n    :param frm: Label to be shown in addition to sender's name\n    :type frm: str\n    :param message_format: How the notification is rendered: html or text\n    :type message_format: str\n    :param color: Background color of the msg: yellow, green, red, purple, gray, or random\n    :type color: str\n    :param attach_to: The message id to attach this notification to\n    :type attach_to: str\n    :param notify: Whether this message should trigger a user notification\n    :type notify: bool\n    :param card: HipChat-defined card object\n    :type card: dict\n    "
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