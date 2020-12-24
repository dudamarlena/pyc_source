# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tomchristie/GitHub/api-star/api_star/environment.py
# Compiled at: 2016-04-18 15:25:28
# Size of source mod 2**32: 308 bytes
import os

class Environment(object):
    environ = os.environ

    def __init__(self, **kwargs):
        for key, config in kwargs.items():
            validator, default = config
            value = self.environ.get(key, default)
            value = validator(value)
            setattr(self, key, value)