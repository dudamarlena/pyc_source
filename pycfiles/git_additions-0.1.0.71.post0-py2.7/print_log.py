# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/git_additions/logs/print_log.py
# Compiled at: 2018-12-30 09:36:41
from __future__ import print_function
from git_additions.logs.t_colors import TColors

class PrintLog(object):

    def __init__(self, lines):
        self.lines = lines

    def run(self):
        for line in self.lines:
            colors = TColors.COLORS
            colors.update({'line': line})
            log_line = '{default}{line[0]} {green}{line[3]} {white}{line[1]}{yellow} [{line[2]}]  {darkgray}{line[4]}{default}'
            print(log_line.format(**colors))