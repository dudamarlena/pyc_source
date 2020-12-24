# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_service/cmd.py
# Compiled at: 2019-09-19 14:44:28
# Size of source mod 2**32: 421 bytes
"""
basic helper stuff for safely handling shell commands
"""
import shlex
from collections import UserList

class ShellCommand(UserList):
    __doc__ = '\n    wrapper class for list of shell-quoted command-line arguments\n    '

    def __init__(self, cmd_exec, args):
        UserList.__init__(self, [cmd_exec] + args)

    def __str__(self):
        return ' '.join((shlex.quote(arg) for arg in self))