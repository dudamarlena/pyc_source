# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/logic/impls/advs.py
# Compiled at: 2019-12-27 10:07:46
# Size of source mod 2**32: 1182 bytes
from typing import Generic, Callable, TypeVar
from exactly_lib.type_system.logic.logic_base_class import ApplicationEnvironmentDependentValue
from exactly_lib.type_system.logic.matcher_base_class import MatcherAdv, MODEL, ApplicationEnvironment, MatcherWTraceAndNegation
T = TypeVar('T')

class ConstantAdv(Generic[T], ApplicationEnvironmentDependentValue[T]):

    def __init__(self, constant: T):
        self._constant = constant

    def applier(self, environment: ApplicationEnvironment) -> T:
        return self._constant


class ConstantMatcherAdv(Generic[MODEL], MatcherAdv[MODEL]):

    def __init__(self, constant: MatcherWTraceAndNegation[MODEL]):
        self._constant = constant

    def applier(self, environment: ApplicationEnvironment) -> MatcherWTraceAndNegation[MODEL]:
        return self._constant


class MatcherAdvFromFunction(Generic[MODEL], MatcherAdv[MODEL]):

    def __init__(self, constructor: Callable[([ApplicationEnvironment], MatcherWTraceAndNegation[MODEL])]):
        self._constructor = constructor

    def applier(self, environment: ApplicationEnvironment) -> MatcherWTraceAndNegation[MODEL]:
        return self._constructor(environment)