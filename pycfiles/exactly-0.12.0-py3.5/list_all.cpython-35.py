# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/cli/program_modes/symbol/impl/reports/list_all.py
# Compiled at: 2019-12-27 10:07:50
# Size of source mod 2**32: 4449 bytes
import functools
from typing import Callable, List, Iterator, Sequence
from exactly_lib.cli.program_modes.symbol.impl.report import ReportGenerator, Report, ReportBlock
from exactly_lib.cli.program_modes.symbol.impl.reports.symbol_info import SymbolDefinitionInfo, DefinitionsResolver
from exactly_lib.definitions.test_case.instructions.define_symbol import ANY_TYPE_INFO_DICT
from exactly_lib.type_system.value_type import ValueType
from exactly_lib.util.simple_textstruct import structure
from exactly_lib.util.simple_textstruct.structure import MajorBlock
from exactly_lib.util.string import inside_parens

class ListReportGenerator(ReportGenerator):

    def generate(self, definitions_resolver: DefinitionsResolver) -> Report:
        return _ListReport(list(definitions_resolver.definitions()))


class SymbolListBlock(ReportBlock):

    def __init__(self, definitions: Sequence[SymbolDefinitionInfo]):
        self.definitions = definitions

    def render(self) -> MajorBlock:
        def_report_infos = map(mk_single_def_report_info, self.definitions)
        definition_lines = _get_list_lines(def_report_infos)
        return MajorBlock([
         structure.MinorBlock([
          structure.LineElement(structure.StringLinesObject(definition_lines))])])


class _ListReport(Report):

    def __init__(self, definitions: Sequence[SymbolDefinitionInfo]):
        self.definitions = definitions

    @property
    def is_success(self) -> bool:
        return True

    def blocks(self) -> Sequence[ReportBlock]:
        return [
         SymbolListBlock([definition for definition in self.definitions if definition.is_user_defined()])]


class _SingleDefinitionReportInfo:

    def __init__(self, name: str, value_type: ValueType, num_refs: int):
        self._name = name
        self._value_type = value_type
        self._num_refs = num_refs
        self._num_refs_str = _format_num_refs_info(num_refs)
        self._type_identifier = ANY_TYPE_INFO_DICT[self.value_type()].identifier

    def name(self) -> str:
        return self._name

    def name_length(self) -> int:
        return len(self._name)

    def value_type(self) -> ValueType:
        return self._value_type

    def type_identifier(self) -> str:
        return self._type_identifier

    def type_identifier_length(self) -> int:
        return len(self._type_identifier)

    def num_refs_str(self) -> str:
        return self._num_refs_str

    def num_refs_str_length(self) -> int:
        return len(self._num_refs_str)


def mk_single_def_report_info(definition: SymbolDefinitionInfo) -> _SingleDefinitionReportInfo:
    return _SingleDefinitionReportInfo(definition.name(), definition.value_type(), len(definition.references))


def _format_num_refs_info(num_refs: int) -> str:
    return inside_parens(num_refs)


def _get_list_lines(symbols: Iterator[_SingleDefinitionReportInfo]) -> List[str]:
    symbol_list = list(symbols)
    symbol_line_formatter = _symbol_line_formatter(symbol_list)
    return [symbol_line_formatter(symbol) for symbol in symbol_list]


def _symbol_line_formatter--- This code section failed: ---

 L. 108         0  LOAD_GLOBAL              functools
                3  LOAD_ATTR                reduce
                6  LOAD_GLOBAL              _max_int

 L. 109         9  LOAD_GLOBAL              map
               12  LOAD_GLOBAL              _SingleDefinitionReportInfo
               15  LOAD_ATTR                type_identifier_length

 L. 110        18  LOAD_FAST                'symbols'
               21  CALL_FUNCTION_2       2  '2 positional, 0 named'

 L. 111        24  LOAD_CONST               0
               27  CALL_FUNCTION_3       3  '3 positional, 0 named'
               30  STORE_FAST               'max_type_identifier_len'

 L. 112        33  LOAD_GLOBAL              functools
               36  LOAD_ATTR                reduce
               39  LOAD_GLOBAL              _max_int

 L. 113        42  LOAD_GLOBAL              map
               45  LOAD_GLOBAL              _SingleDefinitionReportInfo
               48  LOAD_ATTR                num_refs_str_length
               51  LOAD_FAST                'symbols'
               54  CALL_FUNCTION_2       2  '2 positional, 0 named'

 L. 114        57  LOAD_CONST               0
               60  CALL_FUNCTION_3       3  '3 positional, 0 named'
               63  STORE_FAST               'max_num_refs_len'

 L. 116        66  LOAD_STR                 '%-{}s %-{}s'
               69  LOAD_ATTR                format
               72  LOAD_FAST                'max_type_identifier_len'

 L. 117        75  LOAD_FAST                'max_num_refs_len'
               78  CALL_FUNCTION_2       2  '2 positional, 0 named'
               81  STORE_DEREF              'type_formatting_string'

 L. 119        84  LOAD_GLOBAL              _SingleDefinitionReportInfo
               87  LOAD_GLOBAL              str
               90  LOAD_CONST               ('symbol', 'return')
               93  LOAD_CLOSURE             'type_formatting_string'
               96  BUILD_TUPLE_1         1 
               99  LOAD_CODE                <code_object ret_val>
              102  LOAD_STR                 '_symbol_line_formatter.<locals>.ret_val'
              105  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
              111  STORE_FAST               'ret_val'

 L. 126       114  LOAD_FAST                'ret_val'
              117  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_CLOSURE_A_3_0' instruction at offset 105


def _max_int(x: int, y: int) -> int:
    return max(x, y)