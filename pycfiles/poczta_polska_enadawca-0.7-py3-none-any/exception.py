# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/core/exception.py
# Compiled at: 2018-11-28 03:20:09
__doc__ = "\nCopyright (c) 2014-2016 pocsuite developers (https://seebug.org)\nSee the file 'docs/COPYING' for copying permission\n"

class PocsuiteBaseException(Exception):
    pass


class PocsuiteUserQuitException(PocsuiteBaseException):
    pass


class PocsuiteDataException(PocsuiteBaseException):
    pass


class PocsuiteGenericException(PocsuiteBaseException):
    pass


class PocsuiteSystemException(PocsuiteBaseException):
    pass


class PocsuiteFilePathException(PocsuiteBaseException):
    pass


class PocsuiteConnectionException(PocsuiteBaseException):
    pass


class PocsuiteThreadException(PocsuiteBaseException):
    pass


class PocsuiteValueException(PocsuiteBaseException):
    pass


class PocsuiteMissingPrivileges(PocsuiteBaseException):
    pass


class PocsuiteSyntaxException(PocsuiteBaseException):
    pass