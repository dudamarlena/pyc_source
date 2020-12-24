# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/Cellar/python/2.7.10_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/geventwebsocket/__init__.py
# Compiled at: 2015-11-13 17:02:49
VERSION = (0, 9, 5, 'final', 0)
__all__ = [
 'WebSocketApplication',
 'Resource',
 'WebSocketServer',
 'WebSocketError',
 'get_version']

def get_version(*args, **kwargs):
    from .utils import get_version
    return get_version(*args, **kwargs)


try:
    from .resource import WebSocketApplication, Resource
    from .server import WebSocketServer
    from .exceptions import WebSocketError
except ImportError:
    pass