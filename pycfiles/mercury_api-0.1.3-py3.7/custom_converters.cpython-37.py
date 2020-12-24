# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_api/custom_converters.py
# Compiled at: 2018-09-27 14:18:55
# Size of source mod 2**32: 501 bytes
"""
This module defines all the flask custom converters for mercury api.
"""
from werkzeug.routing import BaseConverter, ValidationError

class BlackListConverter(BaseConverter):
    __doc__ = '\n    Converter to validate the value is not part of a specified blacklist\n    '

    def __init__(self, map, *blacklist):
        super().__init__(map)
        self.blacklist = blacklist

    def to_python(self, value):
        if value in self.blacklist:
            raise ValidationError()
        return value