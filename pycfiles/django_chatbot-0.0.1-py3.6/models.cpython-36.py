# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django/chatbot/models.py
# Compiled at: 2020-03-22 14:48:20
# Size of source mod 2**32: 548 bytes
from django.db import models

class Sender(models.Model):
    messengerSenderID = models.TextField()
    topic = models.TextField()


class Memory(models.Model):
    sender = models.ForeignKey(Sender, on_delete=(models.CASCADE))
    key = models.TextField()
    value = models.TextField()


class Conversation(models.Model):
    sender = models.ForeignKey(Sender, on_delete=(models.CASCADE))
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    bot = models.BooleanField(default=True)