# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\srllib\error.py
# Compiled at: 2012-05-11 12:09:02
""" Exception classes. """

class SrlError(Exception):
    """ Base SRL exception. """
    pass


class BusyError(SrlError):
    """ General indication that an object is busy with an operation. """
    pass


class NotFound(SrlError):
    """ General indication that a resource was not found. """
    pass


class Canceled(SrlError):
    """ The operation was canceled. """
    pass