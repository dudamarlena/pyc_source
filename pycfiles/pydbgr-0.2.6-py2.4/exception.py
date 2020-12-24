# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/exception.py
# Compiled at: 2013-03-08 17:51:53


class DebuggerQuit(Exception):
    """Exception to signal graceful debugger termination"""
    __module__ = __name__


class DebuggerRestart(Exception):
    """Exception to signal a (soft) program restart.
    You can pass in an array containing the arguments to restart, should
    we have to issue an execv-style restart.
    """
    __module__ = __name__

    def __init__(self, sys_argv=[]):
        self.sys_argv = sys_argv


if __name__ == '__main__':
    try:
        raise DebuggerRestart(['a', 'b'])
    except DebuggerRestart:
        import sys
        print sys.exc_value.sys_argv