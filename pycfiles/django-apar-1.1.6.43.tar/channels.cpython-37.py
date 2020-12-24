# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/messaging/channels.py
# Compiled at: 2020-02-28 04:29:50
# Size of source mod 2**32: 5205 bytes
"""Base Implementation of a Delivery Backend."""
import abc
from json import dumps
import six, channels.layers
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from . import default_settings as settings
from django.core.management import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import get_user_model
from django.utils.timezone import now
import dateutil.relativedelta as relativedelta
from django.utils.text import Truncator
import json
from fcm_django.models import FCMDevice
from aparnik.utils.utils import get_request
from aparnik.contrib.settings.models import Setting
from aparnik.contrib.notifications.models import Notification
from aparnik.contrib.basemodels.api.serializers import ModelListPolymorphicSerializer
from aparnik.settings import aparnik_settings
User = get_user_model()
UserSummeryListSerializer = aparnik_settings.USER_SUMMARY_LIST_SERIALIZER

@six.add_metaclass(abc.ABCMeta)
class BaseNotificationChannel:
    __doc__ = 'Base channel for sending notifications.'

    def __init__(self, **kwargs):
        self.notification_kwargs = kwargs

    @abc.abstractmethod
    def construct_message(self):
        """Constructs a message from notification details."""
        pass

    @abc.abstractmethod
    def notify(self, message):
        """Sends the notification."""
        pass


class ConsoleChannel(BaseNotificationChannel):
    __doc__ = 'Dummy channel that prints to the console.'

    def construct_message(self):
        """Stringify the notification kwargs."""
        return str(self.notification_kwargs)

    def notify(self, message):
        print(message)


class BasicWebSocketChannel(BaseNotificationChannel):
    __doc__ = 'It creates a Redis user for each user (based on their username).'

    def _connect(self):
        channel_layer = channels.layers.get_channel_layer()
        return channel_layer

    def construct_message(self):
        """Construct message from notification details."""
        return self.notification_kwargs

    def notify(self, message):
        """
        Puts a new message on the queue.
        
        The queue is named based on the username (for Uniqueness)
        """
        uri = self.notification_kwargs['uri']
        if not uri:
            return
        channel_layer = self._connect()
        async_to_sync(channel_layer.group_send)(uri, {'type':'send_data', 
         'data':message})


class BasicPushNotificationChannel(BaseNotificationChannel):

    def construct_message(self):
        """Construct message from notification details."""
        username_source = self.notification_kwargs['source']
        user_source_serial = None
        if username_source:
            user_source = User.objects.filter(username=username_source).first()
            user_source_serial = json.dumps((UserSummeryListSerializer(user_source, many=False, read_only=True, context={'request': get_request()}).data), sort_keys=True, indent=1, cls=DjangoJSONEncoder) if user_source else None
        message = {'title':self.notification_kwargs['short_description'],  'body':'', 
         'data':{'model':self.notification_kwargs['extra_data']['message'], 
          'from_user':user_source_serial, 
          'type':Notification.NOTIFICATION_INFO, 
          'title':self.notification_kwargs['short_description'], 
          'description':''}}
        return message

    def notify(self, message):
        """
        Puts a new message on the queue.

        The queue is named based on the username (for Uniqueness)
        """
        uri = self.notification_kwargs['uri']
        recipient = self.notification_kwargs['recipient']
        if not uri:
            if not recipient:
                return
        try:
            devices = FCMDevice.objects.filter(user__in=User.objects.filter(username=recipient)).order_by('device_id').distinct()
            sent_result = (devices.send_message)(**message)
            print(sent_result)
        except Exception as inst:
            try:
                print('Error happen')
                print(inst)
            finally:
                inst = None
                del inst