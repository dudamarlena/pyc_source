# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/mapscookiegettercli/mapscookiegettercli/__init__.py
# Compiled at: 2019-06-16 09:01:32
# Size of source mod 2**32: 1892 bytes
"""
mapscookiegettercli package

Import all parts from mapscookiegettercli here

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from ._version import __version__
from library.cookiegetter import CookieGetter
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '04-03-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
assert __version__
assert CookieGetter