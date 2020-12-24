# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django/chatbot/__init__.py
# Compiled at: 2020-03-22 14:48:20
# Size of source mod 2**32: 161 bytes
from .chatbot import chat
VERSION = (0, 0, 1)
__version__ = '.'.join(map(str, VERSION))
default_app_config = 'django.chatbot.apps.DjangoChatBotConfig'