# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/log.py
# Compiled at: 2018-11-17 10:28:34
# Size of source mod 2**32: 571 bytes
from sys import stderr
from datetime import datetime

def time() -> str:
    return datetime.now().strftime('%H:%M:%S')


def info(modulename: str, text: str):
    print('[%s] \x1b[96m%s: \x1b[0m%s' % (time(), modulename, text))


def warning(modulename: str, text: str):
    print('[%s] \x1b[93m%s: \x1b[0m%s' % (time(), modulename, text))


def success(modulename: str, text: str):
    print('[%s] \x1b[92m%s: \x1b[0m%s' % (time(), modulename, text))


def error(modulename: str, text: str):
    print(('[%s] \x1b[91m%s: \x1b[0m%s' % (time(), modulename, text)), file=stderr)