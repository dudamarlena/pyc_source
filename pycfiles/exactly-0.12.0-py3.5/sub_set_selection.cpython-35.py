# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/files_matcher/impl/sub_set_selection.py
# Compiled at: 2020-01-31 11:01:49
# Size of source mod 2**32: 1116 bytes
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.symbol.logic.file_matcher import FileMatcherSdv
from exactly_lib.test_case_utils.files_matcher import config
from exactly_lib.type_system.logic.file_matcher import FileMatcher
from exactly_lib.type_system.logic.files_matcher import FilesMatcherModel, GenericFilesMatcherSdv
from exactly_lib.util.cli_syntax import option_syntax
from . import model_modifier_utils

def matcher(dir_selector: FileMatcherSdv, matcher_on_result: GenericFilesMatcherSdv) -> GenericFilesMatcherSdv:
    return model_modifier_utils.matcher(_CONFIGURATION, dir_selector, matcher_on_result)


def _get_model(file_selector: FileMatcher, model: FilesMatcherModel) -> FilesMatcherModel:
    return model.sub_set(file_selector)


_CONFIGURATION = model_modifier_utils.Configuration(' '.join([
 option_syntax.option_syntax(config.SELECTION_OPTION.name),
 syntax_elements.FILE_MATCHER_SYNTAX_ELEMENT.singular_name,
 syntax_elements.FILES_MATCHER_SYNTAX_ELEMENT.singular_name]), _get_model)