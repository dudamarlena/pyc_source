# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/data/path_description.py
# Compiled at: 2020-01-20 02:27:16
# Size of source mod 2**32: 3434 bytes
import pathlib
from typing import Optional
from exactly_lib.test_case_file_structure import path_relativity as pr
from exactly_lib.test_case_file_structure import relative_path_options as rpo
from exactly_lib.test_case_file_structure.path_relativity import RelOptionType
from exactly_lib.test_case_file_structure.tcds import Tcds
from exactly_lib.type_system.data.path_ddv import PathDdv
EXACTLY_SANDBOX_ROOT_DIR_NAME = 'EXACTLY_SANDBOX'

def _with_prefix(prefix: str, path_ddv: PathDdv) -> str:
    return str(pathlib.PurePosixPath(prefix, path_ddv.path_suffix().value()))


def path_ddv_with_relativity_name_prefix__rel_tcds_dir(path_ddv: PathDdv) -> str:
    relativity_type = path_ddv.relativity().relativity_type
    if relativity_type is None:
        raise ValueError('path is absolute')
    if relativity_type is RelOptionType.REL_CWD:
        raise ValueError('path is relative ' + str(RelOptionType.REL_CWD))
    rel_hds_opt = pr.rel_hds_from_rel_any(relativity_type)
    if rel_hds_opt is not None:
        return _with_prefix(rpo.REL_HDS_OPTIONS_MAP[rel_hds_opt].directory_symbol_reference, path_ddv)
    rel_sds_opt = pr.rel_sds_from_rel_any(relativity_type)
    if rel_sds_opt is not None:
        return _with_prefix(rpo.REL_SDS_OPTIONS_MAP[rel_sds_opt].directory_symbol_reference, path_ddv)
    raise ValueError('undefined relativity of {}: {}: '.format(path_ddv, relativity_type))


def path_ddv_with_relativity_name_prefix--- This code section failed: ---

 L.  44         0  LOAD_GLOBAL              str
                3  LOAD_CONST               ('return',)
                6  LOAD_CLOSURE             'path_ddv'
                9  BUILD_TUPLE_1         1 
               12  LOAD_CODE                <code_object absolute>
               15  LOAD_STR                 'path_ddv_with_relativity_name_prefix.<locals>.absolute'
               18  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               24  STORE_FAST               'absolute'

 L.  47        27  LOAD_GLOBAL              str
               30  LOAD_CONST               ('return',)
               33  LOAD_CLOSURE             'cwd'
               36  LOAD_CLOSURE             'path_ddv'
               39  LOAD_CLOSURE             'tcds'
               42  BUILD_TUPLE_3         3 
               45  LOAD_CODE                <code_object rel_cwd>
               48  LOAD_STR                 'path_ddv_with_relativity_name_prefix.<locals>.rel_cwd'
               51  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               57  STORE_FAST               'rel_cwd'

 L.  78        60  LOAD_DEREF               'path_ddv'
               63  LOAD_ATTR                relativity
               66  CALL_FUNCTION_0       0  '0 positional, 0 named'
               69  STORE_FAST               'relativity'

 L.  80        72  LOAD_FAST                'relativity'
               75  LOAD_ATTR                is_absolute
               78  POP_JUMP_IF_FALSE    88  'to 88'

 L.  81        81  LOAD_FAST                'absolute'
               84  CALL_FUNCTION_0       0  '0 positional, 0 named'
               87  RETURN_END_IF    
             88_0  COME_FROM            78  '78'

 L.  83        88  LOAD_FAST                'relativity'
               91  LOAD_ATTR                relativity_type
               94  STORE_FAST               'relativity_type'

 L.  85        97  LOAD_FAST                'relativity_type'
              100  LOAD_GLOBAL              pr
              103  LOAD_ATTR                RelOptionType
              106  LOAD_ATTR                REL_CWD
              109  COMPARE_OP               is
              112  POP_JUMP_IF_FALSE   122  'to 122'

 L.  86       115  LOAD_FAST                'rel_cwd'
              118  CALL_FUNCTION_0       0  '0 positional, 0 named'
              121  RETURN_END_IF    
            122_0  COME_FROM           112  '112'

 L.  88       122  LOAD_GLOBAL              path_ddv_with_relativity_name_prefix__rel_tcds_dir
              125  LOAD_DEREF               'path_ddv'
              128  CALL_FUNCTION_1       1  '1 positional, 0 named'
              131  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1