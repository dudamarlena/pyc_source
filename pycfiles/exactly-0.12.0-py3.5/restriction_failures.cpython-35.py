# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/symbol/err_msg/restriction_failures.py
# Compiled at: 2019-12-27 10:07:54
# Size of source mod 2**32: 5457 bytes
import itertools
from typing import List, Sequence
from exactly_lib.common.err_msg.definitions import Blocks, single_str_block
from exactly_lib.common.report_rendering import text_docs
from exactly_lib.common.report_rendering.text_doc import TextRenderer
from exactly_lib.symbol.data.restrictions.reference_restrictions import FailureOfDirectReference, FailureOfIndirectReference
from exactly_lib.symbol.data.value_restriction import ErrorMessageWithFixTip
from exactly_lib.symbol.err_msg import error_messages
from exactly_lib.symbol.lookups import lookup_container
from exactly_lib.symbol.restriction import Failure, InvalidTypeCategoryFailure, InvalidValueTypeFailure
from exactly_lib.symbol.sdv_structure import SymbolContainer
from exactly_lib.type_system.value_type import TYPE_CATEGORY_2_VALUE_TYPE_SEQUENCE
from exactly_lib.util.render import combinators
from exactly_lib.util.render.renderer import SequenceRenderer
from exactly_lib.util.simple_textstruct.structure import MajorBlock
from exactly_lib.util.symbol_table import SymbolTable

class ErrorMessage(SequenceRenderer[MajorBlock]):

    def __init__(self, failing_symbol: str, symbols: SymbolTable, failure: Failure):
        self._failing_symbol = failing_symbol
        self._symbols = symbols
        self._failure = failure

    def render_sequence(self) -> Sequence[MajorBlock]:
        failure = self._failure
        if isinstance(failure, FailureOfDirectReference):
            return ErrorMessageForDirectReference(failure.error).render_sequence()
        if isinstance(failure, FailureOfIndirectReference):
            return self._of_indirect(failure)
        if isinstance(failure, InvalidTypeCategoryFailure):
            return self._of_invalid_type_category(failure)
        if isinstance(failure, InvalidValueTypeFailure):
            return self._of_invalid_value_type(failure)
        raise TypeError('Unknown type of {}: {}'.format(str(Failure), str(failure)))

    def _of_indirect(self, failure: FailureOfIndirectReference) -> Sequence[MajorBlock]:
        return _of_indirect(self._failing_symbol, self._symbols, failure).render_sequence()

    def _of_invalid_type_category(self, failure: InvalidTypeCategoryFailure) -> Sequence[MajorBlock]:
        value_restriction_failure = error_messages.invalid_type_msg(TYPE_CATEGORY_2_VALUE_TYPE_SEQUENCE[failure.expected], self._failing_symbol, lookup_container(self._symbols, self._failing_symbol))
        return _render_vrf(value_restriction_failure)

    def _of_invalid_value_type(self, failure: InvalidValueTypeFailure) -> Sequence[MajorBlock]:
        value_restriction_failure = error_messages.invalid_type_msg([
         failure.expected], self._failing_symbol, lookup_container(self._symbols, self._failing_symbol))
        return _render_vrf(value_restriction_failure)


class ErrorMessageForDirectReference(SequenceRenderer[MajorBlock]):

    def __init__(self, error: ErrorMessageWithFixTip):
        self._error = error

    def render_sequence(self) -> Sequence[MajorBlock]:
        return _render_vrf(self._error)


def _of_indirect(failing_symbol: str, symbols: SymbolTable, failure: FailureOfIndirectReference) -> TextRenderer:
    major_blocks_sequence = []
    if failure.meaning_of_failure:
        major_blocks_sequence.append(failure.meaning_of_failure)
    error = failure.error
    major_blocks_sequence.append(error.message)
    major_blocks_sequence.append(_path_to_failing_symbol(failing_symbol, failure.path_to_failing_symbol, symbols))
    if error.how_to_fix is not None:
        major_blocks_sequence.append(error.how_to_fix)
    return combinators.ConcatenationR(major_blocks_sequence)


def _path_to_failing_symbol__old--- This code section failed: ---

 L. 104         0  LOAD_GLOBAL              str
                3  LOAD_GLOBAL              Blocks
                6  LOAD_CONST               ('symbol_name', 'return')
                9  LOAD_CLOSURE             'symbols'
               12  BUILD_TUPLE_1         1 
               15  LOAD_CODE                <code_object line_ref_of_symbol>
               18  LOAD_STR                 '_path_to_failing_symbol__old.<locals>.line_ref_of_symbol'
               21  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               27  STORE_FAST               'line_ref_of_symbol'

 L. 109        30  LOAD_FAST                'failing_symbol'
               33  BUILD_LIST_1          1 
               36  LOAD_FAST                'path_to_failing_symbol'
               39  BINARY_ADD       
               40  STORE_FAST               'path_to_failing_symbol'

 L. 112        43  LOAD_GLOBAL              single_str_block
               46  LOAD_STR                 'Referenced via'
               49  CALL_FUNCTION_1       1  '1 positional, 0 named'
               52  BUILD_LIST_1          1 
               55  STORE_FAST               'ret_val'

 L. 115        58  LOAD_FAST                'ret_val'
               61  LOAD_GLOBAL              itertools
               64  LOAD_ATTR                chain
               67  LOAD_ATTR                from_iterable
               70  LOAD_GLOBAL              map
               73  LOAD_FAST                'line_ref_of_symbol'
               76  LOAD_FAST                'path_to_failing_symbol'
               79  CALL_FUNCTION_2       2  '2 positional, 0 named'
               82  CALL_FUNCTION_1       1  '1 positional, 0 named'
               85  INPLACE_ADD      
               86  STORE_FAST               'ret_val'

 L. 117        89  LOAD_FAST                'ret_val'
               92  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _path_to_failing_symbol(failing_symbol: str, path_to_failing_symbol: List[str], symbols: SymbolTable) -> TextRenderer:
    return text_docs.major_blocks_of_string_blocks(_path_to_failing_symbol__old(failing_symbol, path_to_failing_symbol, symbols))


def _render_vrf(vrf: ErrorMessageWithFixTip) -> Sequence[MajorBlock]:
    ret_val = list(vrf.message.render_sequence())
    if vrf.how_to_fix is not None:
        ret_val += vrf.how_to_fix.render_sequence()
    return ret_val