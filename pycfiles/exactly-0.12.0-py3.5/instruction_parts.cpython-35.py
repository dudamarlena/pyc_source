# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/multi_phase/utils/instruction_parts.py
# Compiled at: 2019-12-27 10:07:42
# Size of source mod 2**32: 2519 bytes
"""
Utilities to help constructing an instruction for a specific phase, from phase-independent parts.
"""
from exactly_lib.section_document.parse_source import ParseSource
from exactly_lib.section_document.source_location import FileSystemLocationInfo
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPostSdsStep, PhaseLoggingPaths
from exactly_lib.test_case.result import pfh, sh
from exactly_lib.test_case.validation.sdv_validation import SdvValidator

class MainStepExecutor:
    __doc__ = '\n    Executes the main step of an instruction in any phase.\n    '

    def apply_as_non_assertion(self, environment: InstructionEnvironmentForPostSdsStep, logging_paths: PhaseLoggingPaths, os_services: OsServices) -> sh.SuccessOrHardError:
        """
        Invokes the execution as part of an instruction that is not in the assert phase.
        """
        raise NotImplementedError()

    def apply_as_assertion(self, environment: InstructionEnvironmentForPostSdsStep, logging_paths: PhaseLoggingPaths, os_services: OsServices) -> pfh.PassOrFailOrHardError:
        """
        Invokes the execution as part of an instruction that is in the assert phase.
        """
        raise NotImplementedError()


class InstructionParts(tuple):
    __doc__ = '\n    Parts needed for constructing an instruction that uses a MainStepExecutor.\n\n    This class is designed to be used by phase-specific code that constructs\n    an instruction for the specific phase,\n    given the information in this class.\n    '

    def __new__(cls, validator: SdvValidator, executor: MainStepExecutor, symbol_usages: tuple=()):
        return tuple.__new__(cls, (validator, executor, list(symbol_usages)))

    @property
    def validator(self) -> SdvValidator:
        return self[0]

    @property
    def executor(self) -> MainStepExecutor:
        return self[1]

    @property
    def symbol_usages(self) -> list:
        return self[2]


class InstructionPartsParser:
    __doc__ = '\n    Parser of `InstructionParts` - used by instructions that may be used in multiple phases. \n    '

    def parse(self, fs_location_info: FileSystemLocationInfo, source: ParseSource) -> InstructionParts:
        raise NotImplementedError()