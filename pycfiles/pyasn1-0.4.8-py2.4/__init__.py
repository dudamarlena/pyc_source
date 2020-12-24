# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1/__init__.py
# Compiled at: 2019-10-17 01:00:19
import sys
__version__ = '0.4.8'
if sys.version_info[:2] < (2, 4):
    raise RuntimeError('PyASN1 requires Python 2.4 or later')