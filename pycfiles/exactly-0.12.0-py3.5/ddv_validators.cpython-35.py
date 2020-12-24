# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case/validation/ddv_validators.py
# Compiled at: 2019-12-27 10:07:44
# Size of source mod 2**32: 2877 bytes
from typing import Optional, Sequence, Iterable
from exactly_lib.common.report_rendering.text_doc import TextRenderer
from exactly_lib.symbol.path_resolving_environment import PathResolvingEnvironmentPreSds, PathResolvingEnvironmentPostSds
from exactly_lib.test_case.validation.ddv_validation import DdvValidator, constant_success_validator
from exactly_lib.test_case.validation.sdv_validation import SdvValidator, PreOrPostSdsValidatorPrimitive
from exactly_lib.test_case_file_structure.home_directory_structure import HomeDirectoryStructure
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.util.symbol_table import SymbolTable

class DdvValidatorFromSdvValidator(DdvValidator):

    def __init__(self, symbols: SymbolTable, adapted: SdvValidator):
        self._symbols = symbols
        self._adapted = adapted

    def validate_pre_sds_if_applicable(self, hds: HomeDirectoryStructure) -> Optional[TextRenderer]:
        environment = PathResolvingEnvironmentPreSds(hds, self._symbols)
        return self._adapted.validate_pre_sds_if_applicable(environment)

    def validate_post_sds_if_applicable(self, tcds: Tcds) -> Optional[TextRenderer]:
        environment = PathResolvingEnvironmentPostSds(tcds.sds, self._symbols)
        return self._adapted.validate_post_sds_if_applicable(environment)


def all_of(validators: Sequence[DdvValidator]) -> DdvValidator:
    if len(validators) == 0:
        return constant_success_validator()
    else:
        if len(validators) == 1:
            return validators[0]
        return AndValidator(validators)


class AndValidator(DdvValidator):

    def __init__(self, validators: Iterable[DdvValidator]):
        self.validators = validators

    def validate_pre_sds_if_applicable(self, hds: HomeDirectoryStructure) -> Optional[TextRenderer]:
        for validator in self.validators:
            result = validator.validate_pre_sds_if_applicable(hds)
            if result is not None:
                return result

    def validate_post_sds_if_applicable(self, tcds: Tcds) -> Optional[TextRenderer]:
        for validator in self.validators:
            result = validator.validate_post_sds_if_applicable(tcds)
            if result is not None:
                return result


class FixedPreOrPostSdsValidator(PreOrPostSdsValidatorPrimitive):

    def __init__(self, tcds: Tcds, validator: DdvValidator):
        self._tcds = tcds
        self._validator = validator

    def validate_pre_sds_if_applicable(self) -> Optional[TextRenderer]:
        return self._validator.validate_pre_sds_if_applicable(self._tcds.hds)

    def validate_post_sds_if_applicable(self) -> Optional[TextRenderer]:
        return self._validator.validate_post_sds_if_applicable(self._tcds)