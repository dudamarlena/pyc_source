# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klmitch/devel/src/dtest/tests/__init__.py
# Compiled at: 2011-04-11 11:42:21
t_order = []

def setUp--- This code section failed: ---

 L.  21         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  't_order'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_CONST               0
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               'Ordering error running test suite'
               24  RAISE_VARARGS_2       2  None

 L.  24        27  LOAD_GLOBAL           1  't_order'
               30  LOAD_ATTR             3  'append'
               33  LOAD_CONST               'tests.setUp'
               36  CALL_FUNCTION_1       1  None
               39  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 36


def tearDown--- This code section failed: ---

 L.  29         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  't_order'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_CONST               13
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               'Ordering error running test suite'
               24  RAISE_VARARGS_2       2  None

 L.  30        27  LOAD_GLOBAL           1  't_order'
               30  LOAD_CONST               -1
               33  BINARY_SUBSCR    
               34  LOAD_CONST               'tests.ordering.tearDown'
               37  COMPARE_OP            2  ==
               40  POP_JUMP_IF_TRUE     52  'to 52'
               43  LOAD_ASSERT              AssertionError
               46  LOAD_CONST               'Incorrect previous step'
               49  RAISE_VARARGS_2       2  None

 L.  33        52  LOAD_GLOBAL           1  't_order'
               55  LOAD_ATTR             3  'append'
               58  LOAD_CONST               'tests.tearDown'
               61  CALL_FUNCTION_1       1  None
               64  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 61