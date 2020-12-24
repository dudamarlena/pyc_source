# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/fbnotify/main.py
# Compiled at: 2017-12-28 03:13:00
from fbchat.models import *
from fbchat import Client

class fbnotify:

    def __init__(self, email, password):
        self.client = Client(email, password)

    def send(self, message):
        self.client.send(Message(text=message), thread_id=self.client.uid, thread_type=ThreadType.USER)