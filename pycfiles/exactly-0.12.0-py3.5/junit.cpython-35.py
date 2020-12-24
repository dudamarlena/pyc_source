# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_suite/reporters/junit.py
# Compiled at: 2019-12-27 10:07:29
# Size of source mod 2**32: 8892 bytes
import datetime, os, pathlib, platform
from xml.etree import ElementTree as ET
from exactly_lib.common.exit_value import ExitValue
from exactly_lib.common.process_result_reporter import Environment
from exactly_lib.common.result_reporting import error_message_for_full_result, error_message_for_error_info
from exactly_lib.execution.full_execution.result import FullExeResultStatus
from exactly_lib.processing.test_case_processing import Status, TestCaseFileReference, Result
from exactly_lib.test_suite import reporting, structure
from exactly_lib.test_suite.reporters import simple_progress_reporter as simple_reporter
from exactly_lib.test_suite.reporting import TestCaseProcessingInfo
from exactly_lib.util.file_printer import FilePrinter
from exactly_lib.util.std import StdOutputFiles
FAIL_STATUSES = {
 FullExeResultStatus.FAIL,
 FullExeResultStatus.XPASS}
ERROR_STATUSES = {
 FullExeResultStatus.VALIDATION_ERROR,
 FullExeResultStatus.HARD_ERROR,
 FullExeResultStatus.IMPLEMENTATION_ERROR}
NON_PASS_STATUSES = FAIL_STATUSES.union(ERROR_STATUSES)
UNCONDITIONAL_EXIT_CODE = 0
TEST_SUITE_ELEMENT_NAME = 'testsuite'
TEST_SUITES_ELEMENT_NAME = 'testsuites'

class JUnitRootSuiteProcessingReporter(reporting.RootSuiteProcessingReporter):

    def report_invalid_suite(self, exit_value: ExitValue, reporting_environment: Environment):
        pass

    def execution_reporter(self, root_suite: structure.TestSuiteHierarchy, reporting_environment: Environment, root_suite_file: pathlib.Path) -> reporting.RootSuiteReporter:
        root_suite_dir_abs_path = root_suite_file.resolve().parent
        return JUnitRootSuiteReporter(root_suite, reporting_environment.std_files, root_suite_dir_abs_path)


class JUnitRootSuiteReporter(reporting.RootSuiteReporter):

    def __init__(self, root_suite: structure.TestSuiteHierarchy, std_output_files: StdOutputFiles, root_suite_dir_abs_path: pathlib.Path):
        self._root_suite = root_suite
        self._std_output_files = std_output_files
        self._output_file = FilePrinter(std_output_files.out)
        self._error_file = FilePrinter(std_output_files.err)
        self._sub_reporters = []
        self._start_time = None
        self._total_time_timedelta = None
        self._root_suite_dir_abs_path = root_suite_dir_abs_path
        self._host_name = platform.node()

    def root_suite_begin(self):
        self._start_time = datetime.datetime.now()

    def root_suite_end(self):
        stop_time = datetime.datetime.now()
        self._total_time_timedelta = stop_time - self._start_time

    def new_sub_suite_reporter(self, sub_suite: structure.TestSuiteHierarchy) -> reporting.SubSuiteReporter:
        progress_reporter = simple_reporter.SimpleProgressSubSuiteProgressReporter(self._error_file, sub_suite, self._root_suite_dir_abs_path)
        reporter = reporting.SubSuiteReporter(sub_suite, progress_reporter)
        self._sub_reporters.append(reporter)
        return reporter

    def report_final_results(self) -> int:
        if len(self._sub_reporters) == 1:
            reporter = self._sub_reporters[0]
            xml = ET.ElementTree(self._xml_for_suite(reporter, self._file_path_pres(reporter.suite.source_file)))
        else:
            xml = ET.ElementTree(self._xml_for_suites(self._root_suite, self._sub_reporters))
        xml.write(self._std_output_files.out, encoding='unicode', xml_declaration=True, short_empty_elements=True)
        self._std_output_files.out.write(os.linesep)
        return UNCONDITIONAL_EXIT_CODE

    def _xml_for_suites--- This code section failed: ---

 L.  97         0  LOAD_GLOBAL              reporting
                3  LOAD_ATTR                SubSuiteReporter
                6  LOAD_GLOBAL              bool
                9  LOAD_CONST               ('reporter', 'return')
               12  LOAD_CLOSURE             'root_suite'
               15  BUILD_TUPLE_1         1 
               18  LOAD_CODE                <code_object is_root_suite_and_should_skip_root_suite>
               21  LOAD_STR                 'JUnitRootSuiteReporter._xml_for_suites.<locals>.is_root_suite_and_should_skip_root_suite'
               24  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               30  STORE_FAST               'is_root_suite_and_should_skip_root_suite'

 L. 100        33  LOAD_GLOBAL              ET
               36  LOAD_ATTR                Element
               39  LOAD_GLOBAL              TEST_SUITES_ELEMENT_NAME
               42  CALL_FUNCTION_1       1  '1 positional, 0 named'
               45  STORE_FAST               'root'

 L. 101        48  LOAD_CONST               1
               51  STORE_FAST               'next_suite_id'

 L. 102        54  SETUP_LOOP          164  'to 164'
               57  LOAD_FAST                'suite_reporters'
               60  GET_ITER         
               61  FOR_ITER            163  'to 163'
               64  STORE_FAST               'suite_reporter'

 L. 103        67  LOAD_FAST                'is_root_suite_and_should_skip_root_suite'
               70  LOAD_FAST                'suite_reporter'
               73  CALL_FUNCTION_1       1  '1 positional, 0 named'
               76  UNARY_NOT        
               77  POP_JUMP_IF_FALSE   160  'to 160'

 L. 104        80  LOAD_FAST                'self'
               83  LOAD_ATTR                _package_and_name
               86  LOAD_FAST                'suite_reporter'
               89  LOAD_ATTR                suite
               92  CALL_FUNCTION_1       1  '1 positional, 0 named'
               95  UNPACK_SEQUENCE_2     2 
               98  STORE_FAST               'package_name'
              101  STORE_FAST               'name'

 L. 105       104  LOAD_FAST                'root'
              107  LOAD_ATTR                append
              110  LOAD_FAST                'self'
              113  LOAD_ATTR                _xml_for_suite
              116  LOAD_FAST                'suite_reporter'
              119  LOAD_FAST                'name'

 L. 106       122  LOAD_STR                 'id'
              125  LOAD_GLOBAL              str
              128  LOAD_FAST                'next_suite_id'
              131  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L. 107       134  LOAD_STR                 'package'
              137  LOAD_FAST                'package_name'
              140  BUILD_MAP_2           2 
              143  CALL_FUNCTION_3       3  '3 positional, 0 named'
              146  CALL_FUNCTION_1       1  '1 positional, 0 named'
              149  POP_TOP          

 L. 109       150  LOAD_FAST                'next_suite_id'
              153  LOAD_CONST               1
              156  INPLACE_ADD      
              157  STORE_FAST               'next_suite_id'
            160_0  COME_FROM            77  '77'
              160  JUMP_BACK            61  'to 61'
              163  POP_BLOCK        
            164_0  COME_FROM_LOOP       54  '54'

 L. 110       164  LOAD_FAST                'root'
              167  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _xml_for_suite(self, suite_reporter: reporting.SubSuiteReporter, name: str, additional_attributes: dict=None) -> ET.Element:
        timestamp = suite_reporter.start_time.replace(microsecond=0)
        attributes = {'name': name, 
         'tests': str(len(suite_reporter.result())), 
         'timestamp': timestamp.isoformat(), 
         'hostname': self._host_name}
        if additional_attributes:
            attributes.update(additional_attributes)
        root = ET.Element(TEST_SUITE_ELEMENT_NAME, attributes)
        ET.SubElement(root, 'properties')
        num_errors = 0
        num_failures = 0
        sum_of_time_for_cases = datetime.timedelta()
        for test_case_setup, processing_info in suite_reporter.result():
            sum_of_time_for_cases += processing_info.duration
            result = processing_info.result
            root.append(self._xml_for_case(test_case_setup, processing_info))
            if result.status != Status.EXECUTED:
                num_errors += 1
            else:
                if result.execution_result.status in FAIL_STATUSES:
                    num_failures += 1
                elif result.execution_result.status in ERROR_STATUSES:
                    num_errors += 1

        root.set('failures', str(num_failures))
        root.set('errors', str(num_errors))
        root.set('time', _time_attribute_string(sum_of_time_for_cases))
        root.append(ET.Element('system-out'))
        root.append(ET.Element('system-err'))
        return root

    def _xml_for_case(self, test_case_reference: TestCaseFileReference, processing_info: TestCaseProcessingInfo) -> ET.Element:
        name = self._file_path_pres(test_case_reference.file_path)
        ret_val = ET.Element('testcase', {'name': name, 
         'classname': name, 
         'time': _time_attribute_string(processing_info.duration)})
        result = processing_info.result
        if result.status != Status.EXECUTED or result.execution_result.status in ERROR_STATUSES:
            ret_val.append(_xml_for_error(result))
        elif result.execution_result.status in FAIL_STATUSES:
            ret_val.append(_xml_for_failure(result))
        return ret_val

    def _file_path_pres(self, file: pathlib.Path):
        try:
            return str(file.relative_to(self._root_suite_dir_abs_path))
        except ValueError:
            return str(file)

    def _package_and_name(self, suite: structure.TestSuiteHierarchy):
        try:
            relative_path = suite.source_file.relative_to(self._root_suite_dir_abs_path)
            if relative_path.parts:
                return (str(relative_path.parent), relative_path.name)
            else:
                return (
                 '.', str(relative_path))
        except ValueError:
            return (
             '.', str(suite.source_file))


def _xml_for_failure(result: Result) -> ET.Element:
    ret_val = ET.Element('failure', {'type': _error_type(result)})
    ret_val.text = _error_message_for(result)
    return ret_val


def _xml_for_error(result: Result) -> ET.Element:
    ret_val = ET.Element('error', {'type': _error_type(result)})
    ret_val.text = _error_message_for(result)
    return ret_val


def _error_message_for(result: Result) -> str:
    if result.status != Status.EXECUTED:
        return error_message_for_error_info(result.error_info)
    else:
        return error_message_for_full_result(result.execution_result)


def _error_type(result: Result) -> str:
    if result.status is Status.INTERNAL_ERROR:
        return Status.INTERNAL_ERROR.name
    else:
        if result.status is Status.ACCESS_ERROR:
            return result.access_error_type.name
        return result.execution_result.status.name


def _time_attribute_string(sum_of_time_for_cases: datetime.timedelta) -> str:
    return '%f' % sum_of_time_for_cases.total_seconds()