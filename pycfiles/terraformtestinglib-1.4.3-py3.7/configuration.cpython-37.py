# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/SBP/python/terraformtestinglib/terraformtestinglib/configuration.py
# Compiled at: 2019-10-22 08:58:52
# Size of source mod 2**32: 2300 bytes
"""
Main code for configuration.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import re
from schema import Schema, Optional, And
__author__ = 'Costas Tyfoxylos <ctyfoxylos@schubergphilis.com>'
__docformat__ = 'google'
__date__ = '2018-05-24'
__copyright__ = 'Copyright 2018, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<ctyfoxylos@schubergphilis.com>'
__status__ = 'Development'

def is_valid_regex(value):
    """Validates a regex."""
    try:
        re.compile(value)
        is_valid = True
    except re.error:
        is_valid = False

    return is_valid


NAMING_SCHEMA = Schema([
 {'resource': str, 
  'regex': is_valid_regex, 
  Optional('fields'): [
                       {'value':str,  'regex':is_valid_regex}]}])
POSITIONING_SCHEMA = Schema({And(str, lambda x: x.endswith('.tf')): [str]})
DISASTER_RECOVERY_FILENAME = 'disaster_recovery.tf'