# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/r/prj/p/dosca/env/lib/python3.5/site-packages/dosca/__init__.py
# Compiled at: 2016-12-11 15:37:34
# Size of source mod 2**32: 335 bytes
from __future__ import absolute_import
from .dosca import parse, parse_file, ParseError, save, save_file, dump
from . import ext
__all__ = ('parse', 'parse_file', 'ParseError', 'ext', 'save', 'save_file', 'dump')
__version__ = '2.0.0'
__author__ = 'Roma Sokolov'
__license__ = 'MIT'