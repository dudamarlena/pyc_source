# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\utils\unstruct.py
# Compiled at: 2013-01-14 06:47:43
"""
Unstructured view of a structured array whose fields are all of the same type.
"""
import numpy as np

def unstruct--- This code section failed: ---

 L.  75         0  LOAD_GLOBAL           0  'np'
                3  LOAD_ATTR             1  'asanyarray'
                6  LOAD_FAST             0  'x'
                9  CALL_FUNCTION_1       1  None
               12  STORE_FAST            0  'x'

 L.  76        15  LOAD_FAST             0  'x'
               18  LOAD_ATTR             2  'dtype'
               21  LOAD_GLOBAL           3  'object'
               24  COMPARE_OP            2  ==
               27  POP_JUMP_IF_FALSE    76  'to 76'

 L.  77        30  LOAD_GLOBAL           0  'np'
               33  LOAD_ATTR             4  'concatenate'
               36  BUILD_LIST_0          0 
               39  LOAD_FAST             0  'x'
               42  GET_ITER         
               43  FOR_ITER             21  'to 67'
               46  STORE_FAST            1  'i'
               49  LOAD_GLOBAL           0  'np'
               52  LOAD_ATTR             5  'atleast_1d'
               55  LOAD_FAST             1  'i'
               58  CALL_FUNCTION_1       1  None
               61  LIST_APPEND           2  None
               64  JUMP_BACK            43  'to 43'
               67  CALL_FUNCTION_1       1  None
               70  STORE_FAST            0  'x'
               73  JUMP_FORWARD          0  'to 76'
             76_0  COME_FROM            73  '73'

 L.  78        76  LOAD_FAST             0  'x'
               79  LOAD_ATTR             2  'dtype'
               82  LOAD_ATTR             6  'fields'
               85  LOAD_CONST               None
               88  COMPARE_OP            8  is
               91  POP_JUMP_IF_FALSE    98  'to 98'

 L.  79        94  LOAD_FAST             0  'x'
               97  RETURN_END_IF    
             98_0  COME_FROM            91  '91'

 L.  80        98  LOAD_GLOBAL           0  'np'
              101  LOAD_ATTR             8  'array'
              104  BUILD_LIST_0          0 
              107  LOAD_FAST             0  'x'
              110  LOAD_ATTR             2  'dtype'
              113  LOAD_ATTR             6  'fields'
              116  LOAD_ATTR             9  'values'
              119  CALL_FUNCTION_0       0  None
              122  GET_ITER         
              123  FOR_ITER             16  'to 142'
              126  STORE_FAST            2  't'
              129  LOAD_FAST             2  't'
              132  LOAD_CONST               0
              135  BINARY_SUBSCR    
              136  LIST_APPEND           2  None
              139  JUMP_BACK           123  'to 123'
              142  CALL_FUNCTION_1       1  None
              145  STORE_FAST            3  'types'

 L.  81       148  LOAD_FAST             3  'types'
              151  LOAD_CONST               0
              154  BINARY_SUBSCR    
              155  STORE_FAST            4  'fieldtype'

 L.  82       158  LOAD_CONST               'One or more fields has a different type or shape than the first: %s'
              161  STORE_FAST            5  'msg'

 L.  83       164  LOAD_FAST             3  'types'
              167  LOAD_FAST             4  'fieldtype'
              170  COMPARE_OP            2  ==
              173  LOAD_ATTR            10  'all'
              176  CALL_FUNCTION_0       0  None
              179  POP_JUMP_IF_TRUE    198  'to 198'
              182  LOAD_ASSERT              AssertionError
              185  LOAD_FAST             5  'msg'
              188  LOAD_FAST             0  'x'
              191  LOAD_ATTR             2  'dtype'
              194  BINARY_MODULO    
              195  RAISE_VARARGS_2       2  None

 L.  84       198  LOAD_FAST             4  'fieldtype'
              201  LOAD_ATTR            12  'shape'
              204  STORE_FAST            6  'fieldshape'

 L.  85       207  LOAD_FAST             6  'fieldshape'
              210  POP_JUMP_IF_FALSE   231  'to 231'

 L.  86       213  LOAD_FAST             4  'fieldtype'
              216  LOAD_ATTR            13  'subdtype'
              219  UNPACK_SEQUENCE_2     2 
              222  STORE_FAST            4  'fieldtype'
              225  STORE_FAST            7  '_'
              228  JUMP_FORWARD          0  'to 231'
            231_0  COME_FROM           228  '228'

 L.  87       231  LOAD_FAST             0  'x'
              234  LOAD_ATTR            12  'shape'
              237  LOAD_GLOBAL          14  'len'
              240  LOAD_FAST             3  'types'
              243  CALL_FUNCTION_1       1  None
              246  BUILD_TUPLE_1         1 
              249  BINARY_ADD       
              250  LOAD_FAST             6  'fieldshape'
              253  BINARY_ADD       
              254  STORE_FAST            8  'shape'

 L.  91       257  LOAD_GLOBAL           0  'np'
              260  LOAD_ATTR             5  'atleast_1d'
              263  LOAD_FAST             0  'x'
              266  CALL_FUNCTION_1       1  None
              269  STORE_FAST            0  'x'

 L.  92       272  LOAD_FAST             0  'x'
              275  LOAD_ATTR            15  'view'
              278  LOAD_FAST             4  'fieldtype'
              281  CALL_FUNCTION_1       1  None
              284  STORE_FAST            9  'xv'

 L.  93       287  LOAD_FAST             9  'xv'
              290  LOAD_ATTR            16  'reshape'
              293  LOAD_FAST             8  'shape'
              296  CALL_FUNCTION_1       1  None
              299  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_1' instruction at offset 296


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)