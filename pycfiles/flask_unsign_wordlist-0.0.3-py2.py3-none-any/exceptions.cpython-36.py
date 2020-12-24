# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Paradoxis/Documents/Projects/flask-unsign-wordlist/flask_unsign_wordlist/exceptions.py
# Compiled at: 2019-01-16 12:38:07
# Size of source mod 2**32: 178 bytes


class FlaskUnsignWordlistException(Exception):
    __doc__ = 'Base exception class'


class NoSuchWordlist(FlaskUnsignWordlistException):
    __doc__ = 'Raised when no such wordlist exists'