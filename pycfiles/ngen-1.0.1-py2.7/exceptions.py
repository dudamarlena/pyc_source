# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ngen/exceptions.py
# Compiled at: 2017-10-08 17:55:08
from __future__ import unicode_literals, absolute_import, print_function

class Error(Exception):
    """General error class for inheritance purposes"""
    pass


class ParserError(Error):
    pass


class FieldError(ParserError, TypeError):
    pass


class ValidationError(Error):
    pass


class ImproperlyConfigured(Error):
    pass