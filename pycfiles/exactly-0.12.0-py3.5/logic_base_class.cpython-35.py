# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/logic/logic_base_class.py
# Compiled at: 2019-12-27 10:07:45
# Size of source mod 2**32: 1215 bytes
from abc import abstractmethod, ABC
from typing import TypeVar, Generic
from exactly_lib.test_case_file_structure.dir_dependent_value import DirDependentValue
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.description.tree_structured import WithTreeStructureDescription
from exactly_lib.util.file_utils import TmpDirFileSpace

class ApplicationEnvironment:

    def __init__(self, tmp_files_space: TmpDirFileSpace):
        self._tmp_files_space = tmp_files_space

    @property
    def tmp_files_space(self) -> TmpDirFileSpace:
        return self._tmp_files_space


VALUE_TYPE = TypeVar('VALUE_TYPE')

class ApplicationEnvironmentDependentValue(Generic[VALUE_TYPE], ABC):
    __doc__ = 'Application Environment Dependent Matcher'

    @abstractmethod
    def applier(self, environment: ApplicationEnvironment) -> VALUE_TYPE:
        pass


class LogicTypeDdv(Generic[VALUE_TYPE], DirDependentValue[VALUE_TYPE], WithTreeStructureDescription, ABC):

    @abstractmethod
    def value_of_any_dependency(self, tcds: Tcds) -> ApplicationEnvironmentDependentValue[VALUE_TYPE]:
        pass