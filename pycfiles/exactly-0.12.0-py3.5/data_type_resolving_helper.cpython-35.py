# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/utils/data_type_resolving_helper.py
# Compiled at: 2019-12-27 10:07:48
# Size of source mod 2**32: 442 bytes
from exactly_lib.symbol.data.resolving_helper import DataTypeResolvingHelper
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPostSdsStep

def resolving_helper_for_instruction_env(environment: InstructionEnvironmentForPostSdsStep) -> DataTypeResolvingHelper:
    return DataTypeResolvingHelper(environment.symbols, environment.tcds, environment.application_environment.tmp_files_space)