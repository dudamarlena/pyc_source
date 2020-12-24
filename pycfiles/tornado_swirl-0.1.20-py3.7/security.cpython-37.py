# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tornado_swirl/openapi/security.py
# Compiled at: 2019-12-17 19:31:58
# Size of source mod 2**32: 1165 bytes
"""
Contains classes for security types.
"""

class SecurityScheme(object):
    __doc__ = 'Represents security scheme'


class APIKey(SecurityScheme):

    def __init__(self, name, location='header'):
        self.name = name
        self.location = location if location in ('query', 'header', 'cookie') else 'header'

    @property
    def type(self):
        return 'apiKey'

    def spec(self):
        return {'type':'apiKey', 
         'name':self.name, 
         'in':self.location}


class HTTP(SecurityScheme):
    Schemes = [
     'basic', 'bearer', 'digest', 'hoba', 'mutual', 'negotiate', 'oauth', 'scram-sha-1',
     'scram-sha-256', 'vapid']

    def __init__(self, scheme, bearerFormat=None):
        self.scheme = scheme
        self.bearerFormat = bearerFormat

    @property
    def type(self):
        return 'http'

    def spec(self):
        sp = {'type':'http', 
         'scheme':self.scheme}
        if self.bearerFormat:
            sp['bearerFormat'] = self.bearerFormat
        return sp