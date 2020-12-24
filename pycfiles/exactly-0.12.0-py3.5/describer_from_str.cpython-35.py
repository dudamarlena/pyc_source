# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/data/impl/path/describer_from_str.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 1365 bytes
from typing import Optional, Callable
from exactly_lib.test_case_file_structure.path_relativity import DirectoryStructurePartition
from exactly_lib.type_system.data.path_describer import PathDescriberForDdv, PathDescriberForPrimitive
from exactly_lib.util.render.renderer import Renderer

class PathDescriberForDdvFromStr(PathDescriberForDdv):

    def __init__(self, value: Renderer[str], relativity: Callable[([], Optional[DirectoryStructurePartition])]):
        self._value = value
        self._relativity = relativity

    @property
    def value(self) -> Renderer[str]:
        return self._value

    @property
    def resolving_dependency(self) -> Optional[DirectoryStructurePartition]:
        return self._relativity()


class PathDescriberForPrimitiveFromStr(PathDescriberForPrimitive):

    def __init__(self, value: PathDescriberForDdv, primitive: Renderer[str]):
        self._value = value
        self._primitive = primitive

    @property
    def value(self) -> Renderer[str]:
        return self._value.value

    @property
    def resolving_dependency(self) -> Optional[DirectoryStructurePartition]:
        return self._value.resolving_dependency

    @property
    def primitive(self) -> Renderer[str]:
        return self._primitive