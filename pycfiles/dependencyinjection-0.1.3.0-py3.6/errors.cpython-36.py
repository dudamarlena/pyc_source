# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\errors.py
# Compiled at: 2017-12-18 02:35:53
# Size of source mod 2**32: 435 bytes
import typing

class InvalidError(Exception):
    pass


class CycleDependencyError(Exception):

    def __init__(self, chain: typing.List[type]):
        self._chain = chain


class TypeNotFoundError(Exception):
    pass


class ParameterTypeResolveError(Exception):
    pass