# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/realasking/python_project1_environment_pathways_OR_essential_paths/epw/displayops.py
# Compiled at: 2017-08-23 22:17:01
# Size of source mod 2**32: 1405 bytes
import sys, os, re, shutil

class screenformat:
    max_tty_rows = 0
    max_tty_line_width = 0
    fullptlength = 0
    namelengthmax = 0
    waylengthmax = 0

    def __init__(self):
        arows, awidth = os.popen('stty size', 'r').read().split()
        self.max_tty_rows = int(arows)
        self.max_tty_line_width = int(awidth)

    def size_calc(self, fileds):
        self.fullptlength = self.max_tty_line_width - 3 * int(fileds) - 1
        self.namelengthmax = int(0.3 * self.fullptlength)
        self.waylengthmax = int((self.fullptlength - self.namelengthmax) / (int(fileds) - 1.0))

    def string_formatting(self, data, filed_max_width):
        all_length = 0
        fdata = ''
        for cha in data:
            if all_length + 2 < filed_max_width:
                fdata = fdata + cha
                all_length = all_length + 1
            else:
                all_length = 1
                fdata = fdata + '\n' + cha

        return fdata