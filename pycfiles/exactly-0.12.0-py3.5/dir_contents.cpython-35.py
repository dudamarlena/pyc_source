# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/file_matcher/impl/dir_contents.py
# Compiled at: 2020-01-29 09:08:19
# Size of source mod 2**32: 6362 bytes
from typing import Optional, Sequence
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.definitions.primitives import file_or_dir_contents
from exactly_lib.definitions.test_case import file_check_properties
from exactly_lib.symbol.object_with_symbol_references import references_from_objects_with_symbol_references
from exactly_lib.test_case.validation import ddv_validators
from exactly_lib.test_case.validation.ddv_validation import DdvValidator
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.test_case_utils import file_properties, generic_dependent_value
from exactly_lib.test_case_utils.condition.integer.integer_ddv import IntegerDdv
from exactly_lib.test_case_utils.condition.integer.integer_sdv import IntegerSdv
from exactly_lib.test_case_utils.file_matcher.impl import file_contents_utils
from exactly_lib.test_case_utils.file_matcher.impl.file_contents_utils import ModelConstructor
from exactly_lib.test_case_utils.files_matcher import models
from exactly_lib.test_case_utils.generic_dependent_value import Sdv, sdv_of_constant_primitive, Ddv, Adv
from exactly_lib.type_system.logic.file_matcher import FileMatcherModel, GenericFileMatcherSdv
from exactly_lib.type_system.logic.files_matcher import FilesMatcherModel, GenericFilesMatcherSdv
from exactly_lib.util.cli_syntax import option_syntax
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.description_tree import details
from exactly_lib.util.description_tree.renderer import DetailsRenderer
from exactly_lib.util.description_tree.tree import Detail
from exactly_lib.util.functional import map_optional, filter_not_none
from exactly_lib.util.symbol_table import SymbolTable
NAMES = file_contents_utils.NamesSetup(file_check_properties.DIR_CONTENTS, file_properties.FileType.DIRECTORY, syntax_elements.FILES_MATCHER_SYNTAX_ELEMENT)

class _NonRecursiveModelConstructor(file_contents_utils.ModelConstructor[FilesMatcherModel]):

    def make_model(self, model: FileMatcherModel) -> FilesMatcherModel:
        return models.non_recursive(model.path)


MODEL_CONSTRUCTOR__NON_RECURSIVE = sdv_of_constant_primitive(_NonRecursiveModelConstructor())

def model_constructor__recursive--- This code section failed: ---

 L.  45         0  LOAD_GLOBAL              SymbolTable
                3  LOAD_GLOBAL              Ddv
                6  LOAD_GLOBAL              ModelConstructor
                9  LOAD_GLOBAL              FilesMatcherModel
               12  BINARY_SUBSCR    
               13  BINARY_SUBSCR    
               14  LOAD_CONST               ('symbols', 'return')
               17  LOAD_CLOSURE             'max_depth'
               20  LOAD_CLOSURE             'min_depth'
               23  BUILD_TUPLE_2         2 
               26  LOAD_CODE                <code_object make_ddv>
               29  LOAD_STR                 'model_constructor__recursive.<locals>.make_ddv'
               32  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               38  STORE_FAST               'make_ddv'

 L.  54        41  LOAD_GLOBAL              generic_dependent_value
               44  LOAD_ATTR                SdvFromParts

 L.  55        47  LOAD_FAST                'make_ddv'

 L.  56        50  LOAD_GLOBAL              references_from_objects_with_symbol_references

 L.  57        53  LOAD_GLOBAL              filter_not_none
               56  LOAD_DEREF               'min_depth'
               59  LOAD_DEREF               'max_depth'
               62  BUILD_LIST_2          2 
               65  CALL_FUNCTION_1       1  '1 positional, 0 named'
               68  CALL_FUNCTION_1       1  '1 positional, 0 named'
               71  CALL_FUNCTION_2       2  '2 positional, 0 named'
               74  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def dir_matches_files_matcher_sdv__generic(model_constructor: Sdv[ModelConstructor[FilesMatcherModel]], contents_matcher: GenericFilesMatcherSdv) -> GenericFileMatcherSdv:
    return file_contents_utils.sdv__generic(NAMES, model_constructor, contents_matcher)


class _RecursiveStructureRenderer(DetailsRenderer):

    def __init__(self, min_depth: Optional[DetailsRenderer], max_depth: Optional[DetailsRenderer]):
        self._min_depth = min_depth
        self._max_depth = max_depth

    def render(self) -> Sequence[Detail]:
        return self._renderer().render()

    def _renderer(self) -> DetailsRenderer:
        recursive = details.String(option_syntax.option_syntax(file_or_dir_contents.RECURSIVE_OPTION.name))
        limits = filter_not_none([
         map_optionallambda d: self._mk_detailfile_or_dir_contents.MIN_DEPTH_OPTIONdself._min_depth,
         map_optionallambda d: self._mk_detailfile_or_dir_contents.MAX_DEPTH_OPTIONdself._max_depth])
        return details.SequenceRenderer([recursive] + limits)

    @staticmethod
    def _mk_detail(option: a.Option, limit: DetailsRenderer) -> DetailsRenderer:
        return details.HeaderAndValueoption_syntax.option_syntax(option.name)limit


class _RecursiveModelConstructor(ModelConstructor[FilesMatcherModel]):

    def __init__(self, min_depth: Optional[int], max_depth: Optional[int]):
        self._min_depth = min_depth
        self._max_depth = max_depth

    @property
    def structure(self) -> DetailsRenderer:
        return _RecursiveStructureRenderermap_optionaldetails.Stringself._min_depthmap_optionaldetails.Stringself._max_depth

    def make_model(self, model: FileMatcherModel) -> FilesMatcherModel:
        return models.recursive(model.path, self._min_depth, self._max_depth)


class _RecursiveModelConstructorDdv(Ddv[ModelConstructor[FilesMatcherModel]]):

    def __init__(self, min_depth: Optional[IntegerDdv], max_depth: Optional[IntegerDdv]):
        self._min_depth = min_depth
        self._max_depth = max_depth
        self._validator = ddv_validators.all_of([int_ddv.validator() for int_ddv in [min_depth, max_depth] if int_ddv is not None])

    @property
    def describer(self) -> DetailsRenderer:
        return _RecursiveStructureRenderermap_optionalIntegerDdv.describerself._min_depthmap_optionalIntegerDdv.describerself._max_depth

    @property
    def validator(self) -> DdvValidator:
        return self._validator

    def value_of_any_dependency--- This code section failed: ---

 L. 154         0  LOAD_GLOBAL              IntegerDdv
                3  LOAD_GLOBAL              int
                6  LOAD_CONST               ('x', 'return')
                9  LOAD_CLOSURE             'tcds'
               12  BUILD_TUPLE_1         1 
               15  LOAD_CODE                <code_object get_int_value>
               18  LOAD_STR                 '_RecursiveModelConstructorDdv.value_of_any_dependency.<locals>.get_int_value'
               21  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               27  STORE_FAST               'get_int_value'

 L. 157        30  LOAD_GLOBAL              generic_dependent_value
               33  LOAD_ATTR                ConstantAdv

 L. 158        36  LOAD_GLOBAL              _RecursiveModelConstructor
               39  LOAD_GLOBAL              map_optional
               42  LOAD_FAST                'get_int_value'
               45  LOAD_FAST                'self'
               48  LOAD_ATTR                _min_depth
               51  CALL_FUNCTION_2       2  '2 positional, 0 named'

 L. 159        54  LOAD_GLOBAL              map_optional
               57  LOAD_FAST                'get_int_value'
               60  LOAD_FAST                'self'
               63  LOAD_ATTR                _max_depth
               66  CALL_FUNCTION_2       2  '2 positional, 0 named'
               69  CALL_FUNCTION_2       2  '2 positional, 0 named'
               72  CALL_FUNCTION_1       1  '1 positional, 0 named'
               75  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1