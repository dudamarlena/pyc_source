# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/phases/setup.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 3139 bytes
import pathlib
from typing import Optional, Sequence
from exactly_lib.symbol.symbol_usage import SymbolUsage
from exactly_lib.test_case import phase_identifier
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPreSdsStep, InstructionEnvironmentForPostSdsStep, TestCaseInstructionWithSymbols
from exactly_lib.test_case.result import sh, svh

class StdinConfiguration:

    def __init__(self, file_name: Optional[pathlib.Path], string_contents: Optional[str]):
        self._StdinConfiguration__file_name = file_name
        self._StdinConfiguration__string_contents = string_contents

    @property
    def string_contents(self) -> str:
        return self._StdinConfiguration__string_contents

    @property
    def file_name(self) -> pathlib.Path:
        return self._StdinConfiguration__file_name

    @property
    def has_custom_stdin(self) -> bool:
        return self._StdinConfiguration__file_name is not None or self._StdinConfiguration__string_contents is not None


class StdinSettingsBuilder:

    def __init__(self):
        self._StdinSettingsBuilder__stdin_file_name = None
        self._StdinSettingsBuilder__stdin_contents = None

    @property
    def as_stdin_configuration(self) -> StdinConfiguration:
        return StdinConfiguration(self._StdinSettingsBuilder__stdin_file_name, self._StdinSettingsBuilder__stdin_contents)

    def set_empty(self):
        self._StdinSettingsBuilder__stdin_file_name = None
        self._StdinSettingsBuilder__stdin_contents = None

    @property
    def contents(self) -> str:
        return self._StdinSettingsBuilder__stdin_contents

    @contents.setter
    def contents(self, x: str):
        self._StdinSettingsBuilder__stdin_file_name = None
        self._StdinSettingsBuilder__stdin_contents = x

    @property
    def file_name(self) -> pathlib.Path:
        return self._StdinSettingsBuilder__stdin_file_name

    @file_name.setter
    def file_name(self, x: pathlib.Path):
        self._StdinSettingsBuilder__stdin_contents = None
        self._StdinSettingsBuilder__stdin_file_name = x


class SetupSettingsBuilder:

    def __init__(self):
        self._SetupSettingsBuilder__stdin_settings = StdinSettingsBuilder()

    @property
    def stdin(self) -> StdinSettingsBuilder:
        return self._SetupSettingsBuilder__stdin_settings


def default_settings() -> SetupSettingsBuilder:
    return SetupSettingsBuilder()


class SetupPhaseInstruction(TestCaseInstructionWithSymbols):
    __doc__ = '\n    Abstract base class for instructions of the SETUP phase.\n    '

    @property
    def phase(self) -> phase_identifier.Phase:
        return phase_identifier.SETUP

    def validate_pre_sds(self, environment: InstructionEnvironmentForPreSdsStep) -> svh.SuccessOrValidationErrorOrHardError:
        return svh.new_svh_success()

    def validate_post_setup(self, environment: InstructionEnvironmentForPostSdsStep) -> svh.SuccessOrValidationErrorOrHardError:
        return svh.new_svh_success()

    def main(self, environment: InstructionEnvironmentForPostSdsStep, os_services: OsServices, settings_builder: SetupSettingsBuilder) -> sh.SuccessOrHardError:
        return sh.new_sh_success()


def get_symbol_usages(instruction: SetupPhaseInstruction) -> Sequence[SymbolUsage]:
    return instruction.symbol_usages()