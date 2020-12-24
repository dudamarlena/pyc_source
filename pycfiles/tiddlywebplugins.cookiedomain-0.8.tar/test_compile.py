# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.cookiedomain/test/test_compile.py
# Compiled at: 2010-04-29 08:49:36


def test_compile--- This code section failed: ---

 L.   5         0  SETUP_EXCEPT         28  'to 31'

 L.   6         3  LOAD_CONST               -1
                6  LOAD_CONST               None
                9  IMPORT_NAME           0  'tiddlywebplugins.cookiedomain'
               12  STORE_FAST            0  'tiddlywebplugins'

 L.   7        15  LOAD_GLOBAL           1  'True'
               18  POP_JUMP_IF_TRUE     27  'to 27'
               21  LOAD_ASSERT              AssertionError
               24  RAISE_VARARGS_1       1  None
               27  POP_BLOCK        
               28  JUMP_FORWARD         34  'to 65'
             31_0  COME_FROM             0  '0'

 L.   8        31  DUP_TOP          
               32  LOAD_GLOBAL           3  'ImportError'
               35  COMPARE_OP           10  exception-match
               38  POP_JUMP_IF_FALSE    64  'to 64'
               41  POP_TOP          
               42  STORE_FAST            1  'exc'
               45  POP_TOP          

 L.   9        46  LOAD_GLOBAL           4  'False'
               49  POP_JUMP_IF_TRUE     65  'to 65'
               52  LOAD_ASSERT              AssertionError
               55  LOAD_FAST             1  'exc'
               58  RAISE_VARARGS_2       2  None
               61  JUMP_FORWARD          1  'to 65'
               64  END_FINALLY      
             65_0  COME_FROM            64  '64'
             65_1  COME_FROM            28  '28'

Parse error at or near `END_FINALLY' instruction at offset 64