# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/multi_phase/utils/assert_phase_info.py
# Compiled at: 2017-11-25 19:14:01
# Size of source mod 2**32: 447 bytes
from exactly_lib.test_case.phases.assert_ import WithAssertPhasePurpose, AssertPhasePurpose

class IsAHelperIfInAssertPhase(WithAssertPhasePurpose):

    @property
    def assert_phase_purpose(self) -> AssertPhasePurpose:
        return AssertPhasePurpose.HELPER


class IsBothAssertionAndHelperIfInAssertPhase(WithAssertPhasePurpose):

    @property
    def assert_phase_purpose(self) -> AssertPhasePurpose:
        return AssertPhasePurpose.BOTH