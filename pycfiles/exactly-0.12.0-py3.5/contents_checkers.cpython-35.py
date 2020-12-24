# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/instructions/assert_/utils/file_contents/parts/contents_checkers.py
# Compiled at: 2019-12-27 10:07:53
# Size of source mod 2**32: 3113 bytes
from typing import Sequence
from exactly_lib.instructions.assert_.utils.assertion_part import AssertionPart, IdentityAssertionPart
from exactly_lib.instructions.assert_.utils.file_contents.actual_files import ComparisonActualFileConstructor, ComparisonActualFile
from exactly_lib.symbol.symbol_usage import SymbolReference
from exactly_lib.test_case.os_services import OsServices
from exactly_lib.test_case.phases.common import InstructionEnvironmentForPostSdsStep, InstructionSourceInfo
from exactly_lib.test_case_utils import file_properties, path_check
from exactly_lib.test_case_utils import pfh_exception
from exactly_lib.test_case_utils.string_transformer.impl.identity import IdentityStringTransformer
from exactly_lib.type_system.logic.string_matcher import DestinationFilePathGetter, FileToCheck

class FileConstructorAssertionPart(AssertionPart[(ComparisonActualFileConstructor, ComparisonActualFile)]):
    __doc__ = '\n    Constructs the actual file.\n    '

    def check(self, environment: InstructionEnvironmentForPostSdsStep, os_services: OsServices, custom_environment: InstructionSourceInfo, value_to_check: ComparisonActualFileConstructor) -> ComparisonActualFile:
        return value_to_check.construct(custom_environment, environment, os_services)


class ConstructFileToCheckAssertionPart(AssertionPart[(ComparisonActualFile, FileToCheck)]):

    @property
    def references(self) -> Sequence[SymbolReference]:
        return ()

    def check(self, environment: InstructionEnvironmentForPostSdsStep, os_services: OsServices, custom_environment, file_to_transform: ComparisonActualFile) -> FileToCheck:
        return FileToCheck(file_to_transform.path, IdentityStringTransformer(), DestinationFilePathGetter())


class IsExistingRegularFileAssertionPart(IdentityAssertionPart[ComparisonActualFile]):
    __doc__ = '\n    :raises pfh_exception.PfhFailException: The file is not an existing regular file (symlinks followed).\n    '

    def __init__(self):
        super().__init__()
        self._is_regular_file_check = file_properties.must_exist_as(file_properties.FileType.REGULAR, follow_symlinks=True)

    def _check(self, environment: InstructionEnvironmentForPostSdsStep, os_services: OsServices, custom_environment, actual_file: ComparisonActualFile):
        if actual_file.file_access_needs_to_be_verified:
            self._IsExistingRegularFileAssertionPart__check(actual_file)

    def _IsExistingRegularFileAssertionPart__check(self, actual_file: ComparisonActualFile):
        if actual_file.file_access_needs_to_be_verified:
            mb_failure = path_check.failure_message_or_none(self._is_regular_file_check, actual_file.path)
            if mb_failure:
                raise pfh_exception.PfhHardErrorException(mb_failure)