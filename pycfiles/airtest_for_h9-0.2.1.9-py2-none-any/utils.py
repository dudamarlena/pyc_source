# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\administrator\pycharmprojects\airtest_for_h9\airtest\webgui\routers\utils.py
# Compiled at: 2014-12-03 20:37:50
import os

def selfdir():
    cwd = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(cwd)


def workdir():
    return os.getenv('WORKDIR')


TMPDIR = os.path.join(selfdir(), 'tmp')