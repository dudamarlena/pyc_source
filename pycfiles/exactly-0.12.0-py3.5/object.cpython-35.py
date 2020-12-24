# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/object.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 1402 bytes
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Set, Sequence
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.test_case.validation import ddv_validation
from exactly_lib.test_case.validation.ddv_validation import DdvValidator
from exactly_lib.test_case_file_structure.dir_dependent_value import MultiDependenciesDdv
from exactly_lib.test_case_file_structure.path_relativity import DirectoryStructurePartition
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.util.description_tree.renderer import DetailsRenderer
from exactly_lib.util.symbol_table import SymbolTable
T = TypeVar('T')

class ObjectDdv(Generic[T], MultiDependenciesDdv[T], ABC):
    __doc__ = 'DDV for an arbitrary object'

    @abstractmethod
    def describer(self) -> DetailsRenderer:
        pass

    def resolving_dependencies(self) -> Set[DirectoryStructurePartition]:
        return set()

    @property
    def validator(self) -> DdvValidator:
        return ddv_validation.constant_success_validator()

    @abstractmethod
    def value_of_any_dependency(self, tcds: Tcds) -> T:
        pass


class ObjectSdv(Generic[T], ABC):
    __doc__ = 'Resolves an arbitrary object'

    @property
    def references(self) -> Sequence[SymbolReference]:
        return []

    @abstractmethod
    def resolve(self, symbols: SymbolTable) -> ObjectDdv[T]:
        pass