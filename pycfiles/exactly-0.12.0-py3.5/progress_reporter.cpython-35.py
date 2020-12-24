# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/suite_reporters/objects/progress_reporter.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 3843 bytes
from exactly_lib.common.exit_value import ExitValue
from exactly_lib.definitions import misc_texts
from exactly_lib.definitions.doc_format import exit_value_text
from exactly_lib.definitions.entity.suite_reporters import PROGRESS_REPORTER
from exactly_lib.execution.full_execution.result import FullExeResultStatus
from exactly_lib.help.entities.suite_reporters.contents_structure import SuiteReporterDocumentation
from exactly_lib.processing import exit_values as case_exit_values
from exactly_lib.test_suite import exit_values
from exactly_lib.test_suite.reporters import simple_progress_reporter as reporter
from exactly_lib.util.textformat.structure.structures import *
from exactly_lib.util.textformat.textformat_parser import TextParser

class SimpleProgressSuiteReporterDocumentation(SuiteReporterDocumentation):

    def __init__(self):
        super().__init__(PROGRESS_REPORTER)
        format_map = {}
        self._parser = TextParser(format_map)

    def syntax_of_output(self) -> List[ParagraphItem]:
        return self._parser.fnap(_SYNTAX_OF_OUTPUT)

    def exit_code_description(self) -> List[ParagraphItem]:
        return self._parser.fnap(_EXIT_CODE_DESCRIPTION_PRELUDE) + [
         self._exit_value_table(_exit_values_and_descriptions())]

    def _exit_value_table--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL              ExitValue
                3  LOAD_GLOBAL              str
                6  LOAD_GLOBAL              List
                9  LOAD_GLOBAL              TableCell
               12  BINARY_SUBSCR    
               13  LOAD_CONST               ('exit_value', 'description', 'return')
               16  LOAD_CLOSURE             'self'
               19  BUILD_TUPLE_1         1 
               22  LOAD_CODE                <code_object _row>
               25  LOAD_STR                 'SimpleProgressSuiteReporterDocumentation._exit_value_table.<locals>._row'
               28  MAKE_CLOSURE_A_4_0        '0 positional, 0 keyword only, 4 annotated'
               34  STORE_DEREF              '_row'

 L.  36        37  LOAD_GLOBAL              first_row_is_header_table

 L.  39        40  LOAD_GLOBAL              cell
               43  LOAD_GLOBAL              paras
               46  LOAD_GLOBAL              misc_texts
               49  LOAD_ATTR                EXIT_CODE_TITLE
               52  CALL_FUNCTION_1       1  '1 positional, 0 named'
               55  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  40        58  LOAD_GLOBAL              cell
               61  LOAD_GLOBAL              paras
               64  LOAD_GLOBAL              misc_texts
               67  LOAD_ATTR                EXIT_IDENTIFIER_TITLE
               70  CALL_FUNCTION_1       1  '1 positional, 0 named'
               73  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  41        76  LOAD_GLOBAL              cell
               79  LOAD_GLOBAL              paras
               82  LOAD_STR                 'When'
               85  CALL_FUNCTION_1       1  '1 positional, 0 named'
               88  CALL_FUNCTION_1       1  '1 positional, 0 named'
               91  BUILD_LIST_3          3 
               94  BUILD_LIST_1          1 

 L.  43        97  LOAD_CLOSURE             '_row'
              100  BUILD_TUPLE_1         1 
              103  LOAD_LISTCOMP            '<code_object <listcomp>>'
              106  LOAD_STR                 'SimpleProgressSuiteReporterDocumentation._exit_value_table.<locals>.<listcomp>'
              109  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'
              112  LOAD_FAST                'exit_value_and_description_list'
              115  GET_ITER         
              116  CALL_FUNCTION_1       1  '1 positional, 0 named'
              119  BINARY_ADD       

 L.  44       120  LOAD_STR                 '  '
              123  CALL_FUNCTION_2       2  '2 positional, 0 named'
              126  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


DOCUMENTATION = SimpleProgressSuiteReporterDocumentation()
_SYNTAX_OF_OUTPUT = 'Reports one event per line:\n\n\n * beginning of test suite\n * execution of test case\n * end of test suite\n\n\nBeginning and end of test suites wraps the test cases that are contained directly in the test suite\n(i.e. it does not wrap test cases that are contained in sub suites).\n\n\nLast line is an exit identifier, that depends on the outcome of the suite, and is related to the exit code.\n\nA summary is printed on stderr.\n'
_EXIT_CODE_DESCRIPTION_PRELUDE = 'Exit codes, and corresponding exit identifiers printed as the last line of stdout:\n'

def _exit_values_list(full_result_statuses) -> str:
    evs = mapcase_exit_values.from_full_resultfull_result_statuses
    return ', '.join(sorted(mapExitValue.exit_identifier.fgetevs))


def _all_pass_description() -> str:
    return 'All test cases could be executed, and result was one of ' + _exit_values_list(reporter.SUCCESS_STATUSES) + '.'


def _failed_tests_description() -> str:
    non_pass_result_statuses = set()
    for st in list(FullExeResultStatus):
        if st not in reporter.SUCCESS_STATUSES:
            non_pass_result_statuses.add(st)

    return 'At least one test case could not be executed,\nor was executed with a result other than those above:\n' + _exit_values_list(non_pass_result_statuses) + '.'


_INVALID_SUITE_DESCRIPTION = 'There was an error reading the test suite.\n\nNo test cases have been executed.\n'

def _exit_values_and_descriptions() -> list:
    return [
     (
      exit_values.ALL_PASS, _all_pass_description()),
     (
      exit_values.FAILED_TESTS, _failed_tests_description()),
     (
      exit_values.INVALID_SUITE, _INVALID_SUITE_DESCRIPTION)]