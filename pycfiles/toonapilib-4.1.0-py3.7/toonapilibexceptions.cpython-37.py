# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/toonapilib/toonapilib/toonapilibexceptions.py
# Compiled at: 2019-11-30 07:55:30
# Size of source mod 2**32: 2337 bytes
"""
Custom exception code for toonapilib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '2017-12-09'
__copyright__ = 'Copyright 2017, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'

class InvalidAuthenticationToken(Exception):
    __doc__ = 'The authentication token provided was not accepted as valid.'


class InvalidDisplayName(Exception):
    __doc__ = 'The display name provided was not accepted as valid.'


class InvalidThermostatState(Exception):
    __doc__ = 'The state provided to the thermostat is not a valid one.'


class InvalidProgramState(Exception):
    __doc__ = 'The state provided to the program is not a valid one.'


class IncompleteStatus(Exception):
    __doc__ = 'The status received is missing vital information and is unusable.'


class AgreementsRetrievalError(Exception):
    __doc__ = 'Could not retrieve agreements.'