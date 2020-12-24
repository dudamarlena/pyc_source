# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/processing/standalone/settings.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 2193 bytes
import enum, pathlib
from typing import Optional
from exactly_lib import program_info
from exactly_lib.execution import sandbox_dir_resolving
from exactly_lib.execution.sandbox_dir_resolving import SandboxRootDirNameResolver
from exactly_lib.processing.test_case_handling_setup import TestCaseHandlingSetup

class ReportingOption(enum.Enum):
    STATUS_CODE = 1
    SANDBOX_DIRECTORY_STRUCTURE_ROOT = 2
    ACT_PHASE_OUTPUT = 3


class TestCaseExecutionSettings:
    __doc__ = 'Settings derived after parsing of command line arguments.'

    def __init__(self, test_case_file_path: pathlib.Path, initial_hds_dir_path: pathlib.Path, output: ReportingOption, handling_setup: TestCaseHandlingSetup, sandbox_root_dir_resolver: SandboxRootDirNameResolver=sandbox_dir_resolving.mk_tmp_dir_with_prefix(program_info.PROGRAM_NAME + '-'),
                 run_as_part_of_explicit_suite: Optional[pathlib.Path]=None):
        self._TestCaseExecutionSettings__test_case_file_path = test_case_file_path
        self._TestCaseExecutionSettings__initial_hds_dir_path = initial_hds_dir_path
        self._TestCaseExecutionSettings__output = output
        self._TestCaseExecutionSettings__handling_setup = handling_setup
        self._TestCaseExecutionSettings__sandbox_root_dir_resolver = sandbox_root_dir_resolver
        self._TestCaseExecutionSettings__run_as_part_of_explicit_suite = run_as_part_of_explicit_suite

    @property
    def test_case_file_path(self) -> pathlib.Path:
        return self._TestCaseExecutionSettings__test_case_file_path

    @property
    def initial_hds_dir_path(self) -> pathlib.Path:
        return self._TestCaseExecutionSettings__initial_hds_dir_path

    @property
    def reporting_option(self) -> ReportingOption:
        return self._TestCaseExecutionSettings__output

    @property
    def handling_setup(self) -> TestCaseHandlingSetup:
        return self._TestCaseExecutionSettings__handling_setup

    @property
    def sandbox_root_dir_resolver(self) -> SandboxRootDirNameResolver:
        return self._TestCaseExecutionSettings__sandbox_root_dir_resolver

    @property
    def run_as_part_of_explicit_suite(self) -> Optional[pathlib.Path]:
        """
        If not None, the the file must exist as a suite and the test case is run as part of this suite
        """
        return self._TestCaseExecutionSettings__run_as_part_of_explicit_suite