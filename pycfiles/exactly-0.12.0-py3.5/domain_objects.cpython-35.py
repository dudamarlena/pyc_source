# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/err_msg/msg/domain_objects.py
# Compiled at: 2019-12-27 10:07:32
# Size of source mod 2**32: 596 bytes
import pathlib
from exactly_lib.util.render import combinators as rend_comb
from exactly_lib.util.render.renderer import Renderer, SequenceRenderer
from exactly_lib.util.simple_textstruct.rendering import line_objects, component_renderers as comp_rend
from exactly_lib.util.simple_textstruct.structure import LineElement

def of_path(path: pathlib.Path) -> Renderer[LineElement]:
    return comp_rend.LineElementR(line_objects.PreFormattedString(path))


def single_path(path: pathlib.Path) -> SequenceRenderer[LineElement]:
    return rend_comb.SingletonSequenceR(of_path(path))