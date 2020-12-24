# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sigma/core/util.py
# Compiled at: 2016-01-23 17:25:07
# Size of source mod 2**32: 175 bytes
"""
"""

def validate(Model, *args, **kwargs):
    return Model(*args, **kwargs)


def asdict(model):
    return dict((key, getattr(model, key)) for key in model.__fields__)