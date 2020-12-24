# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modules/bcolors.py
# Compiled at: 2018-07-01 06:51:02
# Size of source mod 2**32: 400 bytes


class Bcolors:

    def __init__(self):
        self.HEADER = '\x1b[95m'
        self.OKBLUE = '\x1b[94m'
        self.OKGREEN = '\x1b[92m'
        self.WARNING = '\x1b[93m'
        self.FAIL = '\x1b[91m'
        self.ENDC = '\x1b[0m'
        self.BOLD = '\x1b[1m'
        self.UNDERLINE = '\x1b[4m'
        self.WHITE = '\x1b[97m'
        self.On_Black = '\x1b[40m'
        self.On_Red = '\x1b[41m'