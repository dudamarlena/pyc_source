# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/common/shell.py
# Compiled at: 2013-12-13 03:37:44
# Size of source mod 2**32: 357 bytes
"""
StackMan
Colton J. Provias - cj@coltonprovias.com
"""
from stackman.stack import StackItem

class ShellCommand(StackItem):
    __doc__ = '\n    The most configurable and most malicious of these\n\n    Arguments:\n    * command str Command\n                  Default: turret\n    * ready_text str Ready Text\n                     Default: I see you.\n    '