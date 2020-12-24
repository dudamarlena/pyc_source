# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/manifestopheles/test/test_example.py
# Compiled at: 2013-01-21 13:39:24
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_compile--- This code section failed: ---

 L.   4         0  SETUP_EXCEPT        118  'to 121'

 L.   5         3  LOAD_CONST               -1
                6  LOAD_CONST               None
                9  IMPORT_NAME           0  'tiddlywebplugins.manifestopheles'
               12  STORE_FAST            0  'tiddlywebplugins'

 L.   6        15  LOAD_GLOBAL           1  'True'
               18  POP_JUMP_IF_TRUE    117  'to 117'
               21  LOAD_CONST               'assert %(py0)s'
               24  BUILD_MAP_1           1  None
               27  LOAD_CONST               'True'
               30  LOAD_GLOBAL           2  '@py_builtins'
               33  LOAD_ATTR             3  'locals'
               36  CALL_FUNCTION_0       0  None
               39  DUP_TOP          
               40  ROT_THREE        
               41  COMPARE_OP            6  in
               44  JUMP_IF_FALSE_OR_POP    62  'to 62'
               47  LOAD_GLOBAL           2  '@py_builtins'
               50  LOAD_ATTR             4  'globals'
               53  CALL_FUNCTION_0       0  None
               56  COMPARE_OP            9  is-not
               59  JUMP_FORWARD          2  'to 64'
             62_0  COME_FROM            44  '44'
               62  ROT_TWO          
               63  POP_TOP          
             64_0  COME_FROM            59  '59'
               64  POP_JUMP_IF_FALSE    82  'to 82'
               67  LOAD_GLOBAL           5  '@pytest_ar'
               70  LOAD_ATTR             6  '_saferepr'
               73  LOAD_GLOBAL           1  'True'
               76  CALL_FUNCTION_1       1  None
               79  JUMP_FORWARD          3  'to 85'
               82  LOAD_CONST               'True'
             85_0  COME_FROM            79  '79'
               85  LOAD_CONST               'py0'
               88  STORE_MAP        
               89  BINARY_MODULO    
               90  STORE_FAST            1  '@py_format1'
               93  LOAD_GLOBAL           7  'AssertionError'
               96  LOAD_GLOBAL           5  '@pytest_ar'
               99  LOAD_ATTR             8  '_format_explanation'
              102  LOAD_FAST             1  '@py_format1'
              105  CALL_FUNCTION_1       1  None
              108  CALL_FUNCTION_1       1  None
              111  RAISE_VARARGS_1       1  None
              114  JUMP_FORWARD          0  'to 117'
            117_0  COME_FROM           114  '114'
              117  POP_BLOCK        
              118  JUMP_FORWARD         34  'to 155'
            121_0  COME_FROM             0  '0'

 L.   7       121  DUP_TOP          
              122  LOAD_GLOBAL           9  'ImportError'
              125  COMPARE_OP           10  exception-match
              128  POP_JUMP_IF_FALSE   154  'to 154'
              131  POP_TOP          
              132  STORE_FAST            2  'exc'
              135  POP_TOP          

 L.   8       136  LOAD_GLOBAL          10  'False'
              139  POP_JUMP_IF_TRUE    155  'to 155'
              142  LOAD_ASSERT              AssertionError
              145  LOAD_FAST             2  'exc'
              148  RAISE_VARARGS_2       2  None
              151  JUMP_FORWARD          1  'to 155'
              154  END_FINALLY      
            155_0  COME_FROM           154  '154'
            155_1  COME_FROM           118  '118'

Parse error at or near `END_FINALLY' instruction at offset 154