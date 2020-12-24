# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/authbone/authorization.py
# Compiled at: 2016-06-21 07:39:12
from flask import g
from functools import wraps

class Authorizator(object):

    def __init__(self, check_capability_func=None, authenticator=None):
        if check_capability_func:
            self.check_capability = check_capability_func
        self.authenticator = authenticator

    def check_capability(self, identity, capability):
        return NotImplemented()

    def identity_getter(self):
        return g.auth_identity

    def _perform_authorization(self, capability):
        if not self.check_capability(self.identity_getter(), capability):
            raise CapabilityMissingException(capability)
        return True

    def __getattr__(self, name):
        if name == 'perform_authorization':
            func = self._perform_authorization
            if self.authenticator:
                func = self.authenticator.requires_authentication(func)
            return func
        raise AttributeError

    def requires_capability(self, capability):

        def decorator(f):

            @wraps(f)
            def decorated(*args, **kwargs):
                self.perform_authorization(capability)
                return f(*args, **kwargs)

            return decorated

        return decorator


class CapabilityMissingException(Exception):

    def __init__(self, capability):
        Exception.__init__(self, capability)