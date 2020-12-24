# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_suite/instruction_set/sections/configuration/instruction_definition.py
# Compiled at: 2018-09-15 16:09:36
# Size of source mod 2**32: 1141 bytes
from exactly_lib.processing.act_phase import ActPhaseSetup
from exactly_lib.processing.test_case_processing import Preprocessor
from exactly_lib.test_suite.instruction_set.instruction import TestSuiteInstruction

class ConfigurationSectionEnvironment:

    def __init__(self, initial_preprocessor: Preprocessor, initial_act_phase_setup: ActPhaseSetup):
        self._preprocessor = initial_preprocessor
        self._act_phase_setup = initial_act_phase_setup

    @property
    def preprocessor(self) -> Preprocessor:
        return self._preprocessor

    @preprocessor.setter
    def preprocessor(self, value: Preprocessor):
        self._preprocessor = value

    @property
    def act_phase_setup(self) -> ActPhaseSetup:
        return self._act_phase_setup

    @act_phase_setup.setter
    def act_phase_setup(self, value: ActPhaseSetup):
        self._act_phase_setup = value


class ConfigurationSectionInstruction(TestSuiteInstruction):

    def execute(self, environment: ConfigurationSectionEnvironment):
        """
        Updates the environment.
        """
        raise NotImplementedError()