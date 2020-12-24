# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/__init__.py
# Compiled at: 2019-04-14 06:02:48
__version__ = '0.3.4'
import sys
if sys.version_info[:2] < (2, 4):
    raise RuntimeError('PySMI requires Python 2.4 or later')