# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/processing/standalone/accessor_resolver.py
# Compiled at: 2019-09-20 02:11:24
# Size of source mod 2**32: 2842 bytes
import pathlib
from typing import Optional, Tuple
from exactly_lib.definitions.test_suite import file_names
from exactly_lib.processing import test_case_processing as processing, processors
from exactly_lib.processing.act_phase import ActPhaseSetup
from exactly_lib.processing.instruction_setup import TestCaseParsingSetup
from exactly_lib.processing.test_case_handling_setup import TestCaseHandlingSetup
from exactly_lib.section_document.section_element_parsing import SectionElementParser

class AccessorResolver:

    def __init__(self, test_case_parsing_setup: TestCaseParsingSetup, suite_configuration_section_parser: SectionElementParser, default_handling_setup: TestCaseHandlingSetup):
        self._test_case_parsing_setup = test_case_parsing_setup
        self._suite_configuration_section_parser = suite_configuration_section_parser
        self._default_handling_setup = default_handling_setup

    def resolve(self, test_case_file_path: pathlib.Path, explicit_suite_file_path: Optional[pathlib.Path]) -> Tuple[(processing.Accessor, ActPhaseSetup)]:
        """
        :raises SuiteParseError
        """
        handling_setup = self._handling_setup(test_case_file_path, explicit_suite_file_path)
        return (
         processors.new_accessor(handling_setup.preprocessor, self._test_case_parsing_setup, handling_setup.transformer),
         handling_setup.act_phase_setup)

    def _handling_setup--- This code section failed: ---

 L.  44         0  LOAD_GLOBAL              Optional
                3  LOAD_GLOBAL              pathlib
                6  LOAD_ATTR                Path
                9  BINARY_SUBSCR    
               10  LOAD_CONST               ('return',)
               13  LOAD_CLOSURE             'explicit_suite_file_path'
               16  LOAD_CLOSURE             'test_case_file_path'
               19  BUILD_TUPLE_2         2 
               22  LOAD_CODE                <code_object get_suite_file>
               25  LOAD_STR                 'AccessorResolver._handling_setup.<locals>.get_suite_file'
               28  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               34  STORE_FAST               'get_suite_file'

 L.  54        37  LOAD_FAST                'get_suite_file'
               40  CALL_FUNCTION_0       0  '0 positional, 0 named'
               43  STORE_FAST               'suite_file_path'

 L.  56        46  LOAD_FAST                'suite_file_path'
               49  UNARY_NOT        
               50  POP_JUMP_IF_FALSE    60  'to 60'

 L.  57        53  LOAD_FAST                'self'
               56  LOAD_ATTR                _default_handling_setup
               59  RETURN_END_IF    
             60_0  COME_FROM            50  '50'

 L.  58        60  LOAD_CONST               0
               63  LOAD_CONST               ('resolve_handling_setup_from_suite_file',)
               66  IMPORT_NAME              exactly_lib.test_suite.file_reading.suite_file_reading
               69  IMPORT_FROM              resolve_handling_setup_from_suite_file
               72  STORE_FAST               'resolve_handling_setup_from_suite_file'
               75  POP_TOP          

 L.  59        76  LOAD_FAST                'resolve_handling_setup_from_suite_file'
               79  LOAD_FAST                'self'
               82  LOAD_ATTR                _default_handling_setup

 L.  60        85  LOAD_FAST                'self'
               88  LOAD_ATTR                _suite_configuration_section_parser

 L.  61        91  LOAD_FAST                'self'
               94  LOAD_ATTR                _test_case_parsing_setup

 L.  62        97  LOAD_FAST                'suite_file_path'
              100  CALL_FUNCTION_4       4  '4 positional, 0 named'
              103  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1