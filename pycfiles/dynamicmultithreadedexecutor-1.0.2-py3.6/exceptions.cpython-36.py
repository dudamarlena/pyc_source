# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/dynamicmultithreadedexecutor/exceptions.py
# Compiled at: 2017-12-22 10:31:10
# Size of source mod 2**32: 221 bytes


class KillExecution(Exception):
    __doc__ = '\n    This is caught in our worker funciton to kill the rest of all our worker functions\n    the rest of our workers will gracefully exit along with all other threads\n    '