# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/webstarts/defaults.py
# Compiled at: 2017-08-10 13:06:00
# Size of source mod 2**32: 506 bytes
"""Applicable to webstarts"""
from inspect import currentframe
__author__ = 'john'
LOG_KEY = 'logid'
TRACE_KEY = 'x-cloud-trace-context'
FORMAT = '%(levelname)s %(logid)s %(name)s "%(message)s" %(extras)s'
FORMAT_DEBUG = '%(levelname)-8s %(logid)-12s %(name)-30s "%(message)-100s"'
CACHE_KEY = lambda *a, **kws: id(currentframe().f_back.f_back.f_locals.get('wrapped'))