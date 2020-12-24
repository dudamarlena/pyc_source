# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/nmf.py
# Compiled at: 2008-02-21 12:25:35
"""V=WH, where W and H are non-negative.

From D. D. Lee and H. S. Seung, 'Learning the parts of objects by
nonnegative matrix factorization.'
"""
import Num, math, die
EPS = 1e-06
CC = 2
IEPS = 0.03

def _norm(x):
    try:
        tmp = math.sqrt(Num.sum(x ** 2, axis=None))
    except OverflowError as x:
        print 'x=', x
        raise

    return tmp


def _converged(wh, whold, v, fudge):
    F = math.sqrt(wh.shape[0] * wh.shape[1])
    d1 = _norm(wh - whold) / _norm(v)
    d2 = _norm(v - wh) / _norm(v)
    die.dbg('Converged= %f %f' % (d1, d2))
    return min(d1 * F, d2) < EPS * fudge


def _updateH(w, h, wh, v):
    eps = EPS * Num.sum(wh, axis=None) / (v.shape[0] * v.shape[1])
    f = Num.matrixmultiply(Num.transpose(w), v / (wh + eps))
    return h * f


def _updateW(w, h, wh, v):
    eps = EPS * Num.sum(wh, axis=None) / (v.shape[0] * v.shape[1])
    print 'eps=', eps
    f = Num.matrixmultiply(v / (wh + eps), Num.transpose(h))
    print 'f=', f
    print 'W:v/wh=', v / (wh + eps)
    print 'W:f=', f
    new_w = w * f
    print 'new_w=', new_w
    first_index_sum = Num.sum(new_w, axis=0)
    print 'fis=', first_index_sum
    print 'new_w=', new_w
    o = new_w / first_index_sum[Num.NewAxis, :]
    print 'o=', o
    return o


def _initialize(v, rank):
    n, m = v.shape
    w = Num.RA.standard_normal((n, rank)) ** 2 + IEPS
    c = Num.sum(v ** 2, axis=0) / (v.shape[0] * v.shape[1])
    h = c * (Num.RA.standard_normal((rank, m)) ** 2 + IEPS)
    return (w, h)


def nmf--- This code section failed: ---

 L.  70         0  LOAD_FAST             1  'rank'
                3  LOAD_CONST               0
                6  COMPARE_OP            4  >
                9  POP_JUMP_IF_TRUE     21  'to 21'
               12  LOAD_ASSERT              AssertionError
               15  LOAD_CONST               'Zero rank approximations are usually pretty awful.'
               18  RAISE_VARARGS_2       2  None

 L.  71        21  LOAD_GLOBAL           1  'Num'
               24  LOAD_ATTR             2  'asarray'
               27  LOAD_FAST             0  'v'
               30  LOAD_GLOBAL           1  'Num'
               33  LOAD_ATTR             3  'Float'
               36  CALL_FUNCTION_2       2  None
               39  STORE_FAST            0  'v'

 L.  72        42  LOAD_GLOBAL           1  'Num'
               45  LOAD_ATTR             4  'alltrue'
               48  LOAD_GLOBAL           1  'Num'
               51  LOAD_ATTR             5  'greater_equal'
               54  LOAD_GLOBAL           1  'Num'
               57  LOAD_ATTR             6  'ravel'
               60  LOAD_FAST             0  'v'
               63  CALL_FUNCTION_1       1  None
               66  LOAD_CONST               0.0
               69  CALL_FUNCTION_2       2  None
               72  CALL_FUNCTION_1       1  None
               75  POP_JUMP_IF_TRUE     87  'to 87'
               78  LOAD_ASSERT              AssertionError
               81  LOAD_CONST               'Negative element!'
               84  RAISE_VARARGS_2       2  None

 L.  73        87  LOAD_GLOBAL           7  '_initialize'
               90  LOAD_FAST             0  'v'
               93  LOAD_FAST             1  'rank'
               96  CALL_FUNCTION_2       2  None
               99  UNPACK_SEQUENCE_2     2 
              102  STORE_FAST            2  'w'
              105  STORE_FAST            3  'h'

 L.  74       108  LOAD_CONST               0
              111  STORE_FAST            4  'cc'

 L.  75       114  LOAD_CONST               0
              117  STORE_FAST            5  'ic'

 L.  76       120  LOAD_GLOBAL           1  'Num'
              123  LOAD_ATTR             8  'zeros'
              126  LOAD_FAST             0  'v'
              129  LOAD_ATTR             9  'shape'
              132  LOAD_GLOBAL           1  'Num'
              135  LOAD_ATTR             3  'Float'
              138  CALL_FUNCTION_2       2  None
              141  STORE_FAST            6  'wh'

 L.  77       144  SETUP_LOOP          166  'to 313'

 L.  79       147  LOAD_FAST             6  'wh'
              150  STORE_FAST            7  'whold'

 L.  80       153  LOAD_GLOBAL           1  'Num'
              156  LOAD_ATTR            10  'matrixmultiply'
              159  LOAD_FAST             2  'w'
              162  LOAD_FAST             3  'h'
              165  CALL_FUNCTION_2       2  None
              168  STORE_FAST            6  'wh'

 L.  81       171  LOAD_GLOBAL          11  '_converged'
              174  LOAD_FAST             6  'wh'
              177  LOAD_FAST             7  'whold'
              180  LOAD_FAST             0  'v'
              183  LOAD_GLOBAL          12  'math'
              186  LOAD_ATTR            13  'sqrt'
              189  LOAD_FAST             5  'ic'
              192  LOAD_GLOBAL          14  'float'
              195  LOAD_FAST             1  'rank'
              198  CALL_FUNCTION_1       1  None
              201  BINARY_DIVIDE    
              202  CALL_FUNCTION_1       1  None
              205  CALL_FUNCTION_4       4  None
              208  POP_JUMP_IF_FALSE   224  'to 224'

 L.  82       211  LOAD_FAST             4  'cc'
              214  LOAD_CONST               1
              217  INPLACE_ADD      
              218  STORE_FAST            4  'cc'
              221  JUMP_FORWARD          6  'to 230'

 L.  84       224  LOAD_CONST               0
              227  STORE_FAST            4  'cc'
            230_0  COME_FROM           221  '221'

 L.  86       230  LOAD_FAST             4  'cc'
              233  LOAD_GLOBAL          15  'CC'
              236  COMPARE_OP            4  >
              239  POP_JUMP_IF_FALSE   246  'to 246'

 L.  87       242  BREAK_LOOP       
              243  JUMP_FORWARD          0  'to 246'
            246_0  COME_FROM           243  '243'

 L.  88       246  LOAD_GLOBAL          16  '_updateW'
              249  LOAD_FAST             2  'w'
              252  LOAD_FAST             3  'h'
              255  LOAD_FAST             6  'wh'
              258  LOAD_FAST             0  'v'
              261  CALL_FUNCTION_4       4  None
              264  STORE_FAST            8  'wnew'

 L.  89       267  LOAD_GLOBAL          17  '_updateH'
              270  LOAD_FAST             2  'w'
              273  LOAD_FAST             3  'h'
              276  LOAD_FAST             6  'wh'
              279  LOAD_FAST             0  'v'
              282  CALL_FUNCTION_4       4  None
              285  STORE_FAST            9  'hnew'

 L.  90       288  LOAD_FAST             8  'wnew'
              291  STORE_FAST            2  'w'

 L.  91       294  LOAD_FAST             9  'hnew'
              297  STORE_FAST            3  'h'

 L.  92       300  LOAD_FAST             5  'ic'
              303  LOAD_CONST               1
              306  INPLACE_ADD      
              307  STORE_FAST            5  'ic'
              310  JUMP_BACK           147  'to 147'
            313_0  COME_FROM           144  '144'

 L.  94       313  LOAD_FAST             2  'w'
              316  LOAD_FAST             3  'h'
              319  LOAD_GLOBAL          18  '_norm'
              322  LOAD_FAST             0  'v'
              325  LOAD_GLOBAL           1  'Num'
              328  LOAD_ATTR            10  'matrixmultiply'
              331  LOAD_FAST             2  'w'
              334  LOAD_FAST             3  'h'
              337  CALL_FUNCTION_2       2  None
              340  BINARY_SUBTRACT  
              341  CALL_FUNCTION_1       1  None
              344  BUILD_TUPLE_3         3 
              347  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 347


def _test1():
    a = [
     [
      1, 0], [1, 0], [0, 0]]
    w, h, err = nmf(a, 1)
    wh = Num.matrixmultiply(w, h)
    assert _norm(wh - a) < 30 * EPS
    assert err < 0.001


def _test2():
    a = [
     [
      1, 0], [0, 1], [0, 0]]
    w, h, err = nmf(a, 2)
    wh = Num.matrixmultiply(w, h)
    assert _norm(wh - a) < 30 * EPS
    assert err < 0.001


def _test3(rank):
    a = [
     [
      1.0, 0.0, 0.5], [0.0, 1.0, 0.5], [1.0, 1.0, 1.0]]
    w, h, err = nmf(a, rank)
    wh = Num.matrixmultiply(w, h)
    assert _norm(wh - a) < 30 * math.sqrt(EPS)
    assert err < 0.001


if __name__ == '__main__':
    print 'TEST1'
    _test1()
    print
    print 'TEST2'
    _test2()
    print
    print 'TEST3(1)'
    try:
        _test3(1)
    except AssertionError:
        pass
    else:
        raise AssertionError, 'Test3(1) should fail!'

    print
    print 'TEST3(2)'
    _test3(2)
    print
    print 'TEST3(3)'
    _test3(3)
    print
    print 'TEST3(4)'
    _test3(4)
    print 'TEST3(5)'
    _test3(5)
    print
    print 'LAST'
    a = [
     [
      1, 0], [0, 1]]
    w, h, err = nmf(a, 4)
    print 'w=', w
    print 'h=', h
    print 'wh=', Num.matrixmultiply(w, h)
    print 'a=', a