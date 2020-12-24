# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/exceptions.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 300 bytes
"""
amcrest.exceptions

This module contains the set of amcrest's exceptions.
"""

class AmcrestError(Exception):
    __doc__ = 'General Amcrest error occurred.'


class CommError(AmcrestError):
    __doc__ = 'A communication error occurred.'


class LoginError(AmcrestError):
    __doc__ = 'A login error occurred.'