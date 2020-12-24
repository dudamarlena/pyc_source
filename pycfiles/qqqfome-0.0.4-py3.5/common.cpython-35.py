# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qqqfome/common.py
# Compiled at: 2016-02-10 10:46:17
# Size of source mod 2**32: 235 bytes
from . import strings as s

def check_type(var, name, t):
    if not isinstance(t, type(str)):
        t = type(t)
    if not isinstance(var, t):
        raise ValueError(s.type_error.format(name, str(t), str(type(var))))