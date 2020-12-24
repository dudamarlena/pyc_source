# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/execution/result.py
# Compiled at: 2019-12-27 10:07:31
# Size of source mod 2**32: 2331 bytes
from enum import Enum
from typing import Optional
from exactly_lib.execution.failure_info import FailureInfo
from exactly_lib.test_case_file_structure.sandbox_directory_structure import SandboxDirectoryStructure

class ExecutionFailureStatus(Enum):
    __doc__ = '\n    Implementation notes: integer values must correspond to FullExeResultStatus\n    '
    VALIDATION_ERROR = 1
    FAIL = 2
    HARD_ERROR = 99
    IMPLEMENTATION_ERROR = 100


class ActionToCheckOutcome(tuple):

    def __new__(cls, exit_code: int):
        return tuple.__new__(cls, (exit_code,))

    @property
    def exit_code(self) -> int:
        return self[0]


class ResultBase:

    def __init__(self, sds: Optional[SandboxDirectoryStructure], action_to_check_outcome: Optional[ActionToCheckOutcome], failure_info: Optional[FailureInfo]):
        self._ResultBase__sds = sds
        self._ResultBase__action_to_check_outcome = action_to_check_outcome
        self._ResultBase__failure_info = failure_info

    @property
    def has_sds(self) -> bool:
        return self._ResultBase__sds is not None

    @property
    def sds(self) -> Optional[SandboxDirectoryStructure]:
        return self._ResultBase__sds

    @property
    def has_action_to_check_outcome(self) -> bool:
        return self._ResultBase__action_to_check_outcome is not None

    @property
    def action_to_check_outcome(self) -> Optional[ActionToCheckOutcome]:
        """
        :return: Not None iff Action To Check has been completely executed
        """
        return self._ResultBase__action_to_check_outcome

    @property
    def is_failure(self) -> bool:
        return self._ResultBase__failure_info is not None

    @property
    def failure_info(self) -> Optional[FailureInfo]:
        return self._ResultBase__failure_info


class PhaseStepFailure:

    def __init__(self, status: ExecutionFailureStatus, failure_info: FailureInfo):
        """
        :param failure_info:
        """
        self._PhaseStepFailure__failure_info = failure_info
        self._PhaseStepFailure__status = status

    @property
    def status(self) -> ExecutionFailureStatus:
        return self._PhaseStepFailure__status

    @property
    def failure_info(self) -> FailureInfo:
        return self._PhaseStepFailure__failure_info


class PhaseStepFailureException(Exception):

    def __init__(self, failure: PhaseStepFailure):
        self.failure = failure