# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/REST/base_endpoint.py
# Compiled at: 2019-05-22 05:00:30
from __future__ import absolute_import
from twisted.web import resource
from twisted.web.resource import _computeAllowedMethods
from . import json_util as json

class BaseEndpoint(resource.Resource, object):
    """
    The base endpoint from which all other endpoints should extend to make them compatible with Cross-Origin Resource
    Sharing requests.
    """

    def __init__(self):
        resource.Resource.__init__(self)
        object.__init__(self)

    @staticmethod
    def twisted_dumps(obj, ensure_ascii=True):
        """
        Attempt to json.dumps() an object and encode it to convert it to bytes.
        This method is helpful when returning JSON data in twisted REST calls.

        :param obj: the object to serialize.
        :param ensure_ascii: allow binary strings to be sent
        :return: the JSON bytes representation of the object.
        """
        return json.dumps(obj, ensure_ascii).encode('utf-8')

    @staticmethod
    def twisted_loads(s, *args, **kwargs):
        """
        Attempt to json.loads() a bytes. This function wraps json.loads, to provide dumps and loads from the same file.

        :param s: the JSON formatted bytes to load objects from.
        :return: the Python object(s) extracted from the JSON input.
        """
        return json.loads(s.decode('utf-8'), *args, **kwargs)

    def render_OPTIONS(self, request):
        """
        This methods renders the HTTP OPTIONS method used for returning available HTTP methods and Cross-Origin Resource
        Sharing preflight request checks.
        """
        try:
            allowed_methods = self.allowedMethods
        except AttributeError:
            allowed_methods = _computeAllowedMethods(self)

        allowed_methods_string = (' ').join(allowed_methods)
        request.setHeader('Allow', allowed_methods_string)
        if request.getHeader('Access-Control-Request-Headers'):
            request.setHeader('Access-Control-Allow-Headers', request.getHeader('Access-Control-Request-Headers'))
        request.setHeader('Access-Control-Allow-Methods', allowed_methods_string)
        request.setHeader('Access-Control-Max-Age', 86400)
        return ''