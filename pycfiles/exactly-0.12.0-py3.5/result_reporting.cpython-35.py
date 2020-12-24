# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/processing/standalone/result_reporting.py
# Compiled at: 2019-12-27 10:07:30
# Size of source mod 2**32: 6887 bytes
from typing import Optional, Callable
from exactly_lib.common import process_result_reporter
from exactly_lib.common import result_reporting as reporting
from exactly_lib.common.exit_value import ExitValue
from exactly_lib.common.process_result_reporter import Environment, ProcessResultReporter
from exactly_lib.common.process_result_reporters import ProcessResultReporterWithInitialExitValueOutput
from exactly_lib.execution.full_execution.result import FullExeResultStatus, FullExeResult
from exactly_lib.processing import test_case_processing, exit_values
from exactly_lib.processing.standalone.settings import ReportingOption
from exactly_lib.processing.test_case_processing import ErrorInfo
from exactly_lib.test_suite.file_reading.exception import SuiteParseError
from exactly_lib.util.process_execution.process_output_files import ProcOutputFile
from exactly_lib.util.std import StdOutputFiles

class ResultReporter:
    __doc__ = 'Reports the result of the execution via exitcode, stdout, stderr.'

    def __init__(self, reporting_environment: process_result_reporter.Environment):
        self._reporting_environment = reporting_environment


class TestSuiteParseErrorReporter(ResultReporter):

    def report(self, ex: SuiteParseError) -> int:
        file_printers = self._reporting_environment.std_file_printers
        from exactly_lib.test_suite import error_reporting
        return error_reporting.report_suite_parse_error(ex, file_printers.out, file_printers.err)


class TestCaseResultReporter(ResultReporter):

    def report(self, result: test_case_processing.Result) -> int:
        exit_value = exit_values.from_result(result)
        if result.status is test_case_processing.Status.EXECUTED:
            return self._report_execution(exit_value, result.execution_result)
        else:
            return self._TestCaseResultReporter__report_unable_to_execute(exit_value, result.error_info)

    def depends_on_result_in_sandbox(self) -> bool:
        raise NotImplementedError('abstract method')

    def _exit_identifier_printer(self) -> ProcOutputFile:
        raise NotImplementedError('abstract method')

    def execute_atc_and_skip_assertions(self) -> Optional[StdOutputFiles]:
        pass

    def _process_reporter_with_exit_value_output(self, exit_value: ExitValue, output_rest: Callable[([Environment], None)]) -> ProcessResultReporter:
        return ProcessResultReporterWithInitialExitValueOutput(exit_value, self._exit_identifier_printer(), output_rest)

    def _report_with_exit_value_output(self, exit_value: ExitValue, output_rest: Callable[([Environment], None)]) -> int:
        reporter = self._process_reporter_with_exit_value_output(exit_value, output_rest)
        return reporter.report(self._reporting_environment)

    def _report_execution(self, exit_value: ExitValue, result: FullExeResult) -> int:
        raise NotImplementedError('abstract method')

    def _report_full_exe_result--- This code section failed: ---

 L.  74         0  LOAD_GLOBAL              Environment
                3  LOAD_CONST               ('reporting_environment',)
                6  LOAD_CLOSURE             'result'
                9  BUILD_TUPLE_1         1 
               12  LOAD_CODE                <code_object output_rest>
               15  LOAD_STR                 'TestCaseResultReporter._report_full_exe_result.<locals>.output_rest'
               18  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               24  STORE_FAST               'output_rest'

 L.  78        27  LOAD_FAST                'self'
               30  LOAD_ATTR                _report_with_exit_value_output
               33  LOAD_FAST                'exit_value'
               36  LOAD_FAST                'output_rest'
               39  CALL_FUNCTION_2       2  '2 positional, 0 named'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _TestCaseResultReporter__report_unable_to_execute(self, exit_value: ExitValue, error_info: ErrorInfo) -> int:
        reporter = reporter_of_unable_to_execute(self._exit_identifier_printer(), exit_value, error_info)
        return reporter.report(self._reporting_environment)


def reporter_of_unable_to_execute--- This code section failed: ---

 L.  96         0  LOAD_GLOBAL              Environment
                3  LOAD_CONST               ('reporting_environment',)
                6  LOAD_CLOSURE             'error_info'
                9  BUILD_TUPLE_1         1 
               12  LOAD_CODE                <code_object output_rest>
               15  LOAD_STR                 'reporter_of_unable_to_execute.<locals>.output_rest'
               18  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               24  STORE_FAST               'output_rest'

 L. 100        27  LOAD_GLOBAL              ProcessResultReporterWithInitialExitValueOutput

 L. 101        30  LOAD_FAST                'exit_value'

 L. 102        33  LOAD_FAST                'exit_value_printer'

 L. 103        36  LOAD_FAST                'output_rest'
               39  CALL_FUNCTION_3       3  '3 positional, 0 named'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


class _ResultReporterForNormalOutput(TestCaseResultReporter):

    def depends_on_result_in_sandbox(self) -> bool:
        return False

    def _exit_identifier_printer(self) -> ProcOutputFile:
        return ProcOutputFile.STDOUT

    def _report_execution(self, exit_value: ExitValue, result: FullExeResult) -> int:
        return self._report_full_exe_result(exit_value, result)


class _ResultReporterForPreserveAndPrintSandboxDir(TestCaseResultReporter):

    def depends_on_result_in_sandbox(self) -> bool:
        return True

    def _exit_identifier_printer(self) -> ProcOutputFile:
        return ProcOutputFile.STDERR

    def _report_execution(self, exit_value: ExitValue, result: FullExeResult) -> int:
        if result.has_sds:
            self._reporting_environment.std_file_printers.out.write_line(str(result.sds.root_dir))
        return self._report_full_exe_result(exit_value, result)


class _ResultReporterForActPhaseOutput(TestCaseResultReporter):

    def depends_on_result_in_sandbox(self) -> bool:
        return False

    def _exit_identifier_printer(self) -> ProcOutputFile:
        return ProcOutputFile.STDERR

    def execute_atc_and_skip_assertions(self) -> Optional[StdOutputFiles]:
        return self._reporting_environment.std_files

    def _report_execution(self, exit_value: ExitValue, result: FullExeResult) -> int:
        if result.status in _FULL_EXECUTION__COMPLETE:
            return result.action_to_check_outcome.exit_code
        return self._report_full_exe_result(exit_value, result)


RESULT_REPORTERS = {ReportingOption.STATUS_CODE: _ResultReporterForNormalOutput, 
 ReportingOption.SANDBOX_DIRECTORY_STRUCTURE_ROOT: _ResultReporterForPreserveAndPrintSandboxDir, 
 ReportingOption.ACT_PHASE_OUTPUT: _ResultReporterForActPhaseOutput}
_FULL_EXECUTION__COMPLETE = {
 FullExeResultStatus.PASS,
 FullExeResultStatus.FAIL,
 FullExeResultStatus.XPASS,
 FullExeResultStatus.XFAIL}