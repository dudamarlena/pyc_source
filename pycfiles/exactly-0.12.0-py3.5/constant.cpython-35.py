# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/impls/constant.py
# Compiled at: 2020-01-31 11:01:50
# Size of source mod 2**32: 1382 bytes
from typing import Generic
from exactly_lib.definitions import logic
from exactly_lib.type_system.description.tree_structured import StructureRenderer
from exactly_lib.type_system.logic.matcher_base_class import MatcherWTraceAndNegation, MODEL, MatchingResult
from exactly_lib.util.description_tree import renderers, tree

class MatcherWithConstantResult(Generic[MODEL], MatcherWTraceAndNegation[MODEL]):

    def __init__(self, result: bool):
        self._result = result
        self._matching_result = MatchingResult(self._result, renderers.Constant(tree.Node(logic.CONSTANT_MATCHER, self._result, (
         tree.StringDetail(logic.BOOLEANS[result]),), ())))
        self._structure = renderers.Constant(tree.Node(logic.CONSTANT_MATCHER, None, (
         tree.StringDetail(logic.BOOLEANS[result]),), ()))

    @property
    def name(self) -> str:
        return self.NAME

    def structure(self) -> StructureRenderer:
        return self._structure

    @property
    def negation(self) -> 'MatcherWithConstantResult[MODEL]':
        return MatcherWithConstantResult(not self._result)

    def matches_w_trace(self, model: MODEL) -> MatchingResult:
        return self._matching_result