# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/contrib/messaging/consumers.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 3586 bytes
from django.contrib.auth.models import AnonymousUser
import django.utils.translation as _
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
import json

class MessagingConsumer(AsyncJsonWebsocketConsumer):
    user = AnonymousUser()

    def __init__(self, *args, **kwargs):
        (super(MessagingConsumer, self).__init__)(*args, **kwargs)

    async def connect(self):
        self.user = self.scope['user']
        if self.user == AnonymousUser():
            raise DenyConnection(_('Invalid User'))
        await self.accept()
        rooms = self.add_to_rooms()
        rooms = await rooms
        rooms.add('broadcast')
        rooms.add(self.user.username)
        for room_id in list(rooms):
            await self.channel_layer.group_add(room_id, self.channel_name)

    async def receive_json(self, content, **kwargs):
        pass

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        pass

    async def send_data(self, event):
        """
        Called when someone has send data.
        """
        params = event['data']
        await self.send_json(params)

    @database_sync_to_async
    def add_to_rooms(self):
        l = set()
        from aparnik.contrib.chats.models import ChatSession
        for room_id in ChatSession.objects.user_session(user=(self.user)).values_list('uri', flat=True):
            l.add(room_id)

        return l