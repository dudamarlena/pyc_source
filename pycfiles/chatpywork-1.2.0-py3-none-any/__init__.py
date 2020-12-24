# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatpy\__init__.py
# Compiled at: 2015-01-11 14:50:45
__doc__ = '\nChatwork API library\n'
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