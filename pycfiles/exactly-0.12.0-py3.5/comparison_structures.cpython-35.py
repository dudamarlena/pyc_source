# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/condition/comparison_structures.py
# Compiled at: 2019-12-27 10:07:53
# Size of source mod 2**32: 1712 bytes
from abc import ABC, abstractmethod
from typing import Sequence, TypeVar, Generic, Set
from exactly_lib.symbol.path_resolving_environment import PathResolvingEnvironmentPreSds
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.test_case_file_structure.dir_dependent_value import MultiDependenciesDdv
from exactly_lib.test_case_file_structure.path_relativity import DirectoryStructurePartition
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.util.description_tree.renderer import DetailsRenderer
from exactly_lib.util.symbol_table import SymbolTable
A = TypeVar('A')
T = TypeVar('T')

class OperandDdv(Generic[T], MultiDependenciesDdv[T], ABC):

    @abstractmethod
    def describer(self) -> DetailsRenderer:
        pass

    def resolving_dependencies(self) -> Set[DirectoryStructurePartition]:
        return set()

    def value_when_no_dir_dependencies(self) -> T:
        """
        :raises DirDependencyError: This value has dir dependencies.
        """
        raise ValueError(str(type(self)) + ' do not support this short cut.')

    @abstractmethod
    def value_of_any_dependency(self, tcds: Tcds) -> T:
        """Gives the value, regardless of actual dependency."""
        pass


class OperandSdv(Generic[T], ABC):
    __doc__ = 'Resolves an operand used in a comparision'

    @property
    def references(self) -> Sequence[SymbolReference]:
        return []

    def validate_pre_sds(self, environment: PathResolvingEnvironmentPreSds):
        """
        Validates by raising exceptions from `return_svh_via_exceptions`
        """
        pass

    @abstractmethod
    def resolve(self, symbols: SymbolTable) -> OperandDdv[T]:
        pass