# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/property_getter.py
# Compiled at: 2019-12-27 10:07:45
# Size of source mod 2**32: 1566 bytes
from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.test_case.validation import ddv_validation
from exactly_lib.test_case.validation.ddv_validation import DdvValidator
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.description.tree_structured import WithTreeStructureDescription
from exactly_lib.type_system.logic.logic_base_class import ApplicationEnvironment
from exactly_lib.util.symbol_table import SymbolTable
MODEL = TypeVar('MODEL')
T = TypeVar('T')

class PropertyGetter(Generic[(MODEL, T)], WithTreeStructureDescription, ABC):

    @abstractmethod
    def get_from(self, model: MODEL) -> T:
        """
        :raises HardErrorException
        """
        pass


class PropertyGetterAdv(Generic[(MODEL, T)], ABC):

    @abstractmethod
    def applier(self, environment: ApplicationEnvironment) -> PropertyGetter[(MODEL, T)]:
        pass


class PropertyGetterDdv(Generic[(MODEL, T)], WithTreeStructureDescription, ABC):

    @property
    def validator(self) -> DdvValidator:
        return ddv_validation.constant_success_validator()

    @abstractmethod
    def value_of_any_dependency(self, tcds: Tcds) -> PropertyGetterAdv[(MODEL, T)]:
        pass


class PropertyGetterSdv(Generic[(MODEL, T)], ABC):

    @property
    @abstractmethod
    def references(self) -> Sequence[SymbolReference]:
        pass

    @abstractmethod
    def resolve(self, symbols: SymbolTable) -> PropertyGetterDdv[(MODEL, T)]:
        pass