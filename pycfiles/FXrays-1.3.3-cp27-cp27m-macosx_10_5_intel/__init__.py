# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.macosx-10.5-intel-2.7/FXrays/__init__.py
# Compiled at: 2017-01-18 15:05:06
"""
This package is a small, fast implementation of an algorithm for
finding extremal rays of a polyhedral cone, with filtering.  It is
intended for finding normal surfaces in triangulated 3-manifolds, and
therefore does not implement various features that might be useful for
general extremal ray problems.
"""
from .FXraysmodule import find_Xrays
__version__ = '1.3.3'

def version():
    return __version__