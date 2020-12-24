# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyculiarity/__init__.py
# Compiled at: 2018-08-28 00:33:09
"""
    pyculiarity

    A Python port of Twitter's AnomalyDetection R Package.

    :license: GPL, see LICENSE for more details.
"""
__version__ = '0.0.6'
from pyculiarity.detect_vec import detect_vec
from pyculiarity.detect_ts import detect_ts