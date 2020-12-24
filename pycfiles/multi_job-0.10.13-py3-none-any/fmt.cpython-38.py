# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/utils/fmt.py
# Compiled at: 2020-01-30 09:01:17
# Size of source mod 2**32: 309 bytes
import os
from typing import Callable

def formatted_update--- This code section failed: ---

 L.   6         0  LOAD_DEREF               'callback'
                2  POP_JUMP_IF_FALSE    28  'to 28'

 L.   7         4  LOAD_CLOSURE             'b'
                6  LOAD_CLOSURE             'callback'
                8  BUILD_TUPLE_2         2 
               10  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               12  LOAD_STR                 'formatted_update.<locals>.<dictcomp>'
               14  MAKE_FUNCTION_8          'closure'
               16  LOAD_FAST                'a'
               18  LOAD_METHOD              items
               20  CALL_METHOD_0         0  ''
               22  GET_ITER         
               24  CALL_FUNCTION_1       1  ''
               26  RETURN_VALUE     
             28_0  COME_FROM             2  '2'

Parse error at or near `LOAD_DICTCOMP' instruction at offset 10


def join_paths(a: str, b: str) -> str:
    return os.path.abspath(os.path.join(a, b))