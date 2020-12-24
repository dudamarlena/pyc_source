# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ctyfoxylos/personal/python/abnamrolib/abnamrolib/abnamrolibexceptions.py
# Compiled at: 2019-12-10 08:01:54
# Size of source mod 2**32: 2014 bytes
__doc__ = '\nCustom exception code for abnamrolib.\n\n.. _Google Python Style Guide:\n   http://google.github.io/styleguide/pyguide.html\n\n'
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
    """AuthenticationFailed"""
    pass


class InvalidCookies(Exception):
    """InvalidCookies"""
    pass


class InvalidDateFormat(Exception):
    """InvalidDateFormat"""
    pass