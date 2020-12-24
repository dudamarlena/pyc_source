# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hubspot/connection/_validators.py
# Compiled at: 2016-08-16 04:41:21
from functools import wraps
from voluptuous import Invalid

def Constant(expected_value):

    @wraps(Constant)
    def _validate(value):
        if value != expected_value:
            raise Invalid(('expected {!r}').format(expected_value))
        return value

    return _validate