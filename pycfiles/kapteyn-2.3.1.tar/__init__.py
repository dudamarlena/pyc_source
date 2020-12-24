# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./kapteyn/__init__.py
# Compiled at: 2016-10-31 08:28:14
"""Kapteyn package.

"""
from os import path
package_dir = path.abspath(path.dirname(__file__))
__all__ = [
 'celestial', 'wcs', 'wcsgrat', 'tabarray', 'maputils',
 'mplutil', 'positions', 'shapes', 'rulers', 'filters',
 'interpolation', 'kmpfit']
__version__ = '2.3.1'