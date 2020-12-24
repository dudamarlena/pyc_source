# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/program/parse/parse_program.py
# Compiled at: 2020-01-31 11:01:50
# Size of source mod 2**32: 2486 bytes
from exactly_lib.definitions.entity import types
from exactly_lib.definitions.primitives import string_transformer
from exactly_lib.section_document import parser_classes
from exactly_lib.section_document.element_parsers.token_stream_parser import TokenParser
from exactly_lib.section_document.parser_classes import Parser
from exactly_lib.symbol.logic.program.program_sdv import ProgramSdv
from exactly_lib.test_case_utils.program import syntax_elements
from exactly_lib.test_case_utils.program.parse import parse_executable_file, parse_system_program, parse_shell_command, parse_with_reference_to_program
from exactly_lib.test_case_utils.string_transformer import parse_string_transformer

def program_parser() -> Parser[ProgramSdv]:
    return parser_classes.ParserFromTokenParserFunction(parse_program)


def parse_program--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL              _parse_simple_program
                3  LOAD_DEREF               'parser'

 L.  23         6  LOAD_FAST                'must_be_on_current_line'
                9  CALL_FUNCTION_2       2  '2 positional, 0 named'
               12  STORE_DEREF              'program'

 L.  25        15  LOAD_GLOBAL              TokenParser
               18  LOAD_GLOBAL              ProgramSdv
               21  LOAD_CONST               ('_parser', 'return')
               24  LOAD_CLOSURE             'parser'
               27  LOAD_CLOSURE             'program'
               30  BUILD_TUPLE_2         2 
               33  LOAD_CODE                <code_object parse_transformer>
               36  LOAD_STR                 'parse_program.<locals>.parse_transformer'
               39  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               45  STORE_FAST               'parse_transformer'

 L.  31        48  LOAD_DEREF               'parser'
               51  LOAD_ATTR                consume_and_handle_optional_option
               54  LOAD_DEREF               'program'

 L.  32        57  LOAD_FAST                'parse_transformer'

 L.  33        60  LOAD_GLOBAL              string_transformer
               63  LOAD_ATTR                WITH_TRANSFORMED_CONTENTS_OPTION_NAME
               66  CALL_FUNCTION_3       3  '3 positional, 0 named'
               69  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 33


def _parse_simple_program(parser: TokenParser, must_be_on_current_line=False) -> ProgramSdv:
    return parser.parse_default_or_optional_commandparse_executable_file.parse_as_program_PROGRAM_VARIANT_SETUPSmust_be_on_current_line


_PROGRAM_VARIANT_SETUPS = {syntax_elements.SHELL_COMMAND_TOKEN: parse_shell_command.parse_as_program, 
 syntax_elements.SYSTEM_PROGRAM_TOKEN: parse_system_program.parse_as_program, 
 syntax_elements.SYMBOL_REF_PROGRAM_TOKEN: parse_with_reference_to_program.parse_from_token_parser}