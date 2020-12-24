# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/file_matcher/impl/regular_file_contents.py
# Compiled at: 2020-01-29 09:08:19
# Size of source mod 2**32: 1414 bytes
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.definitions.test_case import file_check_properties
from exactly_lib.test_case_utils import file_properties
from exactly_lib.test_case_utils.file_matcher.impl import file_contents_utils
from exactly_lib.test_case_utils.generic_dependent_value import sdv_of_constant_primitive
from exactly_lib.test_case_utils.string_transformer.impl import identity
from exactly_lib.type_system.logic import string_matcher
from exactly_lib.type_system.logic.file_matcher import FileMatcherModel, GenericFileMatcherSdv
from exactly_lib.type_system.logic.string_matcher import FileToCheck, GenericStringMatcherSdv
NAMES = file_contents_utils.NamesSetup(file_check_properties.REGULAR_FILE_CONTENTS, file_properties.FileType.REGULAR, syntax_elements.STRING_MATCHER_SYNTAX_ELEMENT)

class _ModelConstructor(file_contents_utils.ModelConstructor[FileToCheck]):

    def make_model(self, model: FileMatcherModel) -> FileToCheck:
        return string_matcher.FileToCheck(model.path, identity.IdentityStringTransformer(), string_matcher.DestinationFilePathGetter())


def sdv__generic(contents_matcher: GenericStringMatcherSdv) -> GenericFileMatcherSdv:
    return file_contents_utils.sdv__generic(NAMES, sdv_of_constant_primitive(_ModelConstructor()), contents_matcher)