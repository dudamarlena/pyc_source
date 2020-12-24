# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/streamio/__init__.py
# Compiled at: 2013-11-21 19:55:34
"""streamio - reading, writing and sorting large files.

streamio is a simple library of functions designed to read, write and sort large files using iterators so that the operations will successfully complete
on systems with limited RAM.

:copyright: CopyRight (C) 2013 by James Mills
"""
__author__ = 'James Mills, j dot mills at griffith dot edu dot au'
__date__ = '21st November 2013'
from .version import version as __version__
from .stat import minmax
from .sort import merge, mergesort
from .stream import stream, csvstream, jsonstream, csvdictstream, compress
__all__ = ('minmax', 'merge', 'mergesort', 'stream', 'csvstream', 'jsonstream', 'csvdictstream',
           'compress')