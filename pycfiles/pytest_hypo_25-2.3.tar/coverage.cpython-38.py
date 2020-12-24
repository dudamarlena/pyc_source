# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\coverage.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 3566 bytes
import json, os, sys
from contextlib import contextmanager
from typing import Dict, Set, Tuple
from hypothesis.internal.reflection import proxies
pretty_file_name_cache = {}

def pretty_file_name--- This code section failed: ---

 L.  41         0  SETUP_FINALLY        12  'to 12'

 L.  42         2  LOAD_GLOBAL              pretty_file_name_cache
                4  LOAD_FAST                'f'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  43        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    30  'to 30'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L.  44        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            18  '18'
               30  END_FINALLY      
             32_0  COME_FROM            28  '28'

 L.  46        32  LOAD_FAST                'f'
               34  LOAD_METHOD              split
               36  LOAD_GLOBAL              os
               38  LOAD_ATTR                path
               40  LOAD_ATTR                sep
               42  CALL_METHOD_1         1  ''
               44  STORE_FAST               'parts'

 L.  47        46  LOAD_STR                 'hypothesis'
               48  LOAD_FAST                'parts'
               50  COMPARE_OP               in
               52  POP_JUMP_IF_FALSE    84  'to 84'

 L.  48        54  LOAD_FAST                'parts'
               56  LOAD_FAST                'parts'
               58  LOAD_CONST               None
               60  LOAD_CONST               None
               62  LOAD_CONST               -1
               64  BUILD_SLICE_3         3 
               66  BINARY_SUBSCR    
               68  LOAD_METHOD              index
               70  LOAD_STR                 'hypothesis'
               72  CALL_METHOD_1         1  ''
               74  UNARY_NEGATIVE   
               76  LOAD_CONST               None
               78  BUILD_SLICE_2         2 
               80  BINARY_SUBSCR    
               82  STORE_FAST               'parts'
             84_0  COME_FROM            52  '52'

 L.  49        84  LOAD_GLOBAL              os
               86  LOAD_ATTR                path
               88  LOAD_ATTR                sep
               90  LOAD_METHOD              join
               92  LOAD_FAST                'parts'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'result'

 L.  50        98  LOAD_FAST                'result'
              100  LOAD_GLOBAL              pretty_file_name_cache
              102  LOAD_FAST                'f'
              104  STORE_SUBSCR     

 L.  51       106  LOAD_FAST                'result'
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 22


IN_COVERAGE_TESTS = os.getenv('HYPOTHESIS_INTERNAL_COVERAGE') == 'true'
if IN_COVERAGE_TESTS:
    written = set()

    def record_branch(name, value):
        key = (
         name, value)
        if key in written:
            return
        written.add(key)
        with open('branch-check', 'a') as (log):
            log.write(json.dumps({'name':name,  'value':value}) + '\n')


    description_stack = []

    @contextmanager
    def check_block(name, depth):
        caller = sys._getframe(depth + 2)
        local_description = '%s at %s:%d' % (
         name,
         pretty_file_name(caller.f_code.co_filename),
         caller.f_lineno)
        try:
            try:
                description_stack.append(local_description)
                description = ' in '.join(reversed(description_stack)) + ' passed'
                yield
                record_branch(description, True)
            except BaseException:
                record_branch(description, False)
                raise

        finally:
            description_stack.pop()


    @contextmanager
    def check(name):
        with check_block(name, 2):
            yield


    def check_function(f):

        @proxies(f)
        def accept--- This code section failed: ---

 L. 104         0  LOAD_GLOBAL              check_block
                2  LOAD_DEREF               'f'
                4  LOAD_ATTR                __name__
                6  LOAD_CONST               2
                8  CALL_FUNCTION_2       2  ''
               10  SETUP_WITH           36  'to 36'
               12  POP_TOP          

 L. 105        14  LOAD_DEREF               'f'
               16  LOAD_FAST                'args'
               18  LOAD_FAST                'kwargs'
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  POP_BLOCK        
               24  ROT_TWO          
               26  BEGIN_FINALLY    
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  POP_FINALLY           0  ''
               34  RETURN_VALUE     
             36_0  COME_FROM_WITH       10  '10'
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 24

        return accept


else:

    def check_function(f):
        return f


    @contextmanager
    def check(name):
        (yield)