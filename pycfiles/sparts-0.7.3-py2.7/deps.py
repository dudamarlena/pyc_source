# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/deps.py
# Compiled at: 2015-01-08 02:58:40
from __future__ import absolute_import
import imp

def HAS(module):
    try:
        return __import__(module)
    except ImportError:
        return

    return


HAS_PSUTIL = HAS('psutil')
HAS_THRIFT = HAS('thrift')
HAS_DAEMONIZE = HAS('daemonize')