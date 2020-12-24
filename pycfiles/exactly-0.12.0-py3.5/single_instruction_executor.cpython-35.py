# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/execution/impl/single_instruction_executor.py
# Compiled at: 2019-12-27 10:07:31
# Size of source mod 2**32: 4254 bytes
from enum import Enum
from typing import Optional
from exactly_lib.common.report_rendering.text_doc import TextRenderer
from exactly_lib.execution.result import ExecutionFailureStatus
from exactly_lib.section_document.model import SectionContentElement, InstructionInfo
from exactly_lib.section_document.source_location import SourceLocationPath
from exactly_lib.test_case.phases.common import TestCaseInstruction
from exactly_lib.test_case.result import failure_details
from exactly_lib.test_case.result.failure_details import FailureDetails

class PartialControlledFailureEnum(Enum):
    __doc__ = '\n    Implementation notes: integer values must correspond to PartialExeResultStatus\n\n    "controlled" means that implementation errors are not handled.\n    '
    VALIDATION_ERROR = 1
    FAIL = 2
    HARD_ERROR = 99


class PartialInstructionControlledFailureInfo(tuple):
    __doc__ = '\n    "controlled" means that implementation errors are not handled.\n    '

    def __new__(cls, status: PartialControlledFailureEnum, error_message: TextRenderer):
        return tuple.__new__(cls, (status,
         error_message))

    @property
    def status(self) -> PartialControlledFailureEnum:
        return self[0]

    @property
    def error_message(self) -> TextRenderer:
        return self[1]


class ControlledInstructionExecutor:
    __doc__ = '\n    Capable of executes a single step of any instruction of a single type.\n    The object knows which method of the instruction to invoke, and also\n    the arguments to pass.\n    It is able to execute many instructions with the same arguments.\n\n    The result is translated to a form that is can handle all the\n     return types used by instructions.\n\n    Does not handle implementation errors (since these can be handled uniformly\n     by the user of this class).\n\n    "Controlled" means that implementation errors are not handled - i.e., it only handles flow\n    that can be considered "controlled".\n    '

    def apply(self, instruction: TestCaseInstruction) -> PartialInstructionControlledFailureInfo:
        """
        :return: None if the execution was successful.
        """
        raise NotImplementedError()


class SingleInstructionExecutionFailure(tuple):
    __doc__ = '\n    Information about a failure of the execution of a single instruction.\n    '

    def __new__(cls, status: ExecutionFailureStatus, source_location: SourceLocationPath, details: failure_details.FailureDetails):
        return tuple.__new__(cls, (status,
         source_location,
         details))

    @property
    def status(self) -> ExecutionFailureStatus:
        """
        :return: Never PartialExeResultStatus.PASS
        """
        return self[0]

    @property
    def source_location_path(self) -> SourceLocationPath:
        return self[1]

    @property
    def failure_details(self) -> failure_details.FailureDetails:
        return self[2]


def execute_element(executor: ControlledInstructionExecutor, element: SectionContentElement, instruction_info: InstructionInfo) -> Optional[SingleInstructionExecutionFailure]:
    """
    :param element: Must be an instruction (i.e., element.is_instruction is True)
    :return: If None, then the execution was successful.
    """
    try:
        instruction = instruction_info.instruction
        assert isinstance(instruction, TestCaseInstruction), _INSTRUCTION_TYPE_ERROR_MESSAGE
        fail_info = executor.apply(instruction)
        if fail_info is None:
            return
        else:
            return SingleInstructionExecutionFailure(ExecutionFailureStatus(fail_info.status.value), element.source_location_info.source_location_path, FailureDetails.new_message(fail_info.error_message))
    except Exception as ex:
        return SingleInstructionExecutionFailure(ExecutionFailureStatus.IMPLEMENTATION_ERROR, element.source_location_info.source_location_path, FailureDetails.new_exception(ex))


_INSTRUCTION_TYPE_ERROR_MESSAGE = 'Instruction in test-case must be ' + str(TestCaseInstruction)