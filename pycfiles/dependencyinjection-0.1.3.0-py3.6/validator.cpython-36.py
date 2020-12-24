# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\validator.py
# Compiled at: 2017-12-18 01:53:00
# Size of source mod 2**32: 411 bytes
from .common import IValidator
from .errors import InvalidError

class Validator(IValidator):

    def verify(self, service_type: type, obj):
        if not isinstance(obj, service_type):
            raise InvalidError('{} is not a {}'.format(obj, service_type))