# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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