# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/flask_limiter/wrappers.py
# Compiled at: 2020-02-25 18:13:15
# Size of source mod 2**32: 2135 bytes
from flask import request
from limits import parse_many

class Limit(object):
    __doc__ = '\n    simple wrapper to encapsulate limits and their context\n    '

    def __init__(self, limit, key_func, scope, per_method, methods, error_message, exempt_when, override_defaults):
        self.limit = limit
        self.key_func = key_func
        self._Limit__scope = scope
        self.per_method = per_method
        self.methods = methods
        self.error_message = error_message
        self.exempt_when = exempt_when
        self.override_defaults = override_defaults

    @property
    def is_exempt(self):
        """Check if the limit is exempt."""
        return self.exempt_when and self.exempt_when()

    @property
    def scope(self):
        if callable(self._Limit__scope):
            return self._Limit__scope(request.endpoint)
        return self._Limit__scope

    @property
    def method_exempt(self):
        """Check if the limit is not applicable for this method"""
        return self.methods is not None and request.method.lower() not in self.methods


class LimitGroup(object):
    __doc__ = '\n    represents a group of related limits either from a string or a callable that returns one\n    '

    def __init__(self, limit_provider, key_function, scope, per_method, methods, error_message, exempt_when, override_defaults):
        self._LimitGroup__limit_provider = limit_provider
        self._LimitGroup__scope = scope
        self.key_function = key_function
        self.per_method = per_method
        self.methods = methods and [m.lower() for m in methods] or methods
        self.error_message = error_message
        self.exempt_when = exempt_when
        self.override_defaults = override_defaults

    def __iter__(self):
        limit_items = parse_many(self._LimitGroup__limit_provider() if callable(self._LimitGroup__limit_provider) else self._LimitGroup__limit_provider)
        for limit in limit_items:
            (yield Limit(limit, self.key_function, self._LimitGroup__scope, self.per_method, self.methods, self.error_message, self.exempt_when, self.override_defaults))