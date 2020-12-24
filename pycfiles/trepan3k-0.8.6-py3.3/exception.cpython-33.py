# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/exception.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1397 bytes
__package__ = 'trepan.exception'

class DebuggerQuit(Exception):
    __doc__ = 'An exception to signal a graceful termination of the program'


class DebuggerRestart(Exception):
    __doc__ = 'An exception to signal a (soft) program restart.\n    You can pass in an array containing the arguments to restart, should\n    we have to issue an execv-style restart.\n    '

    def __init__(self, sys_argv=[]):
        self.sys_argv = sys_argv


if __name__ == '__main__':
    try:
        raise DebuggerRestart(['a', 'b'])
    except DebuggerRestart:
        import sys
        print(sys.exc_info()[1].sys_argv)