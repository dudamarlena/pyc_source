# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatpy\__init__.py
# Compiled at: 2015-01-11 14:50:45
"""
Chatwork API library
"""
__version__ = '0.2.2'
__license__ = 'MIT'
from chatpy.models import Status, ModelFactory
from chatpy.error import ChatpyError
from chatpy.api import API
from chatpy.cache import Cache, MemoryCache, FileCache
from chatpy.auth import TokenAuthHandler
api = API()

def debug(level=1):
    from six.moves import http_client
    http_client.HTTPConnection.debuglevel = level