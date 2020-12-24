# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/execution/sandbox_dir_resolving.py
# Compiled at: 2018-07-07 05:02:31
# Size of source mod 2**32: 276 bytes
import tempfile
from typing import Callable
SandboxRootDirNameResolver = Callable[([], str)]

def mk_tmp_dir_with_prefix--- This code section failed: ---

 L.   8         0  LOAD_GLOBAL              str
                3  LOAD_CONST               ('return',)
                6  LOAD_CLOSURE             'dir_name_prefix'
                9  BUILD_TUPLE_1         1 
               12  LOAD_CODE                <code_object ret_val>
               15  LOAD_STR                 'mk_tmp_dir_with_prefix.<locals>.ret_val'
               18  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               24  STORE_FAST               'ret_val'

 L.  11        27  LOAD_FAST                'ret_val'
               30  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1