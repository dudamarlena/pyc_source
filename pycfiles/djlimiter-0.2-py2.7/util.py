# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djlimiter/util.py
# Compiled at: 2015-01-08 23:14:56
import logging
from django.core.urlresolvers import resolve
from limits.util import parse, parse_many

def get_ipaddr(request):
    """
    :return: the ip address for the current request (or 127.0.0.1 if none found)
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    return ip


class LimitWrapper(object):
    """
    basic wrapper to encapsulate limits and their context
    """

    def __init__(self, limits, key_func, scope, per_method=False):
        self._limits = limits
        self.key_func = key_func
        self._scope = scope
        self.per_method = per_method

    def get_limits(self, request):
        if callable(self._limits):
            return list(parse_many(self._limits(request)))
        return self._limits

    def get_scope(self, request):
        if callable(self._scope):
            return self._scope(resolve(request.path).url_name)
        if self._scope:
            return self._scope
        return resolve(request.path).url_name


class BlackHoleHandler(logging.StreamHandler):

    def emit(*_):
        pass