# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/log.py
# Compiled at: 2010-09-03 02:22:19
from twisted.python.log import *
from logging import DEBUG, INFO, WARN, ERROR
TRACE = 0

def debug(*args, **kw):
    kw.setdefault('logLevel', DEBUG)
    msg(*args, **kw)


def warn(*args, **kw):
    kw.setdefault('logLevel', WARN)
    msg(*args, **kw)


__id__ = '$Id: $'[5:-2]