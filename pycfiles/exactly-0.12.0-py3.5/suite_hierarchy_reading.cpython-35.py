# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_suite/file_reading/suite_hierarchy_reading.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 6945 bytes
import functools, pathlib
from pathlib import Path
from typing import List, Tuple, Callable
from exactly_lib.definitions.test_suite import section_names
from exactly_lib.processing import test_case_processing
from exactly_lib.processing.instruction_setup import TestCaseParsingSetup
from exactly_lib.processing.test_case_handling_setup import TestCaseHandlingSetup
from exactly_lib.section_document.model import SectionContents, ElementType, SectionContentElement
from exactly_lib.section_document.section_element_parsing import SectionElementParser
from exactly_lib.test_suite import structure
from exactly_lib.test_suite import test_suite_doc
from exactly_lib.test_suite.file_reading import exception, suite_file_reading
from exactly_lib.test_suite.instruction_set import instruction
from exactly_lib.test_suite.instruction_set.instruction import TestSuiteFileReferencesInstruction

class SuiteHierarchyReader:

    def apply(self, suite_file_path: pathlib.Path) -> structure.TestSuiteHierarchy:
        """
        :raises SuiteReadError
        """
        raise NotImplementedError()


class Environment(tuple):

    def __new__(cls, configuration_section_parser: SectionElementParser, test_case_parsing_setup: TestCaseParsingSetup, default_test_case_handling_setup: TestCaseHandlingSetup):
        return tuple.__new__(cls, (configuration_section_parser,
         default_test_case_handling_setup,
         test_case_parsing_setup))

    @property
    def configuration_section_parser(self) -> SectionElementParser:
        return self[0]

    @property
    def default_test_case_handling_setup(self) -> TestCaseHandlingSetup:
        return self[1]

    @property
    def test_case_parsing_setup(self) -> TestCaseParsingSetup:
        return self[2]


class Reader(SuiteHierarchyReader):

    def __init__(self, environment: Environment):
        self._environment = environment

    def apply(self, suite_file_path: pathlib.Path) -> structure.TestSuiteHierarchy:
        return _SingleFileReader(self._environment, suite_file_path).apply()


class _SingleFileReader:

    def __init__(self, environment: Environment, root_suite_file_path: pathlib.Path):
        self.environment = environment
        self._root_suite_file_path = root_suite_file_path
        self._visited = {self._root_suite_file_path.resolve(): None}

    def apply(self) -> structure.TestSuiteHierarchy:
        return self.__call__([], self._root_suite_file_path)

    def __call__(self, inclusions: List[pathlib.Path], suite_file_path: pathlib.Path) -> structure.TestSuiteHierarchy:
        test_suite = suite_file_reading.read_suite_document(suite_file_path, self.environment.configuration_section_parser, self.environment.test_case_parsing_setup)
        test_case_handling_setup = suite_file_reading.resolve_test_case_handling_setup(test_suite, self.environment.default_test_case_handling_setup)
        suite_file_path_list, case_file_path_list = self._resolve_paths(test_suite, suite_file_path)
        sub_inclusions = inclusions + [suite_file_path]
        sub_suites_reader = functools.partial(self, sub_inclusions)
        suite_list = list(map(sub_suites_reader, suite_file_path_list))
        case_list = list(map(test_case_processing.test_case_reference_of_source_file, case_file_path_list))
        return structure.TestSuiteHierarchy(suite_file_path, inclusions, test_case_handling_setup, suite_list, case_list)

    def _resolve_paths--- This code section failed: ---

 L.  94         0  LOAD_GLOBAL              instruction
                3  LOAD_ATTR                Environment

 L.  95         6  LOAD_GLOBAL              str

 L.  96         9  LOAD_GLOBAL              SectionContents

 L.  97        12  LOAD_GLOBAL              Callable
               15  LOAD_GLOBAL              SectionContentElement
               18  LOAD_GLOBAL              List
               21  LOAD_GLOBAL              Path
               24  BINARY_SUBSCR    
               25  BUILD_LIST_2          2 
               28  LOAD_CONST               None
               31  BUILD_TUPLE_2         2 
               34  BINARY_SUBSCR    

 L.  98        35  LOAD_GLOBAL              List
               38  LOAD_GLOBAL              Path
               41  BINARY_SUBSCR    
               42  LOAD_CONST               ('env', 'section_name', 'section_contents', 'paths_checker', 'return')
               45  LOAD_CLOSURE             'suite_file_path'
               48  BUILD_TUPLE_1         1 
               51  LOAD_CODE                <code_object paths_for_instructions>
               54  LOAD_STR                 '_SingleFileReader._resolve_paths.<locals>.paths_for_instructions'
               57  MAKE_CLOSURE_A_6_0        '0 positional, 0 keyword only, 6 annotated'
               63  STORE_FAST               'paths_for_instructions'

 L. 116        66  LOAD_GLOBAL              SectionContentElement

 L. 117        69  LOAD_GLOBAL              List
               72  LOAD_GLOBAL              pathlib
               75  LOAD_ATTR                Path
               78  BINARY_SUBSCR    
               79  LOAD_CONST               ('element', 'paths_from_instruction')
               82  LOAD_CLOSURE             'self'
               85  LOAD_CLOSURE             'suite_file_path'
               88  BUILD_TUPLE_2         2 
               91  LOAD_CODE                <code_object check_suite_paths_for_double_inclusion>
               94  LOAD_STR                 '_SingleFileReader._resolve_paths.<locals>.check_suite_paths_for_double_inclusion'
               97  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
              103  STORE_FAST               'check_suite_paths_for_double_inclusion'

 L. 128       106  LOAD_GLOBAL              SectionContentElement

 L. 129       109  LOAD_GLOBAL              List
              112  LOAD_GLOBAL              pathlib
              115  LOAD_ATTR                Path
              118  BINARY_SUBSCR    
              119  LOAD_CONST               ('element', 'paths_from_instruction')
              122  LOAD_CODE                <code_object no_check>
              125  LOAD_STR                 '_SingleFileReader._resolve_paths.<locals>.no_check'
              128  EXTENDED_ARG          3  0x3 << 16 = 196608
              131  MAKE_FUNCTION_A_3_0        '0 positional, 0 keyword only, 3 annotated'
              134  STORE_FAST               'no_check'

 L. 132       137  LOAD_GLOBAL              instruction
              140  LOAD_ATTR                Environment
              143  LOAD_DEREF               'suite_file_path'
              146  LOAD_ATTR                parent
              149  CALL_FUNCTION_1       1  '1 positional, 0 named'
              152  STORE_FAST               'environment'

 L. 133       155  LOAD_FAST                'paths_for_instructions'
              158  LOAD_FAST                'environment'

 L. 134       161  LOAD_GLOBAL              section_names
              164  LOAD_ATTR                SUITES
              167  LOAD_ATTR                plain

 L. 135       170  LOAD_FAST                'test_suite'
              173  LOAD_ATTR                suites_section

 L. 136       176  LOAD_FAST                'check_suite_paths_for_double_inclusion'
              179  CALL_FUNCTION_4       4  '4 positional, 0 named'

 L. 137       182  LOAD_FAST                'paths_for_instructions'
              185  LOAD_FAST                'environment'

 L. 138       188  LOAD_GLOBAL              section_names
              191  LOAD_ATTR                CASES
              194  LOAD_ATTR                plain

 L. 139       197  LOAD_FAST                'test_suite'
              200  LOAD_ATTR                cases_section

 L. 140       203  LOAD_FAST                'no_check'
              206  CALL_FUNCTION_4       4  '4 positional, 0 named'
              209  BUILD_TUPLE_2         2 
              212  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 51