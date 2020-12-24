# uncompyle6 version 3.7.4
# PyPy Python bytecode 3.2 (3187)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewcrosio/projects/pathresolver/pypy3/site-packages/pathresolver/resolver/multi.py
# Compiled at: 2015-04-17 13:50:21
from .key import KeyResolver
from pathresolver.exceptions import UnableToResolve

class MultiKeyResolver(KeyResolver):

    def __init__(self, *resolvers):
        self.resolvers = resolvers
        super(MultiKeyResolver, self).__init__(self.resolve_multi, UnableToResolve)

    def resolve_multi--- This code section failed: ---

 L.  11         0  SETUP_LOOP           57  'to 57'
                3  LOAD_FAST                'self'
                6  LOAD_ATTR                resolvers
                9  GET_ITER         

 L.  11        10  FOR_ITER             56  'to 56'
               13  STORE_FAST               'resolver'

 L.  12        16  SETUP_EXCEPT         35  'to 35'

 L.  13        19  LOAD_FAST                'resolver'
               22  LOOKUP_METHOD            resolve
               25  LOAD_FAST                'key'
               28  LOAD_FAST                'value'
               31  CALL_METHOD_2         2 
               34  RETURN_VALUE     
             35_0  COME_FROM_EXCEPT     16  '16'

 L.  14        35  DUP_TOP          
               36  LOAD_GLOBAL              UnableToResolve
               39  COMPARE_OP               exception-match
               42  POP_JUMP_IF_FALSE    52  'to 52'
               45  POP_TOP          
               46  POP_TOP          
               47  POP_TOP          

 L.  15        48  POP_EXCEPT       
               49  JUMP_BACK            10  'to 10'
               52  END_FINALLY      
               53  JUMP_BACK            10  'to 10'
               56  POP_BLOCK        
             57_0  COME_FROM_LOOP        0  '0'

 L.  18        57  LOAD_GLOBAL              UnableToResolve
               60  LOAD_STR                 'Cannot find {key} in {value}'
               63  LOOKUP_METHOD            format
               66  LOAD_STR                 'key'
               69  LOAD_FAST                'key'
               72  LOAD_STR                 'value'
               75  LOAD_FAST                'value'
               78  CALL_METHOD_512     512 
               81  CALL_FUNCTION_1       1  '1 positional, 0 named'
               84  RAISE_VARARGS_1       1  ''

Parse error at or near `COME_FROM_EXCEPT' instruction at offset 35_0