# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/default/program_modes/test_case/builtin_symbols/string_transformers.py
# Compiled at: 2020-01-20 02:27:16
# Size of source mod 2**32: 1141 bytes
from exactly_lib.cli.main_program import builtin_symbol_of_custom_symbol
from exactly_lib.test_case_utils.string_transformer import custom_transformers
TO_LOWER_CASE = 'TO_LOWER_CASE'
TO_UPPER_CASE = 'TO_UPPER_CASE'
EXACTLY_TEST_CASE_DIRS_REPLACEMENT = 'REPLACE_TEST_CASE_DIRS'
_TO_UPPER_SINGLE_LINE_DESCRIPTION = ''
ALL = (
 builtin_symbol_of_custom_symbol(EXACTLY_TEST_CASE_DIRS_REPLACEMENT, custom_transformers.replace_env_vars(EXACTLY_TEST_CASE_DIRS_REPLACEMENT), custom_transformers.replace_tcds_paths_doc()),
 builtin_symbol_of_custom_symbol(TO_UPPER_CASE, custom_transformers.to_upper_case(TO_UPPER_CASE), custom_transformers.to_upper_case_doc()),
 builtin_symbol_of_custom_symbol(TO_LOWER_CASE, custom_transformers.to_lower_case(TO_LOWER_CASE), custom_transformers.to_lower_case_doc()))