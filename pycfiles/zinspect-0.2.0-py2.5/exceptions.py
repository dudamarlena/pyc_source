# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\zinspect\exceptions.py
# Compiled at: 2007-06-26 10:34:46
"""
Theses are the exceptions that can be raised by this module
"""

class InterfaceError(Exception):
    pass


class MissingAttribute(InterfaceError):
    pass


class MissingMethod(InterfaceError):
    pass


class DoesNotProvide(InterfaceError):
    pass


class DoesNotImplement(InterfaceError):
    pass