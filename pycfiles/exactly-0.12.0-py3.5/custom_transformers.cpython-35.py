# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/string_transformer/custom_transformers.py
# Compiled at: 2020-01-20 02:27:16
# Size of source mod 2**32: 1494 bytes
from exactly_lib.symbol.logic.string_transformer import StringTransformerSdv
from exactly_lib.test_case_utils.string_transformer import sdvs
from exactly_lib.test_case_utils.string_transformer.impl import tcds_paths_replacement, case_converters
from exactly_lib.test_case_utils.symbol.custom_symbol import CustomSymbolDocumentation
from exactly_lib.util.textformat.structure import document

def to_upper_case(name: str) -> StringTransformerSdv:
    return sdvs.StringTransformerSdvConstant(case_converters.ToUpperCaseStringTransformer(name))


def to_lower_case(name: str) -> StringTransformerSdv:
    return sdvs.StringTransformerSdvConstant(case_converters.ToLowerCaseStringTransformer(name))


def replace_env_vars(name: str) -> StringTransformerSdv:
    return sdvs.StringTransformerSdvConstantOfDdv(tcds_paths_replacement.ddv(name))


def to_upper_case_doc() -> CustomSymbolDocumentation:
    return CustomSymbolDocumentation('Converts all cased characters to uppercase', document.empty_section_contents())


def to_lower_case_doc() -> CustomSymbolDocumentation:
    return CustomSymbolDocumentation('Converts all cased characters to lowercase', document.empty_section_contents())


def replace_tcds_paths_doc() -> CustomSymbolDocumentation:
    return CustomSymbolDocumentation(tcds_paths_replacement.SINGLE_LINE_DESCRIPTION, tcds_paths_replacement.help_section_contents(), tcds_paths_replacement.see_also())