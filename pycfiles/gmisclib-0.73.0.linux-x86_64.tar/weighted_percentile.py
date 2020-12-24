# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/weighted_percentile.py
# Compiled at: 2011-05-11 14:58:46
"""This computes order statistics on data with weights.
"""
import numpy
from gmisclib import Num

def wp--- This code section failed: ---

 L.  26         0  LOAD_GLOBAL           0  'Num'
                3  LOAD_ATTR             1  'alltrue'
                6  LOAD_GLOBAL           0  'Num'
                9  LOAD_ATTR             2  'greater_equal'
               12  LOAD_FAST             2  'percentiles'
               15  LOAD_CONST               0.0
               18  CALL_FUNCTION_2       2  None
               21  CALL_FUNCTION_1       1  None
               24  POP_JUMP_IF_TRUE     36  'to 36'
               27  LOAD_ASSERT              AssertionError
               30  LOAD_CONST               'Percentiles less than zero'
               33  RAISE_VARARGS_2       2  None

 L.  27        36  LOAD_GLOBAL           0  'Num'
               39  LOAD_ATTR             1  'alltrue'
               42  LOAD_GLOBAL           0  'Num'
               45  LOAD_ATTR             4  'less_equal'
               48  LOAD_FAST             2  'percentiles'
               51  LOAD_CONST               1.0
               54  CALL_FUNCTION_2       2  None
               57  CALL_FUNCTION_1       1  None
               60  POP_JUMP_IF_TRUE     72  'to 72'
               63  LOAD_ASSERT              AssertionError
               66  LOAD_CONST               'Percentiles greater than one'
               69  RAISE_VARARGS_2       2  None

 L.  28        72  LOAD_GLOBAL           0  'Num'
               75  LOAD_ATTR             5  'asarray'
               78  LOAD_FAST             0  'data'
               81  CALL_FUNCTION_1       1  None
               84  STORE_FAST            0  'data'

 L.  29        87  LOAD_GLOBAL           6  'len'
               90  LOAD_FAST             0  'data'
               93  LOAD_ATTR             7  'shape'
               96  CALL_FUNCTION_1       1  None
               99  LOAD_CONST               1
              102  COMPARE_OP            2  ==
              105  POP_JUMP_IF_TRUE    114  'to 114'
              108  LOAD_ASSERT              AssertionError
              111  RAISE_VARARGS_1       1  None

 L.  30       114  LOAD_FAST             1  'wt'
              117  LOAD_CONST               None
              120  COMPARE_OP            8  is
              123  POP_JUMP_IF_FALSE   153  'to 153'

 L.  31       126  LOAD_GLOBAL           0  'Num'
              129  LOAD_ATTR             9  'ones'
              132  LOAD_FAST             0  'data'
              135  LOAD_ATTR             7  'shape'
              138  LOAD_GLOBAL           0  'Num'
              141  LOAD_ATTR            10  'Float'
              144  CALL_FUNCTION_2       2  None
              147  STORE_FAST            1  'wt'
              150  JUMP_FORWARD         81  'to 234'

 L.  33       153  LOAD_GLOBAL           0  'Num'
              156  LOAD_ATTR             5  'asarray'
              159  LOAD_FAST             1  'wt'
              162  LOAD_GLOBAL           0  'Num'
              165  LOAD_ATTR            10  'Float'
              168  CALL_FUNCTION_2       2  None
              171  STORE_FAST            1  'wt'

 L.  34       174  LOAD_FAST             1  'wt'
              177  LOAD_ATTR             7  'shape'
              180  LOAD_FAST             0  'data'
              183  LOAD_ATTR             7  'shape'
              186  COMPARE_OP            2  ==
              189  POP_JUMP_IF_TRUE    198  'to 198'
              192  LOAD_ASSERT              AssertionError
              195  RAISE_VARARGS_1       1  None

 L.  35       198  LOAD_GLOBAL           0  'Num'
              201  LOAD_ATTR             1  'alltrue'
              204  LOAD_GLOBAL           0  'Num'
              207  LOAD_ATTR             2  'greater_equal'
              210  LOAD_FAST             1  'wt'
              213  LOAD_CONST               0.0
              216  CALL_FUNCTION_2       2  None
              219  CALL_FUNCTION_1       1  None
              222  POP_JUMP_IF_TRUE    234  'to 234'
              225  LOAD_ASSERT              AssertionError
              228  LOAD_CONST               'Not all weights are non-negative.'
              231  RAISE_VARARGS_2       2  None
            234_0  COME_FROM           150  '150'

 L.  36       234  LOAD_GLOBAL           6  'len'
              237  LOAD_FAST             1  'wt'
              240  LOAD_ATTR             7  'shape'
              243  CALL_FUNCTION_1       1  None
              246  LOAD_CONST               1
              249  COMPARE_OP            2  ==
              252  POP_JUMP_IF_TRUE    261  'to 261'
              255  LOAD_ASSERT              AssertionError
              258  RAISE_VARARGS_1       1  None

 L.  37       261  LOAD_FAST             0  'data'
              264  LOAD_ATTR             7  'shape'
              267  LOAD_CONST               0
              270  BINARY_SUBSCR    
              271  STORE_FAST            3  'n'

 L.  38       274  LOAD_FAST             3  'n'
              277  LOAD_CONST               0
              280  COMPARE_OP            4  >
              283  POP_JUMP_IF_TRUE    292  'to 292'
              286  LOAD_ASSERT              AssertionError
              289  RAISE_VARARGS_1       1  None

 L.  39       292  LOAD_GLOBAL           0  'Num'
              295  LOAD_ATTR            11  'argsort'
              298  LOAD_FAST             0  'data'
              301  CALL_FUNCTION_1       1  None
              304  STORE_FAST            4  'i'

 L.  40       307  LOAD_GLOBAL           0  'Num'
              310  LOAD_ATTR            12  'take'
              313  LOAD_FAST             0  'data'
              316  LOAD_FAST             4  'i'
              319  LOAD_CONST               'axis'
              322  LOAD_CONST               0
              325  CALL_FUNCTION_258   258  None
              328  STORE_FAST            5  'sd'

 L.  41       331  LOAD_GLOBAL           0  'Num'
              334  LOAD_ATTR            12  'take'
              337  LOAD_FAST             1  'wt'
              340  LOAD_FAST             4  'i'
              343  LOAD_CONST               'axis'
              346  LOAD_CONST               0
              349  CALL_FUNCTION_258   258  None
              352  STORE_FAST            6  'sw'

 L.  42       355  LOAD_GLOBAL           0  'Num'
              358  LOAD_ATTR            13  'add'
              361  LOAD_ATTR            14  'accumulate'
              364  LOAD_FAST             6  'sw'
              367  CALL_FUNCTION_1       1  None
              370  STORE_FAST            7  'aw'

 L.  43       373  LOAD_FAST             7  'aw'
              376  LOAD_CONST               -1
              379  BINARY_SUBSCR    
              380  LOAD_CONST               0
              383  COMPARE_OP            4  >
              386  POP_JUMP_IF_TRUE    401  'to 401'

 L.  44       389  LOAD_GLOBAL          15  'ValueError'
              392  LOAD_CONST               'Nonpositive weight sum'
              395  RAISE_VARARGS_2       2  None
              398  JUMP_FORWARD          0  'to 401'
            401_0  COME_FROM           398  '398'

 L.  45       401  LOAD_FAST             7  'aw'
              404  LOAD_CONST               0.5
              407  LOAD_FAST             6  'sw'
              410  BINARY_MULTIPLY  
              411  BINARY_SUBTRACT  
              412  LOAD_FAST             7  'aw'
              415  LOAD_CONST               -1
              418  BINARY_SUBSCR    
              419  BINARY_DIVIDE    
              420  STORE_FAST            8  'w'

 L.  46       423  LOAD_GLOBAL           0  'Num'
              426  LOAD_ATTR            16  'searchsorted'
              429  LOAD_FAST             8  'w'
              432  LOAD_FAST             2  'percentiles'
              435  CALL_FUNCTION_2       2  None
              438  STORE_FAST            9  'spots'

 L.  47       441  BUILD_LIST_0          0 
              444  STORE_FAST           10  'o'

 L.  48       447  SETUP_LOOP          292  'to 742'
              450  LOAD_GLOBAL          17  'zip'
              453  LOAD_FAST             9  'spots'
              456  LOAD_FAST             2  'percentiles'
              459  CALL_FUNCTION_2       2  None
              462  GET_ITER         
              463  FOR_ITER            275  'to 741'
              466  UNPACK_SEQUENCE_2     2 
              469  STORE_FAST           11  's'
              472  STORE_FAST           12  'p'

 L.  49       475  LOAD_FAST            11  's'
              478  LOAD_CONST               0
              481  COMPARE_OP            2  ==
              484  POP_JUMP_IF_FALSE   507  'to 507'

 L.  50       487  LOAD_FAST            10  'o'
              490  LOAD_ATTR            18  'append'
              493  LOAD_FAST             5  'sd'
              496  LOAD_CONST               0
              499  BINARY_SUBSCR    
              500  CALL_FUNCTION_1       1  None
              503  POP_TOP          
              504  JUMP_BACK           463  'to 463'

 L.  51       507  LOAD_FAST            11  's'
              510  LOAD_FAST             3  'n'
              513  COMPARE_OP            2  ==
              516  POP_JUMP_IF_FALSE   543  'to 543'

 L.  52       519  LOAD_FAST            10  'o'
              522  LOAD_ATTR            18  'append'
              525  LOAD_FAST             5  'sd'
              528  LOAD_FAST             3  'n'
              531  LOAD_CONST               1
              534  BINARY_SUBTRACT  
              535  BINARY_SUBSCR    
              536  CALL_FUNCTION_1       1  None
              539  POP_TOP          
              540  JUMP_BACK           463  'to 463'

 L.  54       543  LOAD_FAST             8  'w'
              546  LOAD_FAST            11  's'
              549  BINARY_SUBSCR    
              550  LOAD_FAST            12  'p'
              553  BINARY_SUBTRACT  
              554  LOAD_FAST             8  'w'
              557  LOAD_FAST            11  's'
              560  BINARY_SUBSCR    
              561  LOAD_FAST             8  'w'
              564  LOAD_FAST            11  's'
              567  LOAD_CONST               1
              570  BINARY_SUBTRACT  
              571  BINARY_SUBSCR    
              572  BINARY_SUBTRACT  
              573  BINARY_DIVIDE    
              574  STORE_FAST           13  'f1'

 L.  55       577  LOAD_FAST            12  'p'
              580  LOAD_FAST             8  'w'
              583  LOAD_FAST            11  's'
              586  LOAD_CONST               1
              589  BINARY_SUBTRACT  
              590  BINARY_SUBSCR    
              591  BINARY_SUBTRACT  
              592  LOAD_FAST             8  'w'
              595  LOAD_FAST            11  's'
              598  BINARY_SUBSCR    
              599  LOAD_FAST             8  'w'
              602  LOAD_FAST            11  's'
              605  LOAD_CONST               1
              608  BINARY_SUBTRACT  
              609  BINARY_SUBSCR    
              610  BINARY_SUBTRACT  
              611  BINARY_DIVIDE    
              612  STORE_FAST           14  'f2'

 L.  56       615  LOAD_FAST            13  'f1'
              618  LOAD_CONST               0
              621  COMPARE_OP            5  >=
              624  POP_JUMP_IF_FALSE   663  'to 663'
              627  LOAD_FAST            14  'f2'
              630  LOAD_CONST               0
              633  COMPARE_OP            5  >=
              636  POP_JUMP_IF_FALSE   663  'to 663'
              639  LOAD_FAST            13  'f1'
              642  LOAD_CONST               1
              645  COMPARE_OP            1  <=
              648  POP_JUMP_IF_FALSE   663  'to 663'
              651  LOAD_FAST            14  'f2'
              654  LOAD_CONST               1
              657  COMPARE_OP            1  <=
            660_0  COME_FROM           648  '648'
            660_1  COME_FROM           636  '636'
            660_2  COME_FROM           624  '624'
              660  POP_JUMP_IF_TRUE    669  'to 669'
              663  LOAD_ASSERT              AssertionError
              666  RAISE_VARARGS_1       1  None

 L.  57       669  LOAD_GLOBAL          19  'abs'
              672  LOAD_FAST            13  'f1'
              675  LOAD_FAST            14  'f2'
              678  BINARY_ADD       
              679  LOAD_CONST               1.0
              682  BINARY_SUBTRACT  
              683  CALL_FUNCTION_1       1  None
              686  LOAD_CONST               1e-06
              689  COMPARE_OP            0  <
              692  POP_JUMP_IF_TRUE    701  'to 701'
              695  LOAD_ASSERT              AssertionError
              698  RAISE_VARARGS_1       1  None

 L.  58       701  LOAD_FAST            10  'o'
              704  LOAD_ATTR            18  'append'
              707  LOAD_FAST             5  'sd'
              710  LOAD_FAST            11  's'
              713  LOAD_CONST               1
              716  BINARY_SUBTRACT  
              717  BINARY_SUBSCR    
              718  LOAD_FAST            13  'f1'
              721  BINARY_MULTIPLY  
              722  LOAD_FAST             5  'sd'
              725  LOAD_FAST            11  's'
              728  BINARY_SUBSCR    
              729  LOAD_FAST            14  'f2'
              732  BINARY_MULTIPLY  
              733  BINARY_ADD       
              734  CALL_FUNCTION_1       1  None
              737  POP_TOP          
              738  JUMP_BACK           463  'to 463'
              741  POP_BLOCK        
            742_0  COME_FROM           447  '447'

 L.  59       742  LOAD_FAST            10  'o'
              745  RETURN_VALUE     

Parse error at or near `COME_FROM' instruction at offset 234_0


def wtd_median(data, wt):
    """The weighted median is the point where half the weight is above
        and half the weight is below.   If the weights are equal, this is the
        same as the median.   Elements of the C{data} and C{wt} arrays correspond to
        each other and must have equal length (unless C{wt} is C{None}).

        @param data: The data.
        @type data: A L{numpy.ndarray} array or a C{list} of numbers.
        @param wt: How important is a given piece of data.
        @type wt: C{None} or a L{numpy.ndarray} array or a C{list} of numbers.
                All the weights must be non-negative and the sum must be
                greater than zero.
        @rtype: C{float}
        @return: the weighted median of the data.
        """
    spots = wp(data, wt, [0.5])
    assert len(spots) == 1
    return spots[0]


def wtd_median_across(list_of_vectors, wt):
    """Takes a weighted component-by-component median of a sequence of vectors.
        @param list_of_vectors: the data to be combined
        @type list_of_vectors: any sequence of lists or numpy.ndarray.
                All the inside lists must be of the same length.
        @type wt: a vector of weights (one weight for each input vector) or None.
        @param wt: sequence of numbers or None
        @return: the median vector.
        @rtype: C{numpy.ndarray}
        """
    lov = list(list_of_vectors)
    n = len(lov[0])
    for v in lov:
        if len(v) != n:
            for i, vv in enumerate(lov):
                if len(vv) != n:
                    raise ValueError, "Vector lengths don't match: %d[0] and %d[%d]" % (n, len(vv), i)

    m = len(lov)
    tmp = numpy.zeros((m,))
    rv = numpy.zeros((n,))
    for i in range(n):
        for j, v in enumerate(lov):
            tmp[j] = v[i]

        rv[i] = wtd_median(tmp, wt)

    return rv


def test():
    assert Num.allclose(wp([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], None, [
     0.0, 1.0, 0.5, 0.51, 0.49, 0.01, 0.99]), [
     1.0, 10.0, 5.5, 5.6, 5.4, 1.0, 10.0], 0.0001)
    assert Num.allclose(wp([0, 1, 2, 3, 4], [0.1, 1.9, 1.9, 0.1, 1], [
     0.0, 1.0, 0.01, 0.02, 0.99]), [
     0.0, 4.0, 0.0, 0.05, 4.0], 0.0001)
    return


def test_median():
    d = [
     1, 1, 1, 1, 2, 2, 2, 2]
    w = [1, 1, 1, 1, 2, 1, 1, 1]
    assert 1.0 <= wtd_median(d, w) <= 2.0
    d = [1.0, 1, 1, 1, 2, 2, 2, 2]
    w = [1, 1.1, 2, 1, 2, 1, 1, 1]
    assert 1.0 <= wtd_median(d, w) <= 2.0
    d = [1, 1, 1, 1, 2, 3, 3, 3, 3.0]
    w = [1, 1, 1, 1, 1.0, 1, 1, 1, 1]
    assert abs(wtd_median(d, w) - 2.0) < 0.001
    d = [1, 1, 1, 1, 2, 3, 3, 3, 3.0]
    w = [1, 1, 1.1, 1, 1.0, 1, 1, 1, 1]
    assert 1.0 <= wtd_median(d, w) <= 2.0
    d = [1, 1, 1, 1, 2, 3, 3, 3, 3.0]
    w = [1.3, 1.3, 1.3, 1.3, 1.0, 1, 1, 1, 1]
    assert 1.0 <= wtd_median(d, w) <= 2.0
    d = [1, 1, 1, 1, 2, 3, 4, 4.0]
    w = [1.0, 1.0, 1.0, 1.0, 0.0, 1, 2, 2]
    assert abs(wtd_median(d, w) - 3.0) < 0.001


if __name__ == '__main__':
    test_median()
    test()