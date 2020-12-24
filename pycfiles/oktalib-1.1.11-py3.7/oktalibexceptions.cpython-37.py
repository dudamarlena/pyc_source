# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ghawker/code/python/oktalib/oktalib/oktalibexceptions.py
# Compiled at: 2020-01-13 05:24:47
# Size of source mod 2**32: 2136 bytes
"""
Custom exception code for oktalib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-01-08'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'

class AuthFailed(Exception):
    __doc__ = 'The authentication was not possible. Invalid token maybe.'


class InvalidGroup(Exception):
    __doc__ = 'The group provided is invalid.'


class InvalidUser(Exception):
    __doc__ = 'The user provided is invalid.'


class InvalidApplication(Exception):
    __doc__ = 'The application provided is invalid.'


class ApiLimitReached(Exception):
    __doc__ = 'The api limits are close to being reached.'