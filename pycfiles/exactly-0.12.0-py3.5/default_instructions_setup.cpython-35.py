# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/default/program_modes/test_case/default_instructions_setup.py
# Compiled at: 2016-12-07 11:34:17
# Size of source mod 2**32: 399 bytes
from exactly_lib.default.program_modes.test_case.phases import assert_, before_assert, cleanup, configuration, setup
from exactly_lib.processing.instruction_setup import InstructionsSetup
INSTRUCTIONS_SETUP = InstructionsSetup(configuration.INSTRUCTIONS, setup.INSTRUCTIONS, before_assert.INSTRUCTIONS, assert_.INSTRUCTIONS, cleanup.INSTRUCTIONS)