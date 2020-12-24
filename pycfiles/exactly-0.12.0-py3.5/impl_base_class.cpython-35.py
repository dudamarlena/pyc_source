# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/impls/impl_base_class.py
# Compiled at: 2019-12-27 10:07:52
# Size of source mod 2**32: 898 bytes
from abc import ABC
from typing import Generic
from exactly_lib.test_case_utils.description_tree.tree_structured import WithCachedNameAndTreeStructureDescriptionBase
from exactly_lib.test_case_utils.matcher.impls import combinator_matchers
from exactly_lib.type_system.description.trace_building import TraceBuilder
from exactly_lib.type_system.logic.matcher_base_class import MatcherWTraceAndNegation, MODEL

class MatcherImplBase(Generic[MODEL], MatcherWTraceAndNegation[MODEL], WithCachedNameAndTreeStructureDescriptionBase, ABC):

    def __init__(self):
        WithCachedNameAndTreeStructureDescriptionBase.__init__(self)

    def _new_tb(self) -> TraceBuilder:
        return TraceBuilder(self.name)

    @property
    def negation(self) -> MatcherWTraceAndNegation[MODEL]:
        return combinator_matchers.Negation(self)