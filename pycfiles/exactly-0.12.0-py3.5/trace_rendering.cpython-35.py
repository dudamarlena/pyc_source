# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/line_matcher/trace_rendering.py
# Compiled at: 2019-12-27 10:07:28
# Size of source mod 2**32: 743 bytes
from typing import Sequence
from exactly_lib.type_system.logic.line_matcher import LineMatcherLine
from exactly_lib.util import strings
from exactly_lib.util.description_tree import tree
from exactly_lib.util.description_tree.renderer import DetailsRenderer
from exactly_lib.util.description_tree.tree import Detail

class LineMatcherLineRenderer(DetailsRenderer):

    def __init__(self, line: LineMatcherLine):
        self._line = line

    def render(self) -> Sequence[Detail]:
        line = self._line
        return [
         tree.StringDetail(strings.FormatPositional('Line {}. {}', line[0], repr(line[1])))]