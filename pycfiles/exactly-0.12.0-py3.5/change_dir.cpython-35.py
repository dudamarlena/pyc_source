# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/setup/change_dir.py
# Compiled at: 2018-05-11 19:04:38
# Size of source mod 2**32: 607 bytes
from exactly_lib.common.instruction_setup import SingleInstructionSetup
from exactly_lib.instructions.multi_phase import change_dir as cd_utils
from exactly_lib.instructions.setup.utils import instruction_from_parts

def setup(instruction_name: str) -> SingleInstructionSetup:
    return SingleInstructionSetup(instruction_from_parts.Parser(cd_utils.parts_parser(is_after_act_phase=False)), cd_utils.TheInstructionDocumentation(instruction_name, is_after_act_phase=False, is_in_assert_phase=False))