# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: S:\Documents\Code\colourettu\build\lib\colourettu\__init__.py
# Compiled at: 2016-11-27 16:53:35
# Size of source mod 2**32: 1460 bytes
"""
Colourettu is a collection of colour related functions.

Colourettu is a small collection of colour functions in Python. These can be
used to determine the (relative) luminosity of a colour and the contrast
between two colours. There is also the palette class for dealing with a 'list'
of colours.
"""
from __future__ import absolute_import
__title__ = 'Colourettu'
__description__ = 'Colourettu is a collection of colour related functions.'
__url__ = 'http://minchin.ca/colourettu/'
__author__ = 'William Minchin'
__email__ = 'w_minchin@hotmail.com'
__license__ = 'MIT License'
__copyright_years__ = '2014-16'
__copyright__ = 'Copyright (c) {} {}'.format(__copyright_years__, __author__)
__version__ = '2.0.0-dev+0'
from ._colour import *
from ._palette import *