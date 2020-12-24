# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/exception.py
# Compiled at: 2014-10-21 04:10:11
__package__ = 'trepan.exception'

class DebuggerQuit(Exception):
    """An exception to signal a graceful termination of the program"""
    pass


class DebuggerRestart(Exception):
    """An exception to signal a (soft) program restart.
    You can pass in an array containing the arguments to restart, should
    we have to issue an execv-style restart.
    """

    def __init__(self, sys_argv=[]):
        self.sys_argv = sys_argv


if __name__ == '__main__':
    try:
        raise DebuggerRestart(['a', 'b'])
    except DebuggerRestart:
        import sys
        print sys.exc_value.sys_argv