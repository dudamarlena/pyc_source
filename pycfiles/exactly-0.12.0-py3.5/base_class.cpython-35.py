# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/string_matcher/impl/base_class.py
# Compiled at: 2019-12-27 19:58:42
# Size of source mod 2**32: 993 bytes
from abc import ABC
from exactly_lib.test_case_utils.description_tree.tree_structured import WithCachedNameAndTreeStructureDescriptionBase
from exactly_lib.test_case_utils.matcher.impls import combinator_matchers
from exactly_lib.type_system.description.trace_building import TraceBuilder
from exactly_lib.type_system.logic.matcher_base_class import MatcherWTraceAndNegation, MatcherDdv, MatcherAdv
from exactly_lib.type_system.logic.string_matcher import StringMatcher, FileToCheck

class StringMatcherImplBase(WithCachedNameAndTreeStructureDescriptionBase, MatcherWTraceAndNegation[FileToCheck], ABC):

    @property
    def negation(self) -> StringMatcher:
        return combinator_matchers.Negation(self)

    def _new_tb(self) -> TraceBuilder:
        return TraceBuilder(self.name)


class StringMatcherDdvImplBase(MatcherDdv[FileToCheck], ABC):
    pass


class StringMatcherAdvImplBase(MatcherAdv[FileToCheck], ABC):
    pass