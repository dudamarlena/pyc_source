# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/assert_/utils/file_contents/parse_instruction.py
# Compiled at: 2019-12-27 10:07:25
# Size of source mod 2**32: 2779 bytes
from exactly_lib.instructions.assert_.utils import assertion_part
from exactly_lib.instructions.assert_.utils.assertion_part import AssertionInstructionFromAssertionPart, IdentityAssertionPartWithValidationAndReferences
from exactly_lib.instructions.assert_.utils.file_contents import parse_file_contents_assertion_part
from exactly_lib.instructions.assert_.utils.file_contents.actual_files import ComparisonActualFileConstructor
from exactly_lib.instructions.assert_.utils.file_contents.parts.contents_checkers import FileConstructorAssertionPart, IsExistingRegularFileAssertionPart
from exactly_lib.instructions.assert_.utils.instruction_parser import AssertPhaseInstructionTokenParser
from exactly_lib.section_document.element_parsers.token_stream_parser import TokenParser
from exactly_lib.section_document.parser_classes import Parser
from exactly_lib.test_case.phases.assert_ import AssertPhaseInstruction
from exactly_lib.test_case.phases.common import InstructionSourceInfo

class ComparisonActualFileParser(Parser[ComparisonActualFileConstructor]):
    pass


class Parser(AssertPhaseInstructionTokenParser):
    __doc__ = '\n    An instruction that\n\n     - checks the existence of a file,\n     - transform it using a given transformer\n     - performs a last custom check on the transformed file\n    '

    def __init__(self, instruction_name: str, actual_file_parser: ComparisonActualFileParser):
        self._instruction_name = instruction_name
        self._actual_file_parser = actual_file_parser

    def parse_from_token_parser(self, parser: TokenParser) -> AssertPhaseInstruction:
        source_info = InstructionSourceInfo(parser.first_line_number, self._instruction_name)
        actual_file_constructor = self._actual_file_parser.parse_from_token_parser(parser)
        actual_file_assertion_part = parse_file_contents_assertion_part.parse(parser)
        assertion_part_sequence = assertion_part.compose(IdentityAssertionPartWithValidationAndReferences(actual_file_constructor.validator, actual_file_constructor.references), FileConstructorAssertionPart())
        assertion_part_sequence = assertion_part.compose_with_sequence(assertion_part_sequence, IsExistingRegularFileAssertionPart())
        assertion_part_sequence = assertion_part.compose_with_sequence(assertion_part_sequence, actual_file_assertion_part)
        return AssertionInstructionFromAssertionPart(assertion_part_sequence, source_info, lambda env: actual_file_constructor, actual_file_constructor.failure_message_header)