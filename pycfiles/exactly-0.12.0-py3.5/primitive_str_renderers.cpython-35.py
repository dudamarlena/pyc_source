# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/data/impl/path/primitive_str_renderers.py
# Compiled at: 2019-12-27 10:07:32
# Size of source mod 2**32: 236 bytes
from pathlib import Path
from exactly_lib.util.render.renderer import Renderer

class Constant(Renderer[str]):

    def __init__(self, path: Path):
        self._path = path

    def render(self) -> str:
        return str(self._path)