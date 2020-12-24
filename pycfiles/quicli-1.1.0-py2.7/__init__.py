# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/quicli/__init__.py
# Compiled at: 2011-09-04 02:33:14
"""
    quicli: write command line interfaces quickly
    
    A wrapper around Python's argparse module.  Provides argparse
    functionality in a simpler, easier-to-use interface, driven by function
    metadata and decorators, with data validation.
    
    For usage, visit http://dev.kylealanhale.com/wiki/projects/quicli
"""
from .guts import *
from .decorators import *
__all__ = ('run', 'main', 'sub', 'argument', 'FileType', 'RestartProgram')
__version__ = '1.1.0'