# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyTujian/print2.py
# Compiled at: 2020-04-26 11:38:03
# Size of source mod 2**32: 1224 bytes
from sys import stdout
import platform, ctypes

def ifWindows():
    if platform.system() == 'Windows':
        return True
    return False


def error(message):
    if ifWindows():
        print(message)
    else:
        print('\x1b[31m%s\x1b[0m' % message)


def success(message):
    if ifWindows():
        print(message)
    else:
        print('\x1b[32m%s\x1b[0m' % message)


def waring(message):
    if ifWindows():
        print(message)
    else:
        print('\x1b[33m%s\x1b[0m' % message)


class print2:

    @staticmethod
    def message(message):
        stdout.write(message)
        stdout.flush()

    @staticmethod
    def success(message):
        if ifWindows():
            stdout.write(message)
        else:
            stdout.write('\x1b[32m%s\x1b[0m' % message)
        stdout.flush()

    @staticmethod
    def error(message):
        if ifWindows():
            stdout.write(message)
        else:
            stdout.write('\x1b[31m%s\x1b[0m' % message)
        stdout.flush()

    @staticmethod
    def waring(message):
        if ifWindows():
            stdout.write(message)
        else:
            stdout.write('\x1b[33m%s\x1b[0m' % message)
        stdout.flush()