# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/program_modes/test_case/contents/specification/intro.py
# Compiled at: 2020-02-01 11:05:03
# Size of source mod 2**32: 3637 bytes
from exactly_lib.definitions import formatting, misc_texts
from exactly_lib.definitions.entity import concepts
from exactly_lib.definitions.test_case import phase_names
from exactly_lib.definitions.test_case.instructions import instruction_names
from exactly_lib.processing import exit_values
from exactly_lib.program_info import PROGRAM_NAME
from exactly_lib.test_case_utils.condition import comparators
from exactly_lib.test_case_utils.string_matcher.matcher_options import EQUALS_ARGUMENT
from exactly_lib.util.textformat.constructor.environment import ConstructionEnvironment
from exactly_lib.util.textformat.constructor.section import SectionContentsConstructor
from exactly_lib.util.textformat.structure import document as doc
from exactly_lib.util.textformat.structure import structures as docs
from exactly_lib.util.textformat.textformat_parser import TextParser

class Documentation(SectionContentsConstructor):

    def __init__(self):
        self._tp = TextParser({'test_case_file': 'helloworld.case', 
         'EXECUTABLE_PROGRAM': PROGRAM_NAME, 
         'program_name': formatting.program_name(PROGRAM_NAME), 
         'action_to_check': 'helloworld', 
         'ATC': formatting.concept_(concepts.ACTION_TO_CHECK_CONCEPT_INFO), 
         'CONTENTS_EQUALS_ARGUMENT': EQUALS_ARGUMENT, 
         'INT_EQUALS_OPERATOR': comparators.EQ.name, 
         'act': phase_names.ACT, 
         'assert': phase_names.ASSERT, 
         'PASS': exit_values.EXECUTION__PASS.exit_identifier, 
         'FAIL': exit_values.EXECUTION__FAIL.exit_identifier, 
         'stdout_instruction': instruction_names.CONTENTS_OF_STDOUT_INSTRUCTION_NAME, 
         'exit_code_instruction': instruction_names.EXIT_CODE_INSTRUCTION_NAME, 
         'executable_file': formatting.misc_name_with_formatting(misc_texts.EXECUTABLE_FILE)})

    def apply(self, environment: ConstructionEnvironment) -> doc.SectionContents:
        return doc.SectionContents(self._tp.fnap(_INITIAL_DESCRIPTION), [
         docs.section('File structure', self._tp.fnap(_FILE_STRUCTURE))])


_INITIAL_DESCRIPTION = 'A test case is written as a plain text file:\n\n\n```\n{act:syntax}\n\n{action_to_check}\n\n{assert:syntax}\n\n{exit_code_instruction} {INT_EQUALS_OPERATOR} 0\n\n{stdout_instruction} {CONTENTS_EQUALS_ARGUMENT} <<EOF\nHello, World!\nEOF\n```\n\n\nIf the file "{test_case_file}" contains this test case,\nthen {program_name} can execute it:\n\n\n```\n> {EXECUTABLE_PROGRAM} {test_case_file}\n{PASS}\n```\n\n\n"{PASS}" means that {program_name} was able to execute the "{action_to_check}" program,\nand that all assertions were satisfied.\n\n\nIt also means that the executable "{action_to_check}" file\nwas found in in the same directory as the test case file.\n'
_FILE_STRUCTURE = '{act:syntax} marks the beginning of the {act} phase.\n\n\nThe {act} phase contains the {ATC} - the thing that is tested by the test case.\n\n\nIt must consist of a single command line,\nstarting with the name of {executable_file:a}\n(by default).\n\nThe file must be located in the same directory as the test case file (by default).\n\n\n{assert:syntax} marks the beginning of the {assert} phase.\n\n\nThe {assert} phase contains assertions,\nsuch as "{exit_code_instruction}" and "{stdout_instruction}".\n\n\nThe assertions determines the outcome of the test case.\n\nEach assertion either {PASS} or {FAIL}.\nIf any assertion {FAIL}, then the outcome of the test case as a whole is {FAIL}.\nOtherwise it is {PASS}.\n'