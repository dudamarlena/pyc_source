# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/log_stdout.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 329 bytes
from __future__ import print_function
import sys

class Logger(object):

    def __init__(self):
        self.terminal = sys.stdout
        self.log = open('log_stdout.dat', 'w')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)