# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-ppc/egg/validino/messages.py
# Compiled at: 2007-12-06 13:09:46
from threading import local
from pkg_resources import resource_stream

def loadMessages(relative_to=__name__, location='messages.txt'):
    fp = resource_stream(relative_to, location)
    d = {}
    for line in fp:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        (key, value) = line.split(',', 1)
        d[key] = value

    return d


_messagelocal = local()
_messagelocal.messages = loadMessages()

def getMessages():
    return _messagelocal.messages


def setMessages(messages):
    _messagelocal.messages = messages


__all__ = [
 'getMessages', 'setMessages', 'loadMessages']
try:
    from contextlib import contextmanager
except ImportError:
    pass
else:

    @contextmanager
    def msg(messages):
        oldmessages = _messagelocal.messages
        _messagelocal.messages = messages
        try:
            yield
        finally:
            _messagelocal.messages = oldmessages


    __all__.append('msg')