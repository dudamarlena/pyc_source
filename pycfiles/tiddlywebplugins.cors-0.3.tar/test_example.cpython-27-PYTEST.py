# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.cors/test/test_example.py
# Compiled at: 2012-04-14 09:43:34
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

def test_compile--- This code section failed: ---

 L.   2         0  SETUP_EXCEPT         16  'to 19'

 L.   3         3  LOAD_CONST               -1
                6  LOAD_CONST               None
                9  IMPORT_NAME           0  'tiddlywebplugins.cors'
               12  STORE_FAST            0  'tiddlywebplugins'
               15  POP_BLOCK        
               16  JUMP_FORWARD         38  'to 57'
             19_0  COME_FROM             0  '0'

 L.   4        19  DUP_TOP          
               20  LOAD_GLOBAL           1  'ImportError'
               23  COMPARE_OP           10  exception-match
               26  POP_JUMP_IF_FALSE    56  'to 56'
               29  POP_TOP          
               30  STORE_FAST            1  'exc'
               33  POP_TOP          

 L.   5        34  LOAD_GLOBAL           2  'False'
               37  POP_JUMP_IF_TRUE     57  'to 57'
               40  LOAD_ASSERT              AssertionError
               43  LOAD_CONST               'unable to import tiddlywebplugins.cors: %s'
               46  LOAD_FAST             1  'exc'
               49  BINARY_MODULO    
               50  RAISE_VARARGS_2       2  None
               53  JUMP_FORWARD          1  'to 57'
               56  END_FINALLY      
             57_0  COME_FROM            56  '56'
             57_1  COME_FROM            16  '16'

Parse error at or near `END_FINALLY' instruction at offset 56