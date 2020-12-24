# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/caches/nullcache.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 887 bytes
__doc__ = '\nModule containing a null-object cache for OWM Weather API responses\n'
from pyowm.abstractions import owmcache

class NullCache(owmcache.OWMCache):
    """NullCache"""

    def __init__(self):
        pass

    def get(self, request_url):
        """
        Always returns ``None`` (nothing will ever be cached or looked up!)

        :param request_url: the request URL
        :type request_url: str
        :returns: ``None``

        """
        pass

    def set(self, request_url, response_json):
        """
        Does nothing.

        :param request_url: the request URL
        :type request_url: str
        :param response_json: the response JSON
        :type response_json: str

        """
        pass

    def __repr__(self):
        return '<%s.%s>' % (__name__, self.__class__.__name__)