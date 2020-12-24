# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/impls/ddv_components.py
# Compiled at: 2020-01-31 11:01:49
# Size of source mod 2**32: 1811 bytes
from typing import Generic, Callable
from exactly_lib.symbol.logic.matcher import MODEL
from exactly_lib.test_case.validation import ddv_validation
from exactly_lib.test_case.validation.ddv_validation import DdvValidator
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.description.tree_structured import StructureRenderer
from exactly_lib.type_system.logic.impls import advs
from exactly_lib.type_system.logic.impls.advs import ConstantMatcherAdv
from exactly_lib.type_system.logic.matcher_base_class import MatcherDdv, MatcherWTraceAndNegation, MatcherAdv

class MatcherDdvFromConstantPrimitive(Generic[MODEL], MatcherDdv[MODEL]):

    def __init__(self, primitive_value: MatcherWTraceAndNegation[MODEL], validator: DdvValidator=ddv_validation.constant_success_validator()):
        self._primitive_value = primitive_value
        self._validator = validator

    def structure(self) -> StructureRenderer:
        return self._primitive_value.structure()

    @property
    def validator(self) -> DdvValidator:
        return self._validator

    def value_of_any_dependency(self, tcds: Tcds) -> MatcherAdv[MODEL]:
        return advs.ConstantMatcherAdv(self._primitive_value)


class MatcherDdvFromPartsWConstantAdv(Generic[MODEL], MatcherDdv[MODEL]):

    def __init__(self, make_matcher: Callable[([Tcds], MatcherWTraceAndNegation[MODEL])], structure: StructureRenderer):
        self._make_matcher = make_matcher
        self._structure = structure

    def structure(self) -> StructureRenderer:
        return self._structure

    def value_of_any_dependency(self, tcds: Tcds) -> MatcherAdv[MODEL]:
        return ConstantMatcherAdv(self._make_matcher(tcds))