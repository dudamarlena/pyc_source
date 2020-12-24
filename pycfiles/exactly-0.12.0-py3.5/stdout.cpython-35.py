# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/assert_/stdout.py
# Compiled at: 2019-09-29 05:55:08
# Size of source mod 2**32: 992 bytes
from exactly_lib.common.instruction_setup import SingleInstructionSetup
from exactly_lib.instructions.assert_.utils.file_contents import parse_instruction
from exactly_lib.instructions.assert_.utils.file_contents import stdout_stderr as utils
from exactly_lib.instructions.assert_.utils.instruction_parser import AssertPhaseInstructionParser
from exactly_lib.test_case_file_structure import sandbox_directory_structure
from exactly_lib.util.process_execution.process_output_files import ProcOutputFile

def setup_for_stdout(instruction_name: str) -> SingleInstructionSetup:
    return SingleInstructionSetup(parser(instruction_name), utils.TheInstructionDocumentation(instruction_name, sandbox_directory_structure.RESULT_FILE__STDOUT))


def parser(instruction_name: str) -> AssertPhaseInstructionParser:
    return parse_instruction.Parser(instruction_name, utils.Parser(ProcOutputFile.STDOUT))