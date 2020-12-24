# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/interactive_judger/judge_result.py
# Compiled at: 2018-08-02 08:40:23
# Size of source mod 2**32: 202 bytes
from enum import Enum

class Result(Enum):
    AC = 'Accepted'
    WA = 'Wrong Answer'
    TLE = 'Time Limit Exceeded'
    RE = 'Runtime Error'
    PE = 'Presentation Error'
    JE = 'Judgement Error'