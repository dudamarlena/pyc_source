# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/terraformtestinglib/terraformtestinglib/terraformtestinglibexceptions.py
# Compiled at: 2019-10-22 09:03:12
# Size of source mod 2**32: 1982 bytes
"""
Custom exception code for terraformtestinglib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-05-24'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'

class InvalidNaming(Exception):
    __doc__ = 'The rules file provided was invalid.'


class InvalidPositioning(Exception):
    __doc__ = 'The structure file provided was invalid.'


class MissingVariable(Exception):
    __doc__ = 'The variable is missing.'