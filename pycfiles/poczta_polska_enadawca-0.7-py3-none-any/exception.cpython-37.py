# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/exception.py
# Compiled at: 2019-09-18 05:04:31
# Size of source mod 2**32: 1138 bytes


class PocsuiteBaseException(Exception):
    pass


class PocsuiteUserQuitException(PocsuiteBaseException):
    pass


class PocsuiteShellQuitException(PocsuiteBaseException):
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


class PocsuiteValidationException(PocsuiteBaseException):
    pass


class PocsuiteMissingMandatoryOptionException(PocsuiteBaseException):
    pass


class PocsuitePluginBaseException(PocsuiteBaseException):
    pass


class PocsuitePluginDorkException(PocsuitePluginBaseException):
    pass


class PocsuiteHeaderTypeException(PocsuiteBaseException):
    pass