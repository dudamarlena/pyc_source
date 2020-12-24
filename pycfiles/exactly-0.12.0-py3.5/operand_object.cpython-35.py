# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/matcher/impls/operand_object.py
# Compiled at: 2019-12-27 10:07:41
# Size of source mod 2**32: 2695 bytes
from typing import Generic, TypeVar, Sequence, Set, Optional
from exactly_lib.common.report_rendering.text_doc import TextRenderer
from exactly_lib.symbol.path_resolving_environment import PathResolvingEnvironmentPreSds
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.test_case.validation.ddv_validation import DdvValidator
from exactly_lib.test_case_file_structure.home_directory_structure import HomeDirectoryStructure
from exactly_lib.test_case_file_structure.path_relativity import DirectoryStructurePartition
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.test_case_utils.condition.comparison_structures import OperandSdv, OperandDdv
from exactly_lib.test_case_utils.matcher.object import ObjectSdv, ObjectDdv
from exactly_lib.test_case_utils.svh_exception import SvhException
from exactly_lib.util.description_tree.renderer import DetailsRenderer
from exactly_lib.util.symbol_table import SymbolTable
T = TypeVar('T')

class ObjectValueOfOperandDdv(Generic[T], ObjectDdv[T]):

    def __init__(self, validator: DdvValidator, operand: OperandDdv[T]):
        self._validator = validator
        self._operand = operand

    def describer(self) -> DetailsRenderer:
        return self._operand.describer()

    def resolving_dependencies(self) -> Set[DirectoryStructurePartition]:
        return self._operand.resolving_dependencies()

    @property
    def validator(self) -> DdvValidator:
        return self._validator

    def value_of_any_dependency(self, tcds: Tcds) -> T:
        return self._operand.value_of_any_dependency(tcds)


class ObjectSdvOfOperandSdv(Generic[T], ObjectSdv[T]):

    def __init__(self, operand: OperandSdv):
        self._operand = operand

    @property
    def references(self) -> Sequence[SymbolReference]:
        return self._operand.references

    def resolve(self, symbols: SymbolTable) -> ObjectDdv[T]:
        return ObjectValueOfOperandDdv(_Validator(symbols, self._operand), self._operand.resolve(symbols))


class _Validator(DdvValidator):

    def __init__(self, symbols: SymbolTable, operand: OperandSdv):
        self._symbols = symbols
        self._operand = operand

    def validate_pre_sds_if_applicable(self, hds: HomeDirectoryStructure) -> Optional[TextRenderer]:
        try:
            self._operand.validate_pre_sds(PathResolvingEnvironmentPreSds(hds, self._symbols))
        except SvhException as ex:
            return ex.err_msg

    def validate_post_sds_if_applicable(self, tcds: Tcds) -> Optional[TextRenderer]:
        pass