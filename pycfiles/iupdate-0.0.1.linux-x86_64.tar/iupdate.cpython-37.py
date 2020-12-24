# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/iupdate/iupdate.py
# Compiled at: 2019-10-15 12:29:25
# Size of source mod 2**32: 366 bytes
from lib.ansi_code import AnsiCode
from subprocess import run, PIPE, STDOUT

class IUpdate:

    def __init__(self):
        self.name_prog = 'iUpdate'

    @staticmethod
    def system():
        print('[Run iUpdate]')
        print('Warning! Sorry, this package is under construction')