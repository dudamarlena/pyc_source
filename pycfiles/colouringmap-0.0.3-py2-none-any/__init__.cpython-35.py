# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: S:\Documents\Code\colourettu\build\lib\colourettu\__init__.py
# Compiled at: 2016-11-27 16:53:35
# Size of source mod 2**32: 1460 bytes
__doc__ = "\nColourettu is a collection of colour related functions.\n\nColourettu is a small collection of colour functions in Python. These can be\nused to determine the (relative) luminosity of a colour and the contrast\nbetween two colours. There is also the palette class for dealing with a 'list'\nof colours.\n"
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