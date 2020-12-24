# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/executable_factory.py
# Compiled at: 2019-12-27 10:07:48
# Size of source mod 2**32: 293 bytes
from exactly_lib.type_system.logic.program.process_execution.command import Command
from exactly_lib.util.process_execution.execution_elements import Executable

class ExecutableFactory:

    def make(self, command: Command) -> Executable:
        raise NotImplementedError('abstract method')