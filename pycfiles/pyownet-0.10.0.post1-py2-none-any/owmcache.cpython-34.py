# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/abstractions/owmcache.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2087 bytes
__doc__ = '\nModule containing the abstract PyOWM cache provider\n'
from abc import ABCMeta, abstractmethod

class OWMCache(object):
    """OWMCache"""
    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, request_url):
        """
        In case of a hit, returns the JSON string which represents the OWM web
        API response to the request being identified by a specific string URL.

        :param request_url: an URL that uniquely identifies the request whose
            response is to be looked up
        :type request_url: str
        :returns: a JSON str in case of cache hit or ``None`` otherwise

        """
        raise NotImplementedError

    @abstractmethod
    def set(self, request_url, response_json):
        """
        Adds the specified response_json value to the cache using as a lookup
        key the request_url of the request that generated the value.

        :param request_url: the request URL
        :type request_url: str
        :param response_json: the response JSON
        :type response_json: str

        """
        raise NotImplementedError