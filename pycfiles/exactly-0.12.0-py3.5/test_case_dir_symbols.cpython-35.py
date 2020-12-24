# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/default/program_modes/test_case/builtin_symbols/test_case_dir_symbols.py
# Compiled at: 2020-01-20 02:27:16
# Size of source mod 2**32: 1582 bytes
from exactly_lib.cli.main_program import BuiltinSymbol
from exactly_lib.definitions.tcds_symbols import SYMBOL_DESCRIPTION
from exactly_lib.symbol import sdv_structure
from exactly_lib.symbol.data import path_sdvs
from exactly_lib.test_case_file_structure import tcds_symbols
from exactly_lib.test_case_file_structure.path_relativity import RelOptionType
from exactly_lib.util.textformat.structure.document import SectionContents
from exactly_lib.util.textformat.textformat_parser import TextParser

def __sdv_of(rel_option_type: RelOptionType) -> sdv_structure.SymbolDependentValue:
    return path_sdvs.of_rel_option(rel_option_type)


_TEXT_PARSER = TextParser()

def _builtin(symbol_name: str, relativity: RelOptionType) -> BuiltinSymbol:
    return BuiltinSymbol(symbol_name, __sdv_of(relativity), SYMBOL_DESCRIPTION.as_single_line_description_str(symbol_name), SectionContents([]))


SYMBOL_HDS_CASE = _builtin(tcds_symbols.SYMBOL_HDS_CASE, RelOptionType.REL_HDS_CASE)
SYMBOL_HDS_ACT = _builtin(tcds_symbols.SYMBOL_HDS_ACT, RelOptionType.REL_HDS_ACT)
SYMBOL_ACT = _builtin(tcds_symbols.SYMBOL_ACT, RelOptionType.REL_ACT)
SYMBOL_TMP = _builtin(tcds_symbols.SYMBOL_TMP, RelOptionType.REL_TMP)
SYMBOL_RESULT = _builtin(tcds_symbols.SYMBOL_RESULT, RelOptionType.REL_RESULT)
ALL = (
 SYMBOL_HDS_CASE,
 SYMBOL_HDS_ACT,
 SYMBOL_ACT,
 SYMBOL_TMP,
 SYMBOL_RESULT)