# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/csFIFO/__init__.py
# Compiled at: 2013-02-06 12:51:03
__all__ = [
 'csFIFO', 'version']
from csFIFO import *
try:
    from version import __version__
except ImportError:
    __version__ = 'Unknown'