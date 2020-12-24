# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/ynablib/ynablib/ynablibexceptions.py
# Compiled at: 2019-07-28 10:35:14
# Size of source mod 2**32: 1936 bytes
"""
Custom exception code for ynablib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '26-07-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'

class AuthenticationFailed(Exception):
    __doc__ = 'The authentication failed.'


class InvalidBudget(Exception):
    __doc__ = 'The budget does not exist on YNAB.'


class InvalidAccount(Exception):
    __doc__ = 'The account does not exist on YNAB.'