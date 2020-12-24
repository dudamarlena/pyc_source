# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dependencyinjection\internal\param_type_resolver.py
# Compiled at: 2018-01-23 09:48:23
# Size of source mod 2**32: 1059 bytes
import typing, inspect
from .errors import ParameterTypeResolveError

class ParameterTypeResolver:
    __doc__ = ' desgin for resolve type from parameter. '

    def __init__(self, name_map: typing.Dict[(str, type)]):
        self._name_map = name_map.copy()

    def resolve(self, parameter: inspect.Parameter, allow_none):
        if parameter.annotation is inspect.Parameter.empty:
            typ = self._name_map.get(parameter.name)
            if typ is None:
                msg = "cannot resolve parameter type from name: '{}'".format(parameter.name)
                raise ParameterTypeResolveError(msg)
            return typ
        else:
            if isinstance(parameter.annotation, type):
                return parameter.annotation
            msg = allow_none or 'cannot parse type from annotation: {}'.format(parameter.annotation)
            raise ParameterTypeResolveError(msg)