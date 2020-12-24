# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_suite/reporters/simple_progress_reporter.py
# Compiled at: 2020-01-23 16:48:01
# Size of source mod 2**32: 8468 bytes
import datetime, os, pathlib
from typing import Dict, List, Tuple
from exactly_lib.common.exit_value import ExitValue
from exactly_lib.common.process_result_reporter import Environment
from exactly_lib.execution.full_execution.result import FullExeResultStatus
from exactly_lib.processing import test_case_processing, exit_values as test_case_exit_values
from exactly_lib.processing.test_case_processing import Status, TestCaseFileReference
from exactly_lib.test_suite import reporting, structure, exit_values
from exactly_lib.test_suite.reporting import TestCaseProcessingInfo
from exactly_lib.util import name
from exactly_lib.util.file_printer import FilePrinter, file_printer_with_color_if_terminal
from exactly_lib.util.std import StdOutputFiles
SUCCESS_STATUSES = {
 FullExeResultStatus.PASS,
 FullExeResultStatus.SKIPPED,
 FullExeResultStatus.XFAIL}
_TIME_FORMAT = '%.3fs'
_TIME_FORMAT__CASE = '(' + _TIME_FORMAT + ') '

class SimpleProgressSubSuiteProgressReporter(reporting.SubSuiteProgressReporter):

    def __init__(self, output_file: FilePrinter, suite: structure.TestSuiteHierarchy, root_suite_dir_abs_path: pathlib.Path):
        self.output_file = output_file
        self.suite = suite
        self._rel_path_presenter = _RelPathPresenter(root_suite_dir_abs_path)

    def suite_begin(self):
        self.output_file.write_line('suite ' + self._file_path_pres(self.suite.source_file) + ': begin')

    def suite_end(self):
        self.output_file.write_line('suite ' + self._file_path_pres(self.suite.source_file) + ': end')

    def case_begin(self, case: test_case_processing.TestCaseFileReference):
        self.output_file.write('case  ' + self._file_path_pres(case.file_path) + ': ', flush=True)

    def case_end(self, case: test_case_processing.TestCaseFileReference, processing_info: TestCaseProcessingInfo):
        exit_value = test_case_exit_values.from_result(processing_info.result)
        self.output_file.write(_TIME_FORMAT__CASE % processing_info.duration.total_seconds())
        self.output_file.write_colored_line(exit_value.exit_identifier, exit_value.color)

    def _file_path_pres(self, file: pathlib.Path):
        return self._rel_path_presenter.present(file)


class _RelPathPresenter:

    def __init__(self, relativity_root_abs_path: pathlib.Path):
        self.relativity_root_abs_path = relativity_root_abs_path

    def present(self, file: pathlib.Path) -> str:
        try:
            return str(file.relative_to(self.relativity_root_abs_path))
        except ValueError:
            return str(file)


class SimpleProgressRootSuiteProcessingReporter(reporting.RootSuiteProcessingReporter):

    def report_invalid_suite(self, exit_value: ExitValue, reporting_environment: Environment):
        reporting_environment.out_printer.write_colored_line(exit_value.exit_identifier, exit_value.color)

    def execution_reporter(self, root_suite: structure.TestSuiteHierarchy, reporting_environment: Environment, root_suite_file: pathlib.Path) -> reporting.RootSuiteReporter:
        root_suite_dir_abs_path = root_suite_file.resolve().parent
        return SimpleProgressRootSuiteReporter(reporting_environment.std_files, root_suite_dir_abs_path)


class SimpleProgressRootSuiteReporter(reporting.RootSuiteReporter):

    def __init__(self, std_output_files: StdOutputFiles, root_suite_dir_abs_path: pathlib.Path):
        self._std_output_files = std_output_files
        self._output_file = file_printer_with_color_if_terminal(std_output_files.out)
        self._error_file = file_printer_with_color_if_terminal(std_output_files.err)
        self._sub_reporters = []
        self._start_time = None
        self._total_time_timedelta = None
        self._root_suite_dir_abs_path = root_suite_dir_abs_path

    def root_suite_begin(self):
        self._start_time = datetime.datetime.now()

    def root_suite_end(self):
        stop_time = datetime.datetime.now()
        self._total_time_timedelta = stop_time - self._start_time

    def new_sub_suite_reporter(self, sub_suite: structure.TestSuiteHierarchy) -> reporting.SubSuiteReporter:
        progress_reporter = SimpleProgressSubSuiteProgressReporter(self._output_file, sub_suite, self._root_suite_dir_abs_path)
        reporter = reporting.SubSuiteReporter(sub_suite, progress_reporter)
        self._sub_reporters.append(reporter)
        return reporter

    def report_final_results(self) -> int:
        num_cases, errors, exit_value = self._valid_suite_exit_value()
        lines = format_final_result_for_valid_suite(num_cases, self._total_time_timedelta, self._root_suite_dir_abs_path, errors)
        self._std_output_files.out.flush()
        lines.insert(0, '')
        self._error_file.write_line(os.linesep.join(lines))
        self._std_output_files.err.flush()
        self._output_file.write_colored_line(exit_value.exit_identifier, exit_value.color)
        return exit_value.exit_code

    def _valid_suite_exit_value--- This code section failed: ---

 L. 126         0  BUILD_MAP_0           0 
                3  STORE_DEREF              'errors'

 L. 128         6  LOAD_GLOBAL              exit_values
                9  LOAD_ATTR                ExitValue
               12  LOAD_GLOBAL              TestCaseFileReference
               15  LOAD_CONST               ('exit_value', 'case')
               18  LOAD_CLOSURE             'errors'
               21  BUILD_TUPLE_1         1 
               24  LOAD_CODE                <code_object add_error>
               27  LOAD_STR                 'SimpleProgressRootSuiteReporter._valid_suite_exit_value.<locals>.add_error'
               30  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               36  STORE_FAST               'add_error'

 L. 132        39  LOAD_CONST               0
               42  STORE_FAST               'num_tests'

 L. 133        45  LOAD_GLOBAL              exit_values
               48  LOAD_ATTR                ALL_PASS
               51  STORE_FAST               'exit_value'

 L. 134        54  SETUP_LOOP          244  'to 244'
               57  LOAD_FAST                'self'
               60  LOAD_ATTR                _sub_reporters
               63  GET_ITER         
               64  FOR_ITER            243  'to 243'
               67  STORE_FAST               'suite_reporter'

 L. 135        70  LOAD_GLOBAL              isinstance
               73  LOAD_FAST                'suite_reporter'
               76  LOAD_GLOBAL              reporting
               79  LOAD_ATTR                SubSuiteReporter
               82  CALL_FUNCTION_2       2  '2 positional, 0 named'
               85  POP_JUMP_IF_TRUE     94  'to 94'
               88  LOAD_ASSERT              AssertionError
               91  RAISE_VARARGS_1       1  'exception'
             94_0  COME_FROM            85  '85'

 L. 136        94  SETUP_LOOP          240  'to 240'
               97  LOAD_FAST                'suite_reporter'
              100  LOAD_ATTR                result
              103  CALL_FUNCTION_0       0  '0 positional, 0 named'
              106  GET_ITER         
              107  FOR_ITER            239  'to 239'
              110  UNPACK_SEQUENCE_2     2 
              113  STORE_FAST               'case_setup'
              116  STORE_FAST               'processing_info'

 L. 137       119  LOAD_FAST                'processing_info'
              122  LOAD_ATTR                result
              125  STORE_FAST               'result'

 L. 138       128  LOAD_FAST                'num_tests'
              131  LOAD_CONST               1
              134  INPLACE_ADD      
              135  STORE_FAST               'num_tests'

 L. 139       138  LOAD_GLOBAL              test_case_exit_values
              141  LOAD_ATTR                from_result
              144  LOAD_FAST                'result'
              147  CALL_FUNCTION_1       1  '1 positional, 0 named'
              150  STORE_FAST               'case_exit_value'

 L. 140       153  LOAD_FAST                'result'
              156  LOAD_ATTR                status
              159  LOAD_GLOBAL              Status
              162  LOAD_ATTR                EXECUTED
              165  COMPARE_OP               is-not
              168  POP_JUMP_IF_FALSE   196  'to 196'

 L. 141       171  LOAD_GLOBAL              exit_values
              174  LOAD_ATTR                FAILED_TESTS
              177  STORE_FAST               'exit_value'

 L. 142       180  LOAD_FAST                'add_error'
              183  LOAD_FAST                'case_exit_value'
              186  LOAD_FAST                'case_setup'
              189  CALL_FUNCTION_2       2  '2 positional, 0 named'
              192  POP_TOP          
              193  JUMP_FORWARD        236  'to 236'
              196  ELSE                     '236'

 L. 143       196  LOAD_FAST                'result'
              199  LOAD_ATTR                execution_result
              202  LOAD_ATTR                status
              205  LOAD_GLOBAL              SUCCESS_STATUSES
              208  COMPARE_OP               not-in
              211  POP_JUMP_IF_FALSE   236  'to 236'

 L. 144       214  LOAD_GLOBAL              exit_values
              217  LOAD_ATTR                FAILED_TESTS
              220  STORE_FAST               'exit_value'

 L. 145       223  LOAD_FAST                'add_error'
              226  LOAD_FAST                'case_exit_value'
              229  LOAD_FAST                'case_setup'
              232  CALL_FUNCTION_2       2  '2 positional, 0 named'
              235  POP_TOP          
            236_0  COME_FROM           211  '211'
            236_1  COME_FROM           193  '193'
              236  JUMP_BACK           107  'to 107'
              239  POP_BLOCK        
            240_0  COME_FROM_LOOP       94  '94'
              240  JUMP_BACK            64  'to 64'
              243  POP_BLOCK        
            244_0  COME_FROM_LOOP       54  '54'

 L. 146       244  LOAD_FAST                'num_tests'
              247  LOAD_DEREF               'errors'
              250  LOAD_FAST                'exit_value'
              253  BUILD_TUPLE_3         3 
              256  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 24


def format_final_result_for_valid_suite--- This code section failed: ---

 L. 156         0  LOAD_GLOBAL              _RelPathPresenter
                3  LOAD_FAST                'relativity_root_abs_path'
                6  CALL_FUNCTION_1       1  '1 positional, 0 named'
                9  STORE_DEREF              'path_presenter'

 L. 158        12  LOAD_GLOBAL              str
               15  LOAD_CONST               ('return',)
               18  LOAD_CLOSURE             'elapsed_time'
               21  LOAD_CLOSURE             'num_cases'
               24  BUILD_TUPLE_2         2 
               27  LOAD_CODE                <code_object num_tests_line>
               30  LOAD_STR                 'format_final_result_for_valid_suite.<locals>.num_tests_line'
               33  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               39  STORE_FAST               'num_tests_line'

 L. 166        42  LOAD_GLOBAL              List
               45  LOAD_GLOBAL              str
               48  BINARY_SUBSCR    
               49  LOAD_CONST               ('return',)
               52  LOAD_CLOSURE             'errors'
               55  BUILD_TUPLE_1         1 
               58  LOAD_CODE                <code_object num_unsuccessful_lines>
               61  LOAD_STR                 'format_final_result_for_valid_suite.<locals>.num_unsuccessful_lines'
               64  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               70  STORE_FAST               'num_unsuccessful_lines'

 L. 175        73  LOAD_GLOBAL              List
               76  LOAD_GLOBAL              str
               79  BINARY_SUBSCR    
               80  LOAD_CONST               ('return',)
               83  LOAD_CLOSURE             'errors'
               86  LOAD_CLOSURE             'path_presenter'
               89  BUILD_TUPLE_2         2 
               92  LOAD_CODE                <code_object error_lines>
               95  LOAD_STR                 'format_final_result_for_valid_suite.<locals>.error_lines'
               98  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
              104  STORE_FAST               'error_lines'

 L. 184       107  LOAD_FAST                'num_tests_line'
              110  CALL_FUNCTION_0       0  '0 positional, 0 named'
              113  BUILD_LIST_1          1 
              116  STORE_FAST               'ret_val'

 L. 185       119  LOAD_FAST                'ret_val'
              122  LOAD_FAST                'num_unsuccessful_lines'
              125  CALL_FUNCTION_0       0  '0 positional, 0 named'
              128  INPLACE_ADD      
              129  STORE_FAST               'ret_val'

 L. 186       132  LOAD_DEREF               'errors'
              135  POP_JUMP_IF_FALSE   164  'to 164'

 L. 187       138  LOAD_FAST                'ret_val'
              141  LOAD_ATTR                append
              144  LOAD_STR                 ''
              147  CALL_FUNCTION_1       1  '1 positional, 0 named'
              150  POP_TOP          

 L. 188       151  LOAD_FAST                'ret_val'
              154  LOAD_FAST                'error_lines'
              157  CALL_FUNCTION_0       0  '0 positional, 0 named'
              160  INPLACE_ADD      
              161  STORE_FAST               'ret_val'
            164_0  COME_FROM           135  '135'

 L. 189       164  LOAD_FAST                'ret_val'
              167  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CODE' instruction at offset 27


_NUMBER_OF_TESTS = name.NumberOfItemsString(name.name_with_plural_s('test'))
_NUMBER_OF_ERRORS = name.NumberOfItemsString(name.name_with_plural_s('error'))