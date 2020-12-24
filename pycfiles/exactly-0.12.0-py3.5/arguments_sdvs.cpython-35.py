# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/program/command/arguments_sdvs.py
# Compiled at: 2020-02-02 15:10:17
# Size of source mod 2**32: 1822 bytes
from exactly_lib.symbol.data import list_sdvs
from exactly_lib.symbol.data import string_sdvs
from exactly_lib.symbol.data.list_sdv import ListSdv
from exactly_lib.symbol.data.path_sdv import PathSdv
from exactly_lib.symbol.logic.program.arguments_sdv import ArgumentsSdv
from exactly_lib.test_case.validation.ddv_validation import DdvValidator
from exactly_lib.test_case_utils import file_properties
from exactly_lib.test_case_utils.file_properties import FileType
from exactly_lib.test_case_utils.path_check import PathCheckDdvValidator, PathCheckDdv
from exactly_lib.util.symbol_table import SymbolTable

def empty() -> ArgumentsSdv:
    return ArgumentsSdv(list_sdvs.empty(), ())


def new_without_validation(arguments: ListSdv) -> ArgumentsSdv:
    return ArgumentsSdv(arguments, ())


def ref_to_file_that_must_exist--- This code section failed: ---

 L.  24         0  LOAD_GLOBAL              SymbolTable
                3  LOAD_GLOBAL              DdvValidator
                6  LOAD_CONST               ('symbols', 'return')
                9  LOAD_CLOSURE             'file_that_must_exist'
               12  LOAD_CLOSURE             'file_type'
               15  BUILD_TUPLE_2         2 
               18  LOAD_CODE                <code_object get_file_validator>
               21  LOAD_STR                 'ref_to_file_that_must_exist.<locals>.get_file_validator'
               24  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               30  STORE_FAST               'get_file_validator'

 L.  28        33  LOAD_GLOBAL              ArgumentsSdv
               36  LOAD_GLOBAL              list_sdvs
               39  LOAD_ATTR                from_string
               42  LOAD_GLOBAL              string_sdvs
               45  LOAD_ATTR                from_path_sdv
               48  LOAD_DEREF               'file_that_must_exist'
               51  CALL_FUNCTION_1       1  '1 positional, 0 named'
               54  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  29        57  LOAD_FAST                'get_file_validator'
               60  BUILD_TUPLE_1         1 
               63  CALL_FUNCTION_2       2  '2 positional, 0 named'
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def ref_to_path_that_must_exist--- This code section failed: ---

 L.  33         0  LOAD_GLOBAL              SymbolTable
                3  LOAD_GLOBAL              DdvValidator
                6  LOAD_CONST               ('symbols', 'return')
                9  LOAD_CLOSURE             'file_that_must_exist'
               12  BUILD_TUPLE_1         1 
               15  LOAD_CODE                <code_object get_file_validator>
               18  LOAD_STR                 'ref_to_path_that_must_exist.<locals>.get_file_validator'
               21  MAKE_CLOSURE_A_3_0        '0 positional, 0 keyword only, 3 annotated'
               27  STORE_FAST               'get_file_validator'

 L.  37        30  LOAD_GLOBAL              ArgumentsSdv
               33  LOAD_GLOBAL              list_sdvs
               36  LOAD_ATTR                from_string
               39  LOAD_GLOBAL              string_sdvs
               42  LOAD_ATTR                from_path_sdv
               45  LOAD_DEREF               'file_that_must_exist'
               48  CALL_FUNCTION_1       1  '1 positional, 0 named'
               51  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L.  38        54  LOAD_FAST                'get_file_validator'
               57  BUILD_TUPLE_1         1 
               60  CALL_FUNCTION_2       2  '2 positional, 0 named'
               63  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1