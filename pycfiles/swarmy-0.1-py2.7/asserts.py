# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/swarmy/asserts.py
# Compiled at: 2011-09-23 11:14:27


def assert_lists_eq--- This code section failed: ---

 L.   3         0  LOAD_FAST             2  'strict'
                3  POP_JUMP_IF_FALSE    95  'to 95'

 L.   4         6  LOAD_GLOBAL           0  'type'
                9  LOAD_FAST             0  'l1'
               12  CALL_FUNCTION_1       1  None
               15  LOAD_GLOBAL           1  'list'
               18  COMPARE_OP            2  ==
               21  POP_JUMP_IF_TRUE     49  'to 49'
               24  LOAD_ASSERT              AssertionError
               27  LOAD_CONST               'Expected a list for arg 0, got %s.'
               30  LOAD_GLOBAL           3  'str'
               33  LOAD_GLOBAL           0  'type'
               36  LOAD_FAST             0  'l1'
               39  CALL_FUNCTION_1       1  None
               42  CALL_FUNCTION_1       1  None
               45  BINARY_MODULO    
               46  RAISE_VARARGS_2       2  None

 L.   5        49  LOAD_GLOBAL           0  'type'
               52  LOAD_FAST             1  'l2'
               55  CALL_FUNCTION_1       1  None
               58  LOAD_GLOBAL           1  'list'
               61  COMPARE_OP            2  ==
               64  POP_JUMP_IF_TRUE     95  'to 95'
               67  LOAD_ASSERT              AssertionError
               70  LOAD_CONST               'Expected a list for arg 1, got %s.'
               73  LOAD_GLOBAL           3  'str'
               76  LOAD_GLOBAL           0  'type'
               79  LOAD_FAST             1  'l2'
               82  CALL_FUNCTION_1       1  None
               85  CALL_FUNCTION_1       1  None
               88  BINARY_MODULO    
               89  RAISE_VARARGS_2       2  None
               92  JUMP_FORWARD          0  'to 95'
             95_0  COME_FROM            92  '92'

 L.   6        95  LOAD_GLOBAL           4  'len'
               98  LOAD_FAST             0  'l1'
              101  CALL_FUNCTION_1       1  None
              104  LOAD_GLOBAL           4  'len'
              107  LOAD_FAST             1  'l2'
              110  CALL_FUNCTION_1       1  None
              113  COMPARE_OP            2  ==
              116  POP_JUMP_IF_TRUE    150  'to 150'
              119  LOAD_ASSERT              AssertionError
              122  LOAD_CONST               'Expected %d elements, Got %d elements'
              125  LOAD_GLOBAL           4  'len'
              128  LOAD_FAST             1  'l2'
              131  CALL_FUNCTION_1       1  None
              134  LOAD_GLOBAL           4  'len'
              137  LOAD_FAST             0  'l1'
              140  CALL_FUNCTION_1       1  None
              143  BUILD_TUPLE_2         2 
              146  BINARY_MODULO    
              147  RAISE_VARARGS_2       2  None

 L.   7       150  SETUP_LOOP           68  'to 221'
              153  LOAD_GLOBAL           5  'enumerate'
              156  LOAD_FAST             0  'l1'
              159  CALL_FUNCTION_1       1  None
              162  GET_ITER         
              163  FOR_ITER             54  'to 220'
              166  UNPACK_SEQUENCE_2     2 
              169  STORE_FAST            3  'i'
              172  STORE_FAST            4  'element'

 L.   8       175  LOAD_FAST             4  'element'
              178  LOAD_FAST             1  'l2'
              181  LOAD_FAST             3  'i'
              184  BINARY_SUBSCR    
              185  COMPARE_OP            2  ==
              188  POP_JUMP_IF_TRUE    163  'to 163'
              191  LOAD_ASSERT              AssertionError
              194  LOAD_CONST               "At index %d, Expected '%s', Got '%s'"
              197  LOAD_FAST             3  'i'
              200  LOAD_FAST             1  'l2'
              203  LOAD_FAST             3  'i'
              206  BINARY_SUBSCR    
              207  LOAD_FAST             4  'element'
              210  BUILD_TUPLE_3         3 
              213  BINARY_MODULO    
              214  RAISE_VARARGS_2       2  None
              217  JUMP_BACK           163  'to 163'
              220  POP_BLOCK        
            221_0  COME_FROM           150  '150'

Parse error at or near `POP_BLOCK' instruction at offset 220


def assert_dicts_eq--- This code section failed: ---

 L.  11         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             0  'd1'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  'dict'
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               'First argument is not a dict()'
               24  RAISE_VARARGS_2       2  None

 L.  12        27  LOAD_GLOBAL           0  'type'
               30  LOAD_FAST             1  'd2'
               33  CALL_FUNCTION_1       1  None
               36  LOAD_GLOBAL           1  'dict'
               39  COMPARE_OP            2  ==
               42  POP_JUMP_IF_TRUE     54  'to 54'
               45  LOAD_ASSERT              AssertionError
               48  LOAD_CONST               'Second argument is not a dict()'
               51  RAISE_VARARGS_2       2  None

 L.  13        54  LOAD_GLOBAL           3  'len'
               57  LOAD_FAST             0  'd1'
               60  LOAD_ATTR             4  'keys'
               63  CALL_FUNCTION_0       0  None
               66  CALL_FUNCTION_1       1  None
               69  LOAD_GLOBAL           3  'len'
               72  LOAD_FAST             1  'd2'
               75  LOAD_ATTR             4  'keys'
               78  CALL_FUNCTION_0       0  None
               81  CALL_FUNCTION_1       1  None
               84  COMPARE_OP            2  ==
               87  POP_JUMP_IF_TRUE    133  'to 133'
               90  LOAD_ASSERT              AssertionError

 L.  14        93  LOAD_CONST               'Got %d keys. Expected %d keys.'
               96  LOAD_GLOBAL           3  'len'
               99  LOAD_FAST             0  'd1'
              102  LOAD_ATTR             4  'keys'
              105  CALL_FUNCTION_0       0  None
              108  CALL_FUNCTION_1       1  None
              111  LOAD_GLOBAL           3  'len'
              114  LOAD_FAST             1  'd2'
              117  LOAD_ATTR             4  'keys'
              120  CALL_FUNCTION_0       0  None
              123  CALL_FUNCTION_1       1  None
              126  BUILD_TUPLE_2         2 
              129  BINARY_MODULO    
              130  RAISE_VARARGS_2       2  None

 L.  15       133  SETUP_LOOP           98  'to 234'
              136  LOAD_FAST             0  'd1'
              139  LOAD_ATTR             5  'iteritems'
              142  CALL_FUNCTION_0       0  None
              145  GET_ITER         
              146  FOR_ITER             84  'to 233'
              149  UNPACK_SEQUENCE_2     2 
              152  STORE_FAST            2  'k'
              155  STORE_FAST            3  'v'

 L.  16       158  LOAD_FAST             2  'k'
              161  LOAD_FAST             1  'd2'
              164  COMPARE_OP            6  in
              167  POP_JUMP_IF_TRUE    183  'to 183'
              170  LOAD_ASSERT              AssertionError
              173  LOAD_CONST               'Got unexpected key %s'
              176  LOAD_FAST             2  'k'
              179  BINARY_MODULO    
              180  RAISE_VARARGS_2       2  None

 L.  17       183  LOAD_FAST             0  'd1'
              186  LOAD_FAST             2  'k'
              189  BINARY_SUBSCR    
              190  LOAD_FAST             1  'd2'
              193  LOAD_FAST             2  'k'
              196  BINARY_SUBSCR    
              197  COMPARE_OP            2  ==
              200  POP_JUMP_IF_TRUE    146  'to 146'
              203  LOAD_ASSERT              AssertionError
              206  LOAD_CONST               "'%s' != '%s'"
              209  LOAD_FAST             0  'd1'
              212  LOAD_FAST             2  'k'
              215  BINARY_SUBSCR    
              216  LOAD_FAST             1  'd2'
              219  LOAD_FAST             2  'k'
              222  BINARY_SUBSCR    
              223  BUILD_TUPLE_2         2 
              226  BINARY_MODULO    
              227  RAISE_VARARGS_2       2  None
              230  JUMP_BACK           146  'to 146'
              233  POP_BLOCK        
            234_0  COME_FROM           133  '133'

Parse error at or near `POP_BLOCK' instruction at offset 233