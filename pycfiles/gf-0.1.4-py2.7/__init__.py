# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/gf/__init__.py
# Compiled at: 2013-08-22 11:54:06
"""This is the generic function package."""
from base import generic, method, variadic_method
from go import *
__all__ = go.__all__[:]
__all__.extend(('generic', 'method', 'variadic_method'))