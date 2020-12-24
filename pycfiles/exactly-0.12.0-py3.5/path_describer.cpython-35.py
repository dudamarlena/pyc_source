# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/data/path_describer.py
# Compiled at: 2019-12-27 10:07:40
# Size of source mod 2**32: 658 bytes
from abc import abstractmethod
from typing import Optional
from exactly_lib.test_case_file_structure.path_relativity import DirectoryStructurePartition
from exactly_lib.util.render.renderer import Renderer

class PathDescriberForDdv:

    @property
    @abstractmethod
    def value(self) -> Renderer[str]:
        pass

    @property
    @abstractmethod
    def resolving_dependency(self) -> Optional[DirectoryStructurePartition]:
        """
        :return: None iff path is absolute
        """
        pass


class PathDescriberForPrimitive(PathDescriberForDdv):

    @property
    @abstractmethod
    def primitive(self) -> Renderer[str]:
        pass