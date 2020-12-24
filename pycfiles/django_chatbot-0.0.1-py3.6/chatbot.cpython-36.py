# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django/chatbot/chatbot.py
# Compiled at: 2020-03-22 14:48:20
# Size of source mod 2**32: 450 bytes
from django.conf import settings

class __Chat:
    pass


chat = __Chat()

def start_chatbot_engine():
    from .handler import initiate_chat
    if hasattr(settings, 'CHATBOT_TEMPLATE'):
        chat_obj = initiate_chat(settings.CHATBOT_TEMPLATE)
    else:
        chat_obj = initiate_chat()
    for attribute in dir(chat_obj):
        if attribute[0] != '_':
            setattr(chat, attribute, getattr(chat_obj, attribute))