# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/service/test.py
# Compiled at: 2016-12-14 13:49:55
"""
Test Service
"""
from ..debugging import bacpypes_debugging, ModuleLogger
_debug = 0
_log = ModuleLogger(globals())

@bacpypes_debugging
def some_function(*args):
    if _debug:
        some_function._debug('f %r', args)
    return args[0] + 1