# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/data/impl/path/described_w_handler.py
# Compiled at: 2019-12-27 10:07:51
# Size of source mod 2**32: 2726 bytes
from abc import ABC, abstractmethod
from pathlib import Path
from exactly_lib.test_case_file_structure.home_directory_structure import HomeDirectoryStructure
from exactly_lib.test_case_file_structure.sandbox_directory_structure import SandboxDirectoryStructure
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.data.path_ddv import DescribedPath
from exactly_lib.type_system.data.path_describer import PathDescriberForDdv, PathDescriberForPrimitive

class PathDescriberHandlerForPrimitive(ABC):

    @property
    @abstractmethod
    def describer(self) -> PathDescriberForPrimitive:
        pass

    @abstractmethod
    def child(self, child_path: Path, child_path_component: str) -> 'PathDescriberHandlerForPrimitive':
        pass

    @abstractmethod
    def parent(self, parent_path: Path) -> 'PathDescriberHandlerForPrimitive':
        pass


class PathDescriberHandlerForDdv(ABC):

    @property
    @abstractmethod
    def describer(self) -> PathDescriberForDdv:
        pass

    @abstractmethod
    def value_when_no_dir_dependencies(self, primitive: Path) -> PathDescriberHandlerForPrimitive:
        pass

    @abstractmethod
    def value_pre_sds(self, primitive: Path, hds: HomeDirectoryStructure) -> PathDescriberHandlerForPrimitive:
        pass

    @abstractmethod
    def value_post_sds__wo_hds(self, primitive: Path, sds: SandboxDirectoryStructure) -> PathDescriberHandlerForPrimitive:
        pass

    @abstractmethod
    def value_post_sds(self, primitive: Path, tcds: Tcds) -> PathDescriberHandlerForPrimitive:
        pass

    @abstractmethod
    def value_of_any_dependency(self, primitive: Path, tcds: Tcds) -> PathDescriberHandlerForPrimitive:
        pass


class DescribedPathWHandler(DescribedPath):

    def __init__(self, path: Path, describer_handler: PathDescriberHandlerForPrimitive):
        self._path = path
        self._describer_handler = describer_handler

    @property
    def primitive(self) -> Path:
        return self._path

    @property
    def describer(self) -> PathDescriberForPrimitive:
        return self._describer_handler.describer

    def child(self, child_path_component: str) -> DescribedPath:
        child_path = self._path / child_path_component
        return DescribedPathWHandler(child_path, self._describer_handler.child(child_path, child_path_component))

    def parent(self) -> DescribedPath:
        parent_path = self._path.parent
        return DescribedPathWHandler(parent_path, self._describer_handler.parent(parent_path))