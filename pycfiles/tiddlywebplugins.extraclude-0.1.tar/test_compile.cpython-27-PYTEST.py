# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.extraclude/test/test_compile.py
# Compiled at: 2014-02-10 10:04:01
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_compile--- This code section failed: ---

 L.   5         0  SETUP_EXCEPT        111  'to 114'

 L.   6         3  LOAD_CONST               -1
                6  LOAD_CONST               None
                9  IMPORT_NAME           0  'tiddlywebplugins.extraclude'
               12  STORE_FAST            0  'tiddlywebplugins'

 L.   7        15  LOAD_GLOBAL           1  'True'
               18  POP_JUMP_IF_TRUE    110  'to 110'
               21  LOAD_CONST               'assert %(py0)s'
               24  BUILD_MAP_1           1  None
               27  LOAD_CONST               'True'
               30  LOAD_GLOBAL           2  '@py_builtins'
               33  LOAD_ATTR             3  'locals'
               36  CALL_FUNCTION_0       0  None
               39  COMPARE_OP            6  in
               42  POP_JUMP_IF_TRUE     60  'to 60'
               45  LOAD_GLOBAL           4  '@pytest_ar'
               48  LOAD_ATTR             5  '_should_repr_global_name'
               51  LOAD_GLOBAL           1  'True'
               54  CALL_FUNCTION_1       1  None
             57_0  COME_FROM            42  '42'
               57  POP_JUMP_IF_FALSE    75  'to 75'
               60  LOAD_GLOBAL           4  '@pytest_ar'
               63  LOAD_ATTR             6  '_saferepr'
               66  LOAD_GLOBAL           1  'True'
               69  CALL_FUNCTION_1       1  None
               72  JUMP_FORWARD          3  'to 78'
               75  LOAD_CONST               'True'
             78_0  COME_FROM            72  '72'
               78  LOAD_CONST               'py0'
               81  STORE_MAP        
               82  BINARY_MODULO    
               83  STORE_FAST            1  '@py_format1'
               86  LOAD_GLOBAL           7  'AssertionError'
               89  LOAD_GLOBAL           4  '@pytest_ar'
               92  LOAD_ATTR             8  '_format_explanation'
               95  LOAD_FAST             1  '@py_format1'
               98  CALL_FUNCTION_1       1  None
              101  CALL_FUNCTION_1       1  None
              104  RAISE_VARARGS_1       1  None
              107  JUMP_FORWARD          0  'to 110'
            110_0  COME_FROM           107  '107'
              110  POP_BLOCK        
              111  JUMP_FORWARD         34  'to 148'
            114_0  COME_FROM             0  '0'

 L.   8       114  DUP_TOP          
              115  LOAD_GLOBAL           9  'ImportError'
              118  COMPARE_OP           10  exception-match
              121  POP_JUMP_IF_FALSE   147  'to 147'
              124  POP_TOP          
              125  STORE_FAST            2  'exc'
              128  POP_TOP          

 L.   9       129  LOAD_GLOBAL          10  'False'
              132  POP_JUMP_IF_TRUE    148  'to 148'
              135  LOAD_ASSERT              AssertionError
              138  LOAD_FAST             2  'exc'
              141  RAISE_VARARGS_2       2  None
              144  JUMP_FORWARD          1  'to 148'
              147  END_FINALLY      
            148_0  COME_FROM           147  '147'
            148_1  COME_FROM           111  '111'

Parse error at or near `END_FINALLY' instruction at offset 147