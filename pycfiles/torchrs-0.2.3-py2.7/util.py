# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/torchrs/util.py
# Compiled at: 2014-09-17 22:46:46
__author__ = 'Binh Vu <binh@toan2.com>'
from .logger.logger import Logger

def getlogger(ns):
    return Logger(ns, level=Logger.DEBUG)