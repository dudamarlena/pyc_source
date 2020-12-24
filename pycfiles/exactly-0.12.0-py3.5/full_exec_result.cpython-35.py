# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/report_rendering/parts/full_exec_result.py
# Compiled at: 2019-12-27 10:07:32
# Size of source mod 2**32: 961 bytes
from typing import Sequence
from exactly_lib.common.report_rendering.parts import failure_info
from exactly_lib.execution.full_execution.result import FullExeResult
from exactly_lib.util.render import combinators as rend_comb
from exactly_lib.util.render.renderer import SequenceRenderer
from exactly_lib.util.simple_textstruct.rendering.components import MajorBlocksRenderer
from exactly_lib.util.simple_textstruct.structure import MajorBlock

class FullExeResultRenderer(MajorBlocksRenderer):
    _EMPTY = rend_comb.ConstantSequenceR([])

    def __init__(self, full_result: FullExeResult):
        self._result = full_result

    def render_sequence(self) -> Sequence[MajorBlock]:
        return self._renderer().render_sequence()

    def _renderer(self) -> SequenceRenderer[MajorBlock]:
        if self._result.is_failure:
            return failure_info.FailureInfoRenderer(self._result.failure_info)
        return self._EMPTY