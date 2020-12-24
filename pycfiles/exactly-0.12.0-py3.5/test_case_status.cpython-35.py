# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/test_case_status.py
# Compiled at: 2018-07-07 05:02:31
# Size of source mod 2**32: 305 bytes
from enum import Enum

class TestCaseStatus(Enum):
    PASS = 0
    SKIP = 1
    FAIL = 2


NAME_PASS = 'PASS'
NAME_SKIP = 'SKIP'
NAME_FAIL = 'FAIL'
NAME_2_STATUS = {NAME_PASS: TestCaseStatus.PASS, 
 NAME_SKIP: TestCaseStatus.SKIP, 
 NAME_FAIL: TestCaseStatus.FAIL}
NAME_DEFAULT = NAME_PASS