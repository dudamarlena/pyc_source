# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\nekos\errors.py
# Compiled at: 2018-05-15 14:35:13
# Size of source mod 2**32: 385 bytes


class NekoException(Exception):
    __doc__ = ' Base exception class for nekos.py '


class NothingFound(NekoException):
    __doc__ = " The API didn't return anything "


class EmptyArgument(NekoException):
    __doc__ = ' When no target is defined '


class InvalidArgument(NekoException):
    __doc__ = ' Invalid argument within the category '