# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/program/syntax_elements.py
# Compiled at: 2020-02-02 15:10:17
# Size of source mod 2**32: 1098 bytes
from exactly_lib.definitions.primitives import program
from exactly_lib.definitions.test_case.instructions import instruction_names
from exactly_lib.test_case_utils.parse import parse_path
from exactly_lib.util.cli_syntax.elements import argument
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.cli_syntax.option_syntax import long_option_syntax
SHELL_COMMAND_TOKEN = program.SHELL_COMMAND_TOKEN
SYSTEM_PROGRAM_TOKEN = program.SYSTEM_PROGRAM_TOKEN
SYMBOL_REF_PROGRAM_TOKEN = instruction_names.SYMBOL_REF_PROGRAM_INSTRUCTION_NAME
REL_OPTION_ARG_CONF = parse_path.ALL_REL_OPTIONS_CONFIG
PYTHON_EXECUTABLE_OPTION_NAME = argument.OptionName(long_name='python')
PYTHON_EXECUTABLE_OPTION_STRING = long_option_syntax(PYTHON_EXECUTABLE_OPTION_NAME.long)
REMAINING_PART_OF_CURRENT_LINE_AS_LITERAL_MARKER = ':>'
EXISTING_FILE_OPTION_NAME = a.OptionName(long_name='existing-file')
EXISTING_DIR_OPTION_NAME = a.OptionName(long_name='existing-dir')
EXISTING_PATH_OPTION_NAME = a.OptionName(long_name='existing-path')
ARGUMENT_SYNTAX_ELEMENT_NAME = a.Named('ARGUMENT')