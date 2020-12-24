# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/impls/parse_integer_matcher.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 1602 bytes
from typing import Optional
from exactly_lib.common.report_rendering.text_doc import TextRenderer
from exactly_lib.section_document.element_parsers.token_stream_parser import TokenParser
from exactly_lib.symbol.logic.matcher import MatcherSdv
from exactly_lib.test_case_utils.condition.integer import parse_integer_condition
from exactly_lib.test_case_utils.condition.integer.integer_ddv import CustomIntegerValidator
from exactly_lib.test_case_utils.matcher.impls.comparison_matcher import ComparisonMatcherSdv
from exactly_lib.test_case_utils.matcher.impls.operand_object import ObjectSdvOfOperandSdv
from exactly_lib.util.description_tree import details
from exactly_lib.util.logic_types import ExpectationType
from exactly_lib.util.messages import expected_found

def parse(parser: TokenParser, expectation_type: ExpectationType, custom_integer_restriction: Optional[CustomIntegerValidator]) -> MatcherSdv[int]:
    op_and_rhs = parse_integer_condition.parse_integer_comparison_operator_and_rhs(parser, custom_integer_restriction)
    return ComparisonMatcherSdv(expectation_type, op_and_rhs.operator, ObjectSdvOfOperandSdv(op_and_rhs.rhs_operand), lambda x: details.String(x))


def validator_for_non_negative(actual: int) -> Optional[TextRenderer]:
    if actual < 0:
        return expected_found.unexpected_lines(_NON_NEGATIVE_INTEGER_ARGUMENT_DESCRIPTION, str(actual))


_NON_NEGATIVE_INTEGER_ARGUMENT_DESCRIPTION = 'An integer >= 0'