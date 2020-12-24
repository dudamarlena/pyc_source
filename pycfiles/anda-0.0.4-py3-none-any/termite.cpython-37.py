# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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