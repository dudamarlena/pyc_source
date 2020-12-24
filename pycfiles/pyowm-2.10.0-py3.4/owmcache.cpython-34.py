# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/abstractions/owmcache.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2087 bytes
"""
Module containing the abstract PyOWM cache provider
"""
from abc import ABCMeta, abstractmethod

class OWMCache(object):
    __doc__ = '\n    A global abstract class representing a caching provider which can be used\n    to lookup the JSON responses to the most recently or most frequently issued\n    OWM Weather API requests.\n    The purpose of the caching mechanism is to avoid OWM Weather API requests and\n    therefore network traffic: the implementations should be adapted to the\n    time/memory requirements of the OWM data clients (i.e: a "slimmer" cache\n    with lower lookup times but higher miss rates or a "fatter" cache with\n    higher memory consumption and higher hit rates?).\n    Subclasses should implement a proper caching algorithms bearing in mind\n    that different weather data types may have different change rates: in\n    example, observed weather can change very frequently while long-period\n    weather forecasts change less frequently.\n    External caching mechanisms (eg: memcached, redis, etc..) can be used by\n    extending this class into a proper decorator for the correspondent Python\n    bindings.\n    '
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