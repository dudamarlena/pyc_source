# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/line_matcher/line_matchers.py
# Compiled at: 2019-12-27 10:07:52
# Size of source mod 2**32: 512 bytes
from typing import Sequence
from exactly_lib.test_case_utils.matcher.impls import combinator_matchers
from exactly_lib.type_system.logic.line_matcher import LineMatcher

def negation(matcher: LineMatcher) -> LineMatcher:
    return combinator_matchers.Negation(matcher)


def conjunction(matchers: Sequence[LineMatcher]) -> LineMatcher:
    return combinator_matchers.Conjunction(matchers)


def disjunction(matchers: Sequence[LineMatcher]) -> LineMatcher:
    return combinator_matchers.Disjunction(matchers)