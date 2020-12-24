# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/abnamrolib/abnamrolib/abnamrolibexceptions.py
# Compiled at: 2019-12-10 08:01:54
# Size of source mod 2**32: 2014 bytes
"""
Custom exception code for abnamrolib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '19-07-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'

class AuthenticationFailed(Exception):
    __doc__ = 'The token provided is invalid or the authentication failed for some other reason.'


class InvalidCookies(Exception):
    __doc__ = 'The cookies provided are invalid.'


class InvalidDateFormat(Exception):
    __doc__ = 'The date provided cannot be automatically parsed.'