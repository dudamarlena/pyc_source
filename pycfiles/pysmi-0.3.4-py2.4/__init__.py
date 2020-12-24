# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/__init__.py
# Compiled at: 2019-04-14 06:02:48
__version__ = '0.3.4'
import sys
if sys.version_info[:2] < (2, 4):
    raise RuntimeError('PySMI requires Python 2.4 or later')