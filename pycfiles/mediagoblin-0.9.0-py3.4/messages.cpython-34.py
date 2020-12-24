# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/messages.py
# Compiled at: 2013-09-23 12:05:52
# Size of source mod 2**32: 1558 bytes
from mediagoblin.tools import common
DEBUG = 'debug'
INFO = 'info'
SUCCESS = 'success'
WARNING = 'warning'
ERROR = 'error'
ADD_MESSAGE_TEST = []

def add_message(request, level, text):
    global ADD_MESSAGE_TEST
    messages = request.session.setdefault('messages', [])
    messages.append({'level': level,  'text': text})
    if common.TESTS_ENABLED:
        ADD_MESSAGE_TEST.append(messages)
    request.session.save()


def fetch_messages(request, clear_from_session=True):
    messages = request.session.get('messages')
    if messages:
        if clear_from_session:
            request.session['messages'] = []
            request.session.save()
    return messages


def clear_add_message():
    global ADD_MESSAGE_TEST
    ADD_MESSAGE_TEST = []