# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/csFIFO/__init__.py
# Compiled at: 2013-02-06 12:51:03
__all__ = [
 'csFIFO', 'version']
from csFIFO import *
try:
    from version import __version__
except ImportError:
    __version__ = 'Unknown'