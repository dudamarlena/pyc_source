# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kali/Development/Projects/shellen/shellen/syscalls/linux_handler.py
# Compiled at: 2018-01-19 17:37:15
# Size of source mod 2**32: 281 bytes
import os
from os.path import join
from syscalls.base_handler import SysHandler

class LinuxSysHandler(SysHandler):

    def __init__(self):
        super().__init__()
        self.dir = join(os.path.dirname(os.path.realpath(__file__)), 'linux_tables')
        self.load_tables()