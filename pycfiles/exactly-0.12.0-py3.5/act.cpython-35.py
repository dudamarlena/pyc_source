# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/phases/act.py
# Compiled at: 2016-12-07 11:34:17
# Size of source mod 2**32: 476 bytes
from exactly_lib.test_case import phase_identifier
from exactly_lib.test_case.phases.common import TestCaseInstruction
from exactly_lib.util.line_source import LineSequence

class ActPhaseInstruction(TestCaseInstruction):
    __doc__ = '\n    Abstract base class for instructions of the ACT phase.\n    '

    @property
    def phase(self) -> phase_identifier.Phase:
        return phase_identifier.ACT

    def source_code(self) -> LineSequence:
        raise NotImplementedError()