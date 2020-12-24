# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/jws/exceptions.py
# Compiled at: 2015-03-10 10:15:45


class MissingKey(Exception):
    pass


class MissingSigner(Exception):
    pass


class MissingVerifier(Exception):
    pass


class SignatureError(Exception):
    pass


class RouteMissingError(Exception):
    pass


class RouteEndpointError(Exception):
    pass


class AlgorithmNotImplemented(Exception):
    pass


class ParameterNotImplemented(Exception):
    pass


class ParameterNotUnderstood(Exception):
    pass