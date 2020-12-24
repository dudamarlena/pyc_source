# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/negation_of_predicate.py
# Compiled at: 2020-01-31 11:01:50
# Size of source mod 2**32: 1116 bytes
from exactly_lib.common.help.syntax_contents_structure import SyntaxElementDescription
from exactly_lib.definitions import logic
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.textformat.parse import normalize_and_parse

def assertion_syntax_element_description(additional_text: str='') -> SyntaxElementDescription:
    return SyntaxElementDescription(logic.NOT_OPERATOR_NAME, normalize_and_parse(_ASSERTION_NEGATION_ELEMENT_DESCRIPTION + additional_text))


def matcher_syntax_element_description(additional_text: str='') -> SyntaxElementDescription:
    return SyntaxElementDescription(logic.NOT_OPERATOR_NAME, normalize_and_parse(_MATCHER_NEGATION_ELEMENT_DESCRIPTION + additional_text))


def optional_negation_argument_usage() -> a.ArgumentUsage:
    return a.Single(a.Multiplicity.OPTIONAL, a.Constant(logic.NOT_OPERATOR_NAME))


_ASSERTION_NEGATION_ELEMENT_DESCRIPTION = 'Negates the assertion.\n'
_MATCHER_NEGATION_ELEMENT_DESCRIPTION = 'Negates the matcher.\n'