# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: distributions/__init__.py
# Compiled at: 2017-10-28 18:53:45
__version__ = '2.2.0'
import os
try:
    import distributions.has_cython
    has_cython = distributions.has_cython.has_cython()
except ImportError:
    has_cython = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))