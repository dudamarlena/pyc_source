# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/jansky/data/users/breddels/src/kapteyn-sky2/kapteyn/__init__.py
# Compiled at: 2016-03-21 08:46:34
# Size of source mod 2**32: 281 bytes
"""Kapteyn package.

"""
from os import path
package_dir = path.abspath(path.dirname(__file__))
__all__ = [
 'celestial', 'wcs', 'wcsgrat', 'tabarray', 'maputils',
 'mplutil', 'positions', 'shapes', 'rulers', 'filters',
 'interpolation', 'kmpfit']
__version__ = '2.3'