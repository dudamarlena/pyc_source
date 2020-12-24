# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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