# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/line_matcher/impl/line_number.py
# Compiled at: 2020-01-16 12:15:32
# Size of source mod 2**32: 2143 bytes
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.definitions.primitives import line_matcher
from exactly_lib.section_document.element_parsers.token_stream_parser import TokenParser
from exactly_lib.symbol.logic.line_matcher import LineMatcherSdv
from exactly_lib.test_case_utils.description_tree.tree_structured import WithCachedTreeStructureDescriptionBase
from exactly_lib.test_case_utils.matcher import property_matcher
from exactly_lib.test_case_utils.matcher.impls import parse_integer_matcher, property_getters, property_matcher_describers
from exactly_lib.test_case_utils.matcher.property_getter import PropertyGetterSdv
from exactly_lib.type_system.description.tree_structured import StructureRenderer
from exactly_lib.type_system.logic.line_matcher import LineMatcherLine, GenericLineMatcherSdv
from exactly_lib.util.description_tree import renderers
from exactly_lib.util.logic_types import ExpectationType
_NAME = ' '.join((line_matcher.LINE_NUMBER_MATCHER_NAME,
 syntax_elements.INTEGER_MATCHER_SYNTAX_ELEMENT.singular_name))

def parse_line_number(parser: TokenParser) -> LineMatcherSdv:
    return LineMatcherSdv(parse_line_number__generic(parser))


def parse_line_number__generic(parser: TokenParser) -> GenericLineMatcherSdv:
    matcher = parse_integer_matcher.parse(parser, ExpectationType.POSITIVE, parse_integer_matcher.validator_for_non_negative)
    return property_matcher.PropertyMatcherSdv(matcher, _operand_from_model_sdv(), property_matcher_describers.GetterWithMatcherAsChild())


def _operand_from_model_sdv() -> PropertyGetterSdv[(LineMatcherLine, int)]:
    return property_getters.PropertyGetterSdvConstant(property_getters.PropertyGetterDdvConstant(_PropertyGetter()))


class _PropertyGetter(property_getters.PropertyGetter[(LineMatcherLine, int)], WithCachedTreeStructureDescriptionBase):

    def _structure(self) -> StructureRenderer:
        return renderers.header_only(_NAME)

    def get_from(self, model: LineMatcherLine) -> int:
        return model[0]