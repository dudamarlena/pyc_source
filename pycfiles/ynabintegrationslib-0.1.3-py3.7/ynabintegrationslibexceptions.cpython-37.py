# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/ynabintegrationslib/ynabintegrationslib/ynabintegrationslibexceptions.py
# Compiled at: 2019-09-15 05:31:29
# Size of source mod 2**32: 1964 bytes
"""
Custom exception code for ynabintegrationslib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '26-06-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'

class InvalidBudget(Exception):
    __doc__ = 'The budget does not exist on YNAB.'


class InvalidAccount(Exception):
    __doc__ = 'The account does not exist on YNAB.'


class MultipleBudgets(Exception):
    __doc__ = 'There are multiple budgets on YNAB.'