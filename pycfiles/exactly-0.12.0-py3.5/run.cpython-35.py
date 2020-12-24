# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/setup/run.py
# Compiled at: 2019-05-02 06:35:46
# Size of source mod 2**32: 615 bytes
from exactly_lib.common.instruction_setup import SingleInstructionSetup
from exactly_lib.instructions.multi_phase import run
from exactly_lib.instructions.setup.utils import instruction_from_parts

def setup(instruction_name: str) -> SingleInstructionSetup:
    return SingleInstructionSetup(instruction_from_parts.Parser(run.parts_parser(instruction_name)), run.TheInstructionDocumentation(instruction_name, run.NON_ASSERT_PHASE_SINGLE_LINE_DESCRIPTION, description_rest_text=run.NON_ASSERT_PHASE_DESCRIPTION_REST))