# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django/chatbot/apps.py
# Compiled at: 2020-03-22 14:48:20
# Size of source mod 2**32: 238 bytes
from __future__ import unicode_literals
from django.apps import AppConfig
from .chatbot import start_chatbot_engine

class DjangoChatBotConfig(AppConfig):
    name = 'django.chatbot'

    def ready(self):
        start_chatbot_engine()