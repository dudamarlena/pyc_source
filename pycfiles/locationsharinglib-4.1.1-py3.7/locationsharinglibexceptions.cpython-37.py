# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/Personal_to_cleanup/python/locationsharinglib/locationsharinglib/locationsharinglibexceptions.py
# Compiled at: 2020-04-07 02:47:26
# Size of source mod 2**32: 1927 bytes
"""
Custom exception code for locationsharinglib.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '2017-12-24'
__copyright__ = 'Copyright 2017, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos', 'Chris Helming']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'

class InvalidCookies(Exception):
    __doc__ = 'The cookies provided do not provide a valid session.'


class InvalidData(Exception):
    __doc__ = 'The data received do not fit the expected format.'