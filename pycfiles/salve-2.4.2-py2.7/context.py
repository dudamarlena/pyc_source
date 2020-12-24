# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/tests/util/context.py
# Compiled at: 2015-11-06 23:45:35
from salve.context import ExecutionContext

def clear_exec_context():
    """
    Ensure that there is no current ExecutionContext
    """
    try:
        del ExecutionContext._instance
    except AttributeError:
        pass