# uncompyle6 version 3.7.4
# PyPy Python bytecode 3.2 (3187)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewcrosio/projects/pathresolver/pypy3/site-packages/pathresolver/resolver/key.py
# Compiled at: 2015-04-17 13:50:21
from .base import ResolverBase
from pathresolver.exceptions import UnableToResolve

class KeyResolver(ResolverBase):

    def __init__(self, func, failure_exc):
        self.func = func
        self.failure_exc = failure_exc

    def resolve--- This code section failed: ---

 L.  11         0  SETUP_EXCEPT         19  'to 19'

 L.  12         3  LOAD_FAST                'self'
                6  LOOKUP_METHOD            func
                9  LOAD_FAST                'key'
               12  LOAD_FAST                'value'
               15  CALL_METHOD_2         2 
               18  RETURN_VALUE     
             19_0  COME_FROM_EXCEPT      0  '0'

 L.  13        19  DUP_TOP          
               20  LOAD_FAST                'self'
               23  LOAD_ATTR                failure_exc
               26  COMPARE_OP               exception-match
               29  POP_JUMP_IF_FALSE    69  'to 69'
               32  POP_TOP          
               33  POP_TOP          
               34  POP_TOP          

 L.  14        35  LOAD_GLOBAL              UnableToResolve
               38  LOAD_STR                 'Cannot find {key} in {value}'
               41  LOOKUP_METHOD            format
               44  LOAD_STR                 'key'
               47  LOAD_FAST                'key'
               50  LOAD_STR                 'value'
               53  LOAD_FAST                'value'
               56  CALL_METHOD_512     512 
               59  CALL_FUNCTION_1       1  '1 positional, 0 named'
               62  RAISE_VARARGS_1       1  ''
               65  POP_EXCEPT       
               66  JUMP_FORWARD         70  'to 70'
               69  END_FINALLY      
             70_0  COME_FROM            66  '66'

Parse error at or near `COME_FROM_EXCEPT' instruction at offset 19_0