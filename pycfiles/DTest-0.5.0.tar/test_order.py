# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klmitch/devel/src/dtest/tests/ordering/test_order.py
# Compiled at: 2011-04-11 14:50:36
import dtest, tests

def setUp--- This code section failed: ---

 L.  24         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  'tests'
                6  LOAD_ATTR             2  't_order'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               2
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     30  'to 30'
               21  LOAD_ASSERT              AssertionError
               24  LOAD_CONST               'Ordering error running test suite'
               27  RAISE_VARARGS_2       2  None

 L.  25        30  LOAD_GLOBAL           1  'tests'
               33  LOAD_ATTR             2  't_order'
               36  LOAD_CONST               -1
               39  BINARY_SUBSCR    
               40  LOAD_CONST               'tests.ordering.setUp'
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_TRUE     58  'to 58'
               49  LOAD_ASSERT              AssertionError

 L.  26        52  LOAD_CONST               'Incorrect previous step'
               55  RAISE_VARARGS_2       2  None

 L.  29        58  LOAD_GLOBAL           1  'tests'
               61  LOAD_ATTR             2  't_order'
               64  LOAD_ATTR             4  'append'
               67  LOAD_CONST               'tests.ordering.test_order.setUp'
               70  CALL_FUNCTION_1       1  None
               73  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 70


def tearDown--- This code section failed: ---

 L.  34         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  'tests'
                6  LOAD_ATTR             2  't_order'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               11
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     30  'to 30'
               21  LOAD_ASSERT              AssertionError
               24  LOAD_CONST               'Ordering error running test suite'
               27  RAISE_VARARGS_2       2  None

 L.  35        30  LOAD_GLOBAL           1  'tests'
               33  LOAD_ATTR             2  't_order'
               36  LOAD_CONST               -1
               39  BINARY_SUBSCR    
               40  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.tearDownClass'
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_TRUE     58  'to 58'
               49  LOAD_ASSERT              AssertionError

 L.  37        52  LOAD_CONST               'Incorrect previous step'
               55  RAISE_VARARGS_2       2  None

 L.  40        58  LOAD_GLOBAL           1  'tests'
               61  LOAD_ATTR             2  't_order'
               64  LOAD_ATTR             4  'append'
               67  LOAD_CONST               'tests.ordering.test_order.tearDown'
               70  CALL_FUNCTION_1       1  None
               73  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 70


class OrderingTestCase(dtest.DTestCase):

    @classmethod
    def setUpClass--- This code section failed: ---

 L.  47         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  'tests'
                6  LOAD_ATTR             2  't_order'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               3
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     30  'to 30'
               21  LOAD_ASSERT              AssertionError
               24  LOAD_CONST               'Ordering error running test suite'
               27  RAISE_VARARGS_2       2  None

 L.  48        30  LOAD_GLOBAL           1  'tests'
               33  LOAD_ATTR             2  't_order'
               36  LOAD_CONST               -1
               39  BINARY_SUBSCR    
               40  LOAD_CONST               'tests.ordering.test_order.setUp'
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_TRUE     58  'to 58'
               49  LOAD_ASSERT              AssertionError

 L.  49        52  LOAD_CONST               'Incorrect previous step'
               55  RAISE_VARARGS_2       2  None

 L.  52        58  LOAD_GLOBAL           1  'tests'
               61  LOAD_ATTR             2  't_order'
               64  LOAD_ATTR             4  'append'
               67  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.setUpClass'
               70  CALL_FUNCTION_1       1  None
               73  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 70

    @classmethod
    def tearDownClass--- This code section failed: ---

 L.  58         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  'tests'
                6  LOAD_ATTR             2  't_order'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               10
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     30  'to 30'
               21  LOAD_ASSERT              AssertionError
               24  LOAD_CONST               'Ordering error running test suite'
               27  RAISE_VARARGS_2       2  None

 L.  59        30  LOAD_GLOBAL           1  'tests'
               33  LOAD_ATTR             2  't_order'
               36  LOAD_CONST               -1
               39  BINARY_SUBSCR    
               40  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.tearDown'
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_TRUE     58  'to 58'
               49  LOAD_ASSERT              AssertionError

 L.  61        52  LOAD_CONST               'Incorrect previous step'
               55  RAISE_VARARGS_2       2  None

 L.  64        58  LOAD_GLOBAL           1  'tests'
               61  LOAD_ATTR             2  't_order'
               64  LOAD_ATTR             4  'append'
               67  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.tearDownClass'
               70  CALL_FUNCTION_1       1  None
               73  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 70

    def setUp--- This code section failed: ---

 L.  69         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  'tests'
                6  LOAD_ATTR             2  't_order'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               4
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     51  'to 51'
               21  LOAD_GLOBAL           0  'len'
               24  LOAD_GLOBAL           1  'tests'
               27  LOAD_ATTR             2  't_order'
               30  CALL_FUNCTION_1       1  None
               33  LOAD_CONST               7
               36  COMPARE_OP            2  ==
               39  POP_JUMP_IF_TRUE     51  'to 51'
               42  LOAD_ASSERT              AssertionError

 L.  70        45  LOAD_CONST               'Ordering error running test suite'
               48  RAISE_VARARGS_2       2  None

 L.  71        51  LOAD_GLOBAL           0  'len'
               54  LOAD_GLOBAL           1  'tests'
               57  LOAD_ATTR             2  't_order'
               60  CALL_FUNCTION_1       1  None
               63  LOAD_CONST               4
               66  COMPARE_OP            2  ==
               69  POP_JUMP_IF_FALSE   103  'to 103'

 L.  72        72  LOAD_GLOBAL           1  'tests'
               75  LOAD_ATTR             2  't_order'
               78  LOAD_CONST               -1
               81  BINARY_SUBSCR    
               82  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.setUpClass'
               85  COMPARE_OP            2  ==
               88  POP_JUMP_IF_TRUE    131  'to 131'
               91  LOAD_ASSERT              AssertionError

 L.  74        94  LOAD_CONST               'Incorrect previous step'
               97  RAISE_VARARGS_2       2  None
              100  JUMP_FORWARD         28  'to 131'

 L.  76       103  LOAD_GLOBAL           1  'tests'
              106  LOAD_ATTR             2  't_order'
              109  LOAD_CONST               -1
              112  BINARY_SUBSCR    
              113  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.tearDown'
              116  COMPARE_OP            2  ==
              119  POP_JUMP_IF_TRUE    131  'to 131'
              122  LOAD_ASSERT              AssertionError

 L.  78       125  LOAD_CONST               'Incorrect previous step'
              128  RAISE_VARARGS_2       2  None
            131_0  COME_FROM           100  '100'

 L.  81       131  LOAD_GLOBAL           1  'tests'
              134  LOAD_ATTR             2  't_order'
              137  LOAD_ATTR             4  'append'
              140  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.setUp'
              143  CALL_FUNCTION_1       1  None
              146  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 131_0

    def tearDown--- This code section failed: ---

 L.  86         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  'tests'
                6  LOAD_ATTR             2  't_order'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               6
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     51  'to 51'
               21  LOAD_GLOBAL           0  'len'
               24  LOAD_GLOBAL           1  'tests'
               27  LOAD_ATTR             2  't_order'
               30  CALL_FUNCTION_1       1  None
               33  LOAD_CONST               9
               36  COMPARE_OP            2  ==
               39  POP_JUMP_IF_TRUE     51  'to 51'
               42  LOAD_ASSERT              AssertionError

 L.  87        45  LOAD_CONST               'Ordering error running test suite'
               48  RAISE_VARARGS_2       2  None

 L.  88        51  LOAD_GLOBAL           0  'len'
               54  LOAD_GLOBAL           1  'tests'
               57  LOAD_ATTR             2  't_order'
               60  CALL_FUNCTION_1       1  None
               63  LOAD_CONST               6
               66  COMPARE_OP            2  ==
               69  POP_JUMP_IF_FALSE   103  'to 103'

 L.  89        72  LOAD_GLOBAL           1  'tests'
               75  LOAD_ATTR             2  't_order'
               78  LOAD_CONST               -1
               81  BINARY_SUBSCR    
               82  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.test1'
               85  COMPARE_OP            2  ==
               88  POP_JUMP_IF_TRUE    131  'to 131'
               91  LOAD_ASSERT              AssertionError

 L.  91        94  LOAD_CONST               'Incorrect previous step'
               97  RAISE_VARARGS_2       2  None
              100  JUMP_FORWARD         28  'to 131'

 L.  93       103  LOAD_GLOBAL           1  'tests'
              106  LOAD_ATTR             2  't_order'
              109  LOAD_CONST               -1
              112  BINARY_SUBSCR    
              113  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.test2'
              116  COMPARE_OP            2  ==
              119  POP_JUMP_IF_TRUE    131  'to 131'
              122  LOAD_ASSERT              AssertionError

 L.  95       125  LOAD_CONST               'Incorrect previous step'
              128  RAISE_VARARGS_2       2  None
            131_0  COME_FROM           100  '100'

 L.  98       131  LOAD_GLOBAL           1  'tests'
              134  LOAD_ATTR             2  't_order'
              137  LOAD_ATTR             4  'append'
              140  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.tearDown'
              143  CALL_FUNCTION_1       1  None
              146  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 131_0

    def test1--- This code section failed: ---

 L. 103         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  'tests'
                6  LOAD_ATTR             2  't_order'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               5
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     30  'to 30'
               21  LOAD_ASSERT              AssertionError
               24  LOAD_CONST               'Ordering error running test suite'
               27  RAISE_VARARGS_2       2  None

 L. 104        30  LOAD_GLOBAL           1  'tests'
               33  LOAD_ATTR             2  't_order'
               36  LOAD_CONST               -1
               39  BINARY_SUBSCR    
               40  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.setUp'
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_TRUE     58  'to 58'
               49  LOAD_ASSERT              AssertionError

 L. 106        52  LOAD_CONST               'Incorrect previous step'
               55  RAISE_VARARGS_2       2  None

 L. 109        58  LOAD_GLOBAL           1  'tests'
               61  LOAD_ATTR             2  't_order'
               64  LOAD_ATTR             4  'append'
               67  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.test1'
               70  CALL_FUNCTION_1       1  None
               73  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 70

    @dtest.depends(test1)
    def test2--- This code section failed: ---

 L. 115         0  LOAD_GLOBAL           0  'len'
                3  LOAD_GLOBAL           1  'tests'
                6  LOAD_ATTR             2  't_order'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               8
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     30  'to 30'
               21  LOAD_ASSERT              AssertionError
               24  LOAD_CONST               'Ordering error running test suite'
               27  RAISE_VARARGS_2       2  None

 L. 116        30  LOAD_GLOBAL           1  'tests'
               33  LOAD_ATTR             2  't_order'
               36  LOAD_CONST               -1
               39  BINARY_SUBSCR    
               40  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.setUp'
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_TRUE     58  'to 58'
               49  LOAD_ASSERT              AssertionError

 L. 118        52  LOAD_CONST               'Incorrect previous step'
               55  RAISE_VARARGS_2       2  None

 L. 121        58  LOAD_GLOBAL           1  'tests'
               61  LOAD_ATTR             2  't_order'
               64  LOAD_ATTR             4  'append'
               67  LOAD_CONST               'tests.ordering.test_order.OrderingTestCase.test2'
               70  CALL_FUNCTION_1       1  None
               73  POP_TOP          

Parse error at or near `CALL_FUNCTION_1' instruction at offset 70