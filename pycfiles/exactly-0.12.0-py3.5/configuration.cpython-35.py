# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/phases/configuration.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 2660 bytes
import pathlib
from typing import Optional
from exactly_lib.test_case import phase_identifier
from exactly_lib.test_case.actor import Actor
from exactly_lib.test_case.phases.common import TestCaseInstruction
from exactly_lib.test_case.result.sh import SuccessOrHardError
from exactly_lib.test_case.test_case_status import TestCaseStatus
from exactly_lib.test_case_file_structure.home_directory_structure import HomeDirectoryStructure
from exactly_lib.test_case_file_structure.path_relativity import RelHdsOptionType

class ConfigurationBuilder:

    def __init__(self, home_case_dir_path: pathlib.Path, home_act_dir_path: pathlib.Path, actor: Actor, timeout_in_seconds: Optional[int]=None,
                 test_case_status: TestCaseStatus=TestCaseStatus.PASS):
        self._ConfigurationBuilder__actor = actor
        self._ConfigurationBuilder__test_case_status = test_case_status
        self._ConfigurationBuilder__timeout_in_seconds = timeout_in_seconds
        self._ConfigurationBuilder__hds_dirs = {RelHdsOptionType.REL_HDS_CASE: home_case_dir_path, 
         RelHdsOptionType.REL_HDS_ACT: home_act_dir_path}

    @property
    def test_case_status(self) -> TestCaseStatus:
        return self._ConfigurationBuilder__test_case_status

    def set_test_case_status(self, x: TestCaseStatus):
        self._ConfigurationBuilder__test_case_status = x

    def set_hds_dir(self, d: RelHdsOptionType, value: pathlib.Path):
        self._ConfigurationBuilder__hds_dirs[d] = value

    def get_hds_dir(self, d: RelHdsOptionType) -> pathlib.Path:
        return self._ConfigurationBuilder__hds_dirs[d]

    @property
    def hds(self) -> HomeDirectoryStructure:
        return HomeDirectoryStructure(case_dir=self._ConfigurationBuilder__hds_dirs[RelHdsOptionType.REL_HDS_CASE], act_dir=self._ConfigurationBuilder__hds_dirs[RelHdsOptionType.REL_HDS_ACT])

    @property
    def actor(self) -> Actor:
        return self._ConfigurationBuilder__actor

    def set_actor(self, x: Actor):
        self._ConfigurationBuilder__actor = x

    @property
    def timeout_in_seconds(self) -> int:
        """
        :return: None if no timeout
        """
        return self._ConfigurationBuilder__timeout_in_seconds

    def set_timeout_in_seconds(self, num_seconds: int):
        self._ConfigurationBuilder__timeout_in_seconds = num_seconds


class ConfigurationPhaseInstruction(TestCaseInstruction):
    __doc__ = '\n    Abstract base class for instructions of the configuration phase.\n    '

    @property
    def phase(self) -> phase_identifier.Phase:
        return phase_identifier.CONFIGURATION

    def main(self, configuration_builder: ConfigurationBuilder) -> SuccessOrHardError:
        """
        :param configuration_builder Collects the settings set by the instruction.
        """
        raise NotImplementedError()