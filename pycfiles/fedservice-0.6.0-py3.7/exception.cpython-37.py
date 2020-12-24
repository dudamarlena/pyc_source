# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/exception.py
# Compiled at: 2020-01-25 11:27:56
# Size of source mod 2**32: 292 bytes


class FedServiceError(Exception):
    pass


class NoSuitableFederation(FedServiceError):
    pass


class NoTrustedClaims(FedServiceError):
    pass


class DbFault(FedServiceError):
    pass


class WrongSubject(FedServiceError):
    pass


class ConstraintError(FedServiceError):
    pass