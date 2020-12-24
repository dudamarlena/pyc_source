# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jiangyongkang/anaconda3/lib/python3.7/site-packages/jyk/logging/__init__.py
# Compiled at: 2020-04-01 00:46:22
# Size of source mod 2**32: 153 bytes
"""jyk file package"""
from .core import initConsoleLogging, initLogging, LogRootPath, FormatterMode
from .test import makeLogs
__version__ = '1.0.1'