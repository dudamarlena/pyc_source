# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ancypwn_terminal_termite/termite.py
# Compiled at: 2019-09-17 11:36:17
# Size of source mod 2**32: 309 bytes
import os

def _escape_command_unix(command):
    return repr(command)[1:-1]


def run(command):
    execute = 'termite -e "{}"'.format(_escape_command_unix(command))
    os.system(execute)


def run_test():
    run("ancypwn attach -c '/usr/bin/gdb /bin/echo'")


if __name__ == '__main__':
    run_test()