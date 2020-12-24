# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/files_matcher/impl/quant_over_files.py
# Compiled at: 2020-01-29 10:10:30
# Size of source mod 2**32: 1523 bytes
import contextlib
from typing import Iterator
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.definitions.primitives import files_matcher as files_matcher_primitives
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.test_case_utils.description_tree import custom_details
from exactly_lib.test_case_utils.matcher.impls import quantifier_matchers
from exactly_lib.type_system.logic.file_matcher import FileMatcherModel
from exactly_lib.type_system.logic.files_matcher import FilesMatcherModel
from exactly_lib.type_system.logic.logic_base_class import ApplicationEnvironment
from exactly_lib.util.description_tree.renderer import DetailsRenderer

def _element_detail_renderer(element: FileMatcherModel) -> DetailsRenderer:
    return custom_details.path_primitive_details_renderer(element.path.describer)


@contextlib.contextmanager
def _file_elements_from_model(tcds: Tcds, environment: ApplicationEnvironment, model: FilesMatcherModel) -> Iterator[FileMatcherModel]:
    yield (file_element.as_file_matcher_model() for file_element in model.files())


ELEMENT_SETUP = quantifier_matchers.ElementSetup(quantifier_matchers.ElementRendering(files_matcher_primitives.QUANTIFICATION_OVER_FILE_ARGUMENT, syntax_elements.FILE_MATCHER_SYNTAX_ELEMENT.singular_name, _element_detail_renderer), _file_elements_from_model)