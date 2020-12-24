# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_client/cmd.py
# Compiled at: 2020-02-24 06:32:10
# Size of source mod 2**32: 412 bytes
"""
client for EKCA service -- SSH shell commands
"""
import os.path, shlex
from collections import UserList
__all__ = [
 'ShellCommand',
 'SSH_ADD_PWPROMPT',
 'SSH_ADD_WAIT']
SSH_ADD_WAIT = 0.4

class ShellCommand(UserList):
    __doc__ = '\n    wrapper class for list of shell-quoted command-line arguments\n    '

    def __str__(self):
        return ' '.join((shlex.quote(arg) for arg in self))