# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/logic/line_matcher.py
# Compiled at: 2020-01-16 12:15:32
# Size of source mod 2**32: 558 bytes
from typing import Tuple
from exactly_lib.symbol.logic.matcher import MatcherSdv
from exactly_lib.type_system.logic.logic_base_class import ApplicationEnvironmentDependentValue
from exactly_lib.type_system.logic.matcher_base_class import MatcherWTraceAndNegation, MatcherDdv
LineMatcherLine = Tuple[(int, str)]
FIRST_LINE_NUMBER = 1
LineMatcher = MatcherWTraceAndNegation[LineMatcherLine]
LineMatcherAdv = ApplicationEnvironmentDependentValue[LineMatcher]
LineMatcherDdv = MatcherDdv[LineMatcherLine]
GenericLineMatcherSdv = MatcherSdv[LineMatcherLine]