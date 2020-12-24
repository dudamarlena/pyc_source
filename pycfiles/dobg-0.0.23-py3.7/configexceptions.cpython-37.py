# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dobg/exceptions/configexceptions.py
# Compiled at: 2019-07-20 11:35:31
# Size of source mod 2**32: 492 bytes


class TokenException(Exception):
    __doc__ = ' '


class InvalidTokenException(TokenException):

    def __str__(self):
        return "Your Digital Ocean authentication token is invalid.                    \nPlease, set valid token with 'settoken' command."


class MissingTokenException(TokenException):

    def __str__(self):
        return "It seems like you haven't set up your Digital Ocean authentication token.                     \nPlease, set your token using 'settoken' command."