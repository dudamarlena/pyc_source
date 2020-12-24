# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/setup/env.py
# Compiled at: 2018-05-11 19:04:38
# Size of source mod 2**32: 453 bytes
from exactly_lib.common.instruction_setup import SingleInstructionSetup
from exactly_lib.instructions.multi_phase import env as env_instruction
from exactly_lib.instructions.setup.utils import instruction_from_parts

def setup(instruction_name: str) -> SingleInstructionSetup:
    return SingleInstructionSetup(instruction_from_parts.Parser(env_instruction.PARTS_PARSER), env_instruction.TheInstructionDocumentation(instruction_name))