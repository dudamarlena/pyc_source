# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/gpkmisc.py
# Compiled at: 2011-04-20 04:20:14
from __future__ import with_statement
import os, sys, math, time, stat, errno, die
try:
    from Numeric_gpk import N_maximum, N_minimum, N_median, N_mean_ad, variance, stdev, set_diag, make_diag, limit, vec_variance, qform, KolmogorovSmirnov, interp, interpN
except ImportError as _x:
    if str(_x).startswith('cannot import name'):
        raise

def median(x):
    """
        @except ValueError: if the input list is zero length.
        """
    xx = sorted(x)
    n = len(xx)
    if not n > 0:
        raise ValueError, 'No data to median.'
    return 0.5 * (xx[(n // 2)] + xx[((n - 1) // 2)])


def median_across(xl):
    """
        @note: There is a version of this in Numeric_gpk that is more efficient when the input
                is a list of numpy.ndarray vectors.
        @except ValueError: If the input vectors are different lengths.
        @except ValueError: see L{median}.
        """
    rv = []
    tl = None
    for i, tup in enumerate(zip(*xl)):
        if tl is None:
            tl = len(tup)
        elif tl != len(tup):
            raise ValueError, 'Vector %d has a different length(%d) from the rest(%d)' % (i, len(tup), tl)
        rv.append(median(tup))

    return rv


def avg(x):
    s = 0.0
    n = 0
    for t in x:
        s += t
        n += 1

    return s / float(n)


def median_ad(x):
    """Median absolute deviation"""
    medn = median(x)
    return median([ abs(t - medn) for t in x ])


mad = median_ad

def mean_ad(x):
    medn = median(x)
    sum = 0.0
    for t in x:
        sum += abs(t - medn)

    return (
     medn, sum / float(len(x)))


def geo_mean(*d):
    """
        @except ValueError: if any argument is negative.
        @return: Geometric mean of its arguments.
        @rtype: float
        """
    s = 0.0
    for t in d:
        if t == 0.0:
            return 0.0
        if t > 0.0:
            s += math.log(t)
        else:
            raise ValueError, 'Negative/NaN argument to geo_mean: %s' % str(t)

    return math.exp(s / len(d))


def entropy--- This code section failed: ---

 L.  96         0  LOAD_CONST               0.0
                3  STORE_FAST            1  'e'

 L.  97         6  LOAD_CONST               0.0
                9  STORE_FAST            2  'ps'

 L.  98        12  SETUP_LOOP           80  'to 95'
               15  LOAD_FAST             0  'x'
               18  GET_ITER         
               19  FOR_ITER             72  'to 94'
               22  STORE_FAST            3  'p'

 L.  99        25  LOAD_FAST             3  'p'
               28  LOAD_CONST               1.0
               31  COMPARE_OP            1  <=
               34  POP_JUMP_IF_TRUE     43  'to 43'
               37  LOAD_ASSERT              AssertionError
               40  RAISE_VARARGS_1       1  None

 L. 100        43  LOAD_FAST             3  'p'
               46  LOAD_CONST               0.0
               49  COMPARE_OP            4  >
               52  POP_JUMP_IF_FALSE    81  'to 81'

 L. 101        55  LOAD_FAST             1  'e'
               58  LOAD_FAST             3  'p'
               61  LOAD_GLOBAL           1  'math'
               64  LOAD_ATTR             2  'log'
               67  LOAD_FAST             3  'p'
               70  CALL_FUNCTION_1       1  None
               73  BINARY_MULTIPLY  
               74  INPLACE_SUBTRACT 
               75  STORE_FAST            1  'e'
               78  JUMP_FORWARD          0  'to 81'
             81_0  COME_FROM            78  '78'

 L. 102        81  LOAD_FAST             2  'ps'
               84  LOAD_FAST             3  'p'
               87  INPLACE_ADD      
               88  STORE_FAST            2  'ps'
               91  JUMP_BACK            19  'to 19'
               94  POP_BLOCK        
             95_0  COME_FROM            12  '12'

 L. 103        95  LOAD_CONST               0.999
               98  LOAD_FAST             2  'ps'
              101  DUP_TOP          
              102  ROT_THREE        
              103  COMPARE_OP            0  <
              106  JUMP_IF_FALSE_OR_POP   118  'to 118'
              109  LOAD_CONST               1.001
              112  COMPARE_OP            0  <
              115  JUMP_FORWARD          2  'to 120'
            118_0  COME_FROM           106  '106'
              118  ROT_TWO          
              119  POP_TOP          
            120_0  COME_FROM           115  '115'
              120  POP_JUMP_IF_TRUE    132  'to 132'
              123  LOAD_ASSERT              AssertionError
              126  LOAD_CONST               'Probabilities must sum to one.'
              129  RAISE_VARARGS_2       2  None

 L. 104       132  LOAD_FAST             1  'e'
              135  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 135


def resample(d):
    """Bootstrap resampling.  Call this many times: each one
        returns a random resampling.
        """
    import random
    o = []
    for i in range(len(d)):
        o.append(random.choice(d))

    return o


def jackknife(d):
    """Jackknife resampling.  Call this once.
        It returns a list of deleted lists."""
    for drop in range(len(d)):
        yield [ di for i, di in enumerate(d) if i != drop ]


def Student_t_dens(x, n):
    """From p.337 Statistical Theory by Bernard Lindgren."""
    from transcendental import gamma
    p = gamma((n + 1) / 2.0) * (1 + x * x / n) ** (-(n + 1) / 2.0) / (math.sqrt(n * math.pi) * gamma(n / 2.0))
    return p


def log_Student_t_dens(x, n):
    """From p.337 Statistical Theory by Bernard Lindgren."""
    assert n > 0
    from gmisclib import stats
    lp = math.log(1 + x * x / n) * (-(n + 1) / 2.0)
    lp += stats.gammaln((n + 1) / 2.0) - stats.gammaln(n / 2.0)
    lp -= 0.5 * math.log(n * math.pi)
    return lp


_fcache = {}

def log_factorial(n):
    assert n >= 0
    try:
        lf = _fcache[n]
    except KeyError:
        lf = 0.0
        for i in range(2, n):
            lf += math.log(i)

        _fcache[n] = lf

    return lf


def log_Combinations(n, m):
    assert n >= m
    assert m >= 0
    return log_factorial(n) - log_factorial(m) - log_factorial(n - m)


def ComplexMedian--- This code section failed: ---

 L. 179         0  LOAD_CONST               -1
                3  LOAD_CONST               None
                6  IMPORT_NAME           0  'convex_hull2d'
                9  STORE_FAST            1  'convex_hull2d'

 L. 180        12  LOAD_CONST               -1
               15  LOAD_CONST               None
               18  IMPORT_NAME           1  'cmath'
               21  STORE_FAST            2  'cmath'

 L. 181        24  LOAD_CONST               -1
               27  LOAD_CONST               None
               30  IMPORT_NAME           2  'dictops'
               33  STORE_FAST            3  'dictops'

 L. 182        36  LOAD_CONST               1e+30
               39  STORE_FAST            4  'HUGE'

 L. 183        42  LOAD_CONST               1e-07
               45  STORE_FAST            5  'EPS'

 L. 184        48  LOAD_FAST             3  'dictops'
               51  LOAD_ATTR             3  'dict_of_accums'
               54  CALL_FUNCTION_0       0  None
               57  STORE_FAST            6  'Q'

 L. 185        60  SETUP_LOOP           30  'to 93'
               63  LOAD_FAST             0  'P'
               66  GET_ITER         
               67  FOR_ITER             22  'to 92'
               70  STORE_FAST            7  'p'

 L. 186        73  LOAD_FAST             6  'Q'
               76  LOAD_ATTR             4  'add'
               79  LOAD_FAST             7  'p'
               82  LOAD_CONST               1.0
               85  CALL_FUNCTION_2       2  None
               88  POP_TOP          
               89  JUMP_BACK            67  'to 67'
               92  POP_BLOCK        
             93_0  COME_FROM            60  '60'

 L. 188        93  SETUP_LOOP          676  'to 772'
               96  LOAD_GLOBAL           5  'len'
               99  LOAD_FAST             6  'Q'
              102  CALL_FUNCTION_1       1  None
              105  LOAD_CONST               3
              108  COMPARE_OP            4  >
              111  POP_JUMP_IF_FALSE   771  'to 771'

 L. 190       114  LOAD_FAST             1  'convex_hull2d'
              117  LOAD_ATTR             6  'convexHull'
              120  LOAD_FAST             6  'Q'
              123  LOAD_ATTR             7  'keys'
              126  CALL_FUNCTION_0       0  None
              129  CALL_FUNCTION_1       1  None
              132  STORE_FAST            8  'edge'

 L. 192       135  LOAD_FAST             8  'edge'
              138  LOAD_CONST               -1
              141  BINARY_SUBSCR    
              142  BUILD_TUPLE_1         1 
              145  LOAD_FAST             8  'edge'
              148  BINARY_ADD       
              149  LOAD_FAST             8  'edge'
              152  LOAD_CONST               0
              155  BINARY_SUBSCR    
              156  BUILD_TUPLE_1         1 
              159  BINARY_ADD       
              160  STORE_FAST            9  'ee'

 L. 193       163  BUILD_MAP_0           0  None
              166  STORE_FAST           10  'wt'

 L. 194       169  SETUP_LOOP          342  'to 514'
              172  LOAD_GLOBAL           8  'range'
              175  LOAD_CONST               1
              178  LOAD_GLOBAL           5  'len'
              181  LOAD_FAST             8  'edge'
              184  CALL_FUNCTION_1       1  None
              187  LOAD_CONST               1
              190  BINARY_ADD       
              191  CALL_FUNCTION_2       2  None
              194  GET_ITER         
              195  FOR_ITER            315  'to 513'
              198  STORE_FAST           11  'i'

 L. 195       201  LOAD_FAST             9  'ee'
              204  LOAD_FAST            11  'i'
              207  BINARY_SUBSCR    
              208  LOAD_FAST             9  'ee'
              211  LOAD_FAST            11  'i'
              214  LOAD_CONST               1
              217  BINARY_SUBTRACT  
              218  BINARY_SUBSCR    
              219  BINARY_SUBTRACT  
              220  STORE_FAST           12  'em'

 L. 196       223  LOAD_FAST             9  'ee'
              226  LOAD_FAST            11  'i'
              229  LOAD_CONST               1
              232  BINARY_ADD       
              233  BINARY_SUBSCR    
              234  LOAD_FAST             9  'ee'
              237  LOAD_FAST            11  'i'
              240  BINARY_SUBSCR    
              241  BINARY_SUBTRACT  
              242  STORE_FAST           13  'ep'

 L. 198       245  LOAD_GLOBAL           9  'min'
              248  LOAD_GLOBAL          10  'abs'
              251  LOAD_FAST            13  'ep'
              254  CALL_FUNCTION_1       1  None
              257  LOAD_GLOBAL          10  'abs'
              260  LOAD_FAST            12  'em'
              263  CALL_FUNCTION_1       1  None
              266  CALL_FUNCTION_2       2  None
              269  LOAD_FAST             5  'EPS'
              272  LOAD_GLOBAL          11  'max'
              275  LOAD_GLOBAL          10  'abs'
              278  LOAD_FAST            12  'em'
              281  CALL_FUNCTION_1       1  None
              284  LOAD_GLOBAL          10  'abs'
              287  LOAD_FAST            13  'ep'
              290  CALL_FUNCTION_1       1  None
              293  CALL_FUNCTION_2       2  None
              296  BINARY_MULTIPLY  
              297  COMPARE_OP            0  <
              300  POP_JUMP_IF_FALSE   319  'to 319'

 L. 199       303  LOAD_GLOBAL          12  'math'
              306  LOAD_ATTR            13  'pi'
              309  LOAD_CONST               2.0
              312  BINARY_DIVIDE    
              313  STORE_FAST           14  'angle'
              316  JUMP_FORWARD         22  'to 341'

 L. 201       319  LOAD_FAST             2  'cmath'
              322  LOAD_ATTR            14  'log'
              325  LOAD_FAST            12  'em'
              328  LOAD_FAST            13  'ep'
              331  BINARY_DIVIDE    
              332  CALL_FUNCTION_1       1  None
              335  LOAD_ATTR            15  'imag'
              338  STORE_FAST           14  'angle'
            341_0  COME_FROM           316  '316'

 L. 203       341  LOAD_FAST            14  'angle'
              344  LOAD_CONST               0.0
              347  COMPARE_OP            1  <=
              350  POP_JUMP_IF_FALSE   374  'to 374'
              353  LOAD_FAST            14  'angle'
              356  LOAD_CONST               -0.5
              359  COMPARE_OP            4  >
            362_0  COME_FROM           350  '350'
              362  POP_JUMP_IF_FALSE   374  'to 374'

 L. 204       365  LOAD_FAST             5  'EPS'
              368  STORE_FAST           14  'angle'
              371  JUMP_FORWARD          0  'to 374'
            374_0  COME_FROM           371  '371'

 L. 205       374  LOAD_FAST            14  'angle'
              377  LOAD_CONST               0.0
              380  COMPARE_OP            0  <
              383  POP_JUMP_IF_FALSE   406  'to 406'

 L. 206       386  LOAD_FAST            14  'angle'
              389  LOAD_CONST               2
              392  LOAD_GLOBAL          12  'math'
              395  LOAD_ATTR            13  'pi'
              398  BINARY_MULTIPLY  
              399  INPLACE_ADD      
              400  STORE_FAST           14  'angle'
              403  JUMP_FORWARD          0  'to 406'
            406_0  COME_FROM           403  '403'

 L. 207       406  LOAD_FAST            14  'angle'
              409  LOAD_GLOBAL          12  'math'
              412  LOAD_ATTR            13  'pi'
              415  COMPARE_OP            5  >=
              418  POP_JUMP_IF_FALSE   456  'to 456'
              421  LOAD_FAST            14  'angle'
              424  LOAD_GLOBAL          12  'math'
              427  LOAD_ATTR            13  'pi'
              430  LOAD_CONST               0.5
              433  BINARY_ADD       
              434  COMPARE_OP            0  <
            437_0  COME_FROM           418  '418'
              437  POP_JUMP_IF_FALSE   456  'to 456'

 L. 208       440  LOAD_GLOBAL          12  'math'
              443  LOAD_ATTR            13  'pi'
              446  LOAD_FAST             5  'EPS'
              449  BINARY_SUBTRACT  
              450  STORE_FAST           14  'angle'
              453  JUMP_FORWARD          0  'to 456'
            456_0  COME_FROM           453  '453'

 L. 210       456  LOAD_FAST            14  'angle'
              459  LOAD_CONST               0
              462  COMPARE_OP            5  >=
              465  POP_JUMP_IF_FALSE   483  'to 483'
              468  LOAD_FAST            14  'angle'
              471  LOAD_GLOBAL          12  'math'
              474  LOAD_ATTR            13  'pi'
              477  COMPARE_OP            1  <=
            480_0  COME_FROM           465  '465'
              480  POP_JUMP_IF_TRUE    496  'to 496'
              483  LOAD_ASSERT              AssertionError
              486  LOAD_CONST               'angle=%g'
              489  LOAD_FAST            14  'angle'
              492  BINARY_MODULO    
              493  RAISE_VARARGS_2       2  None

 L. 211       496  LOAD_FAST            14  'angle'
              499  LOAD_FAST            10  'wt'
              502  LOAD_FAST             9  'ee'
              505  LOAD_FAST            11  'i'
              508  BINARY_SUBSCR    
              509  STORE_SUBSCR     
              510  JUMP_BACK           195  'to 195'
              513  POP_BLOCK        
            514_0  COME_FROM           169  '169'

 L. 212       514  LOAD_FAST             4  'HUGE'
              517  STORE_FAST           15  'fmin'

 L. 213       520  SETUP_LOOP           53  'to 576'
              523  LOAD_FAST             8  'edge'
              526  GET_ITER         
              527  FOR_ITER             45  'to 575'
              530  STORE_FAST            7  'p'

 L. 214       533  LOAD_FAST             6  'Q'
              536  LOAD_FAST             7  'p'
              539  BINARY_SUBSCR    
              540  LOAD_FAST            10  'wt'
              543  LOAD_FAST             7  'p'
              546  BINARY_SUBSCR    
              547  BINARY_DIVIDE    
              548  STORE_FAST           16  'f'

 L. 215       551  LOAD_FAST            16  'f'
              554  LOAD_FAST            15  'fmin'
              557  COMPARE_OP            0  <
              560  POP_JUMP_IF_FALSE   527  'to 527'

 L. 216       563  LOAD_FAST            16  'f'
              566  STORE_FAST           15  'fmin'
              569  JUMP_BACK           527  'to 527'
              572  JUMP_BACK           527  'to 527'
              575  POP_BLOCK        
            576_0  COME_FROM           520  '520'

 L. 218       576  LOAD_FAST            15  'fmin'
              579  LOAD_CONST               0.0
              582  COMPARE_OP            4  >
              585  POP_JUMP_IF_TRUE    594  'to 594'
              588  LOAD_ASSERT              AssertionError
              591  RAISE_VARARGS_1       1  None

 L. 219       594  LOAD_GLOBAL          17  'complex'
              597  CALL_FUNCTION_0       0  None
              600  STORE_FAST           17  'sum'

 L. 220       603  LOAD_CONST               0.0
              606  STORE_FAST           18  'swt'

 L. 221       609  SETUP_LOOP          130  'to 742'
              612  LOAD_FAST             8  'edge'
              615  GET_ITER         
              616  FOR_ITER            122  'to 741'
              619  STORE_FAST            7  'p'

 L. 222       622  LOAD_FAST            15  'fmin'
              625  LOAD_FAST            10  'wt'
              628  LOAD_FAST             7  'p'
              631  BINARY_SUBSCR    
              632  BINARY_MULTIPLY  
              633  STORE_FAST           19  'fwp'

 L. 224       636  LOAD_FAST            18  'swt'
              639  LOAD_FAST            19  'fwp'
              642  INPLACE_ADD      
              643  STORE_FAST           18  'swt'

 L. 225       646  LOAD_FAST            17  'sum'
              649  LOAD_FAST             7  'p'
              652  LOAD_FAST            19  'fwp'
              655  BINARY_MULTIPLY  
              656  INPLACE_ADD      
              657  STORE_FAST           17  'sum'

 L. 226       660  LOAD_FAST             6  'Q'
              663  LOAD_FAST             7  'p'
              666  BINARY_SUBSCR    
              667  LOAD_FAST            19  'fwp'
              670  LOAD_FAST             5  'EPS'
              673  BINARY_ADD       
              674  COMPARE_OP            4  >
              677  POP_JUMP_IF_FALSE   699  'to 699'

 L. 227       680  LOAD_FAST             6  'Q'
              683  LOAD_FAST             7  'p'
              686  DUP_TOPX_2            2  None
              689  BINARY_SUBSCR    
              690  LOAD_FAST            19  'fwp'
              693  INPLACE_SUBTRACT 
              694  ROT_THREE        
              695  STORE_SUBSCR     
              696  JUMP_BACK           616  'to 616'

 L. 230       699  LOAD_GLOBAL          10  'abs'
              702  LOAD_FAST             6  'Q'
              705  LOAD_FAST             7  'p'
              708  BINARY_SUBSCR    
              709  LOAD_FAST            19  'fwp'
              712  BINARY_SUBTRACT  
              713  CALL_FUNCTION_1       1  None
              716  LOAD_FAST             5  'EPS'
              719  COMPARE_OP            0  <
              722  POP_JUMP_IF_TRUE    731  'to 731'
              725  LOAD_ASSERT              AssertionError
              728  RAISE_VARARGS_1       1  None

 L. 232       731  LOAD_FAST             6  'Q'
              734  LOAD_FAST             7  'p'
              737  DELETE_SUBSCR    
              738  JUMP_BACK           616  'to 616'
              741  POP_BLOCK        
            742_0  COME_FROM           609  '609'

 L. 233       742  LOAD_GLOBAL           5  'len'
              745  LOAD_FAST             6  'Q'
              748  CALL_FUNCTION_1       1  None
              751  LOAD_CONST               0
              754  COMPARE_OP            2  ==
              757  POP_JUMP_IF_FALSE    96  'to 96'

 L. 234       760  LOAD_FAST            17  'sum'
              763  LOAD_FAST            18  'swt'
              766  BINARY_DIVIDE    
              767  RETURN_END_IF    
            768_0  COME_FROM           757  '757'
              768  JUMP_BACK            96  'to 96'
              771  POP_BLOCK        
            772_0  COME_FROM            93  '93'

 L. 236       772  LOAD_GLOBAL          17  'complex'
              775  CALL_FUNCTION_0       0  None
              778  STORE_FAST           17  'sum'

 L. 237       781  LOAD_CONST               0.0
              784  STORE_FAST           20  'w'

 L. 238       787  SETUP_LOOP           50  'to 840'
              790  LOAD_FAST             6  'Q'
              793  LOAD_ATTR            18  'items'
              796  CALL_FUNCTION_0       0  None
              799  GET_ITER         
              800  FOR_ITER             36  'to 839'
              803  UNPACK_SEQUENCE_2     2 
              806  STORE_FAST            7  'p'
              809  STORE_FAST           21  'n'

 L. 239       812  LOAD_FAST            17  'sum'
              815  LOAD_FAST             7  'p'
              818  LOAD_FAST            21  'n'
              821  BINARY_MULTIPLY  
              822  INPLACE_ADD      
              823  STORE_FAST           17  'sum'

 L. 240       826  LOAD_FAST            20  'w'
              829  LOAD_FAST            21  'n'
              832  INPLACE_ADD      
              833  STORE_FAST           20  'w'
              836  JUMP_BACK           800  'to 800'
              839  POP_BLOCK        
            840_0  COME_FROM           787  '787'

 L. 241       840  LOAD_FAST            17  'sum'
              843  LOAD_FAST            20  'w'
              846  BINARY_DIVIDE    
              847  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 513


def testCM():

    def eq(a, b):
        tmp = abs(a - b) / (abs(a) + abs(b)) < 1e-06
        if not tmp:
            print 'eq fails: %s vs %s' % (str(a), str(b))
        return tmp

    print 'CM'
    assert eq(ComplexMedian([complex(1, 0), complex(2, 0), complex(3, 0)]), 2)
    assert eq(ComplexMedian([complex(1), complex(2), complex(3), complex(4)]), 2.5)
    assert eq(ComplexMedian([complex(1), complex(2), complex(3), complex(4), complex(5)]), 3)
    assert eq(ComplexMedian([complex(1), complex(2), complex(3), complex(4), complex(4)]), 3)
    assert eq(ComplexMedian([complex(1, 1), complex(2, 2), complex(3, 3), complex(4, 4)]), complex(2.5, 2.5))
    assert eq(ComplexMedian([complex(0, 0), complex(1, 0), complex(0, 1), complex(1, 1)]), complex(0.5, 0.5))
    assert eq(ComplexMedian([complex(0, 0), complex(1, 0), complex(0, 1),
     complex(1, 1), complex(1, 1)]), complex(1, 1))
    assert eq(ComplexMedian([complex(0, 0), complex(1, 0), complex(0, 1),
     complex(1, 1), complex(0.6, 0.6)]), complex(0.6, 0.6))
    assert eq(ComplexMedian([complex(0, 0), complex(1, 0), complex(0, 1), complex(1, 1),
     complex(0, 0), complex(2, 0), complex(0, 2), complex(2, 2)]), complex(0.5, 0.5))
    assert eq(ComplexMedian([complex(0, 0), complex(1, 0), complex(0, 1)]), complex(1.0 / 3.0, 1.0 / 3.0))
    assert eq(ComplexMedian([complex(0, 0), complex(1, 0), complex(0, 1),
     complex(0, 0), complex(2, 0), complex(0, 2)]), complex(0.3, 0.3))
    import cmath
    for N in [3, 4, 5, 6, 7, 8, 13, 40, 100, 2351]:
        print 'N=', N
        assert eq(ComplexMedian([ 1 + cmath.exp(2 * cmath.pi * complex(0.0, 1.0) * float(q) / N) for q in range(N)
                                ]), complex(1.0, 0.0))


import Queue, threading

class threaded_readable_file(object):
    QSIZE = 100
    _string = type('')

    def __init__(self, fd):
        self.q = Queue.Queue(self.QSIZE)

        def rhelper(fd, q):
            try:
                for l in fd:
                    q.put(l)

                q.put(None)
            except (Exception, KeyboardInterrupt):
                q.put(sys.exc_info())

            return

        self.rh = threading.Thread(target=rhelper, args=(fd, self.q))
        self.rh.start()

    def readline(self):
        if self.q is None:
            return ''
        else:
            x = self.q.get()
            if type(x) != self._string:
                self.rh.join()
                self.q = None
                if x is not None:
                    raise x[0], x[1], x[2]
                return ''
            return x

    def readlines(self):
        o = []
        while self.q is not None:
            x = self.q.get()
            if type(x) != self._string:
                self.rh.join()
                self.q = None
                if x is not None:
                    raise x[0], x[1], x[2]
                break
            o.append(x)

        return o

    def read_iter(self):
        while self.q is not None:
            x = self.q.get()
            if type(x) != self._string:
                self.rh.join()
                self.q = None
                if x is not None:
                    raise x[0], x[1], x[2]
                break
            yield x

        return

    __iter__ = read_iter


def thr_iter_read(fd):
    """Read the contents of a file as an iterator.
        The read is two-threaded, so that one thread can be
        waiting on disk I/O while the other thread is
        processing the results.
        """
    x = threaded_readable_file(fd)
    return x.read_iter()


def makedirs(fname, mode=509):
    """This makes the specified directory, including all
        necessary directories above it.    It is like os.makedirs(),
        except that if the directory already exists
        it does not raise an exception.
        @param fname:Name of the directory to create.
        @param mode: Linux file permissions for any directories it needs to create.
        @type fname: L{str}
        @type mode: L{int}
        @note: If the directory already exists, it does not force it to
                have the specified C{mode}.
        @except OSError: If it cannot create a part of the directory chain.
        """
    c = fname.split('/')
    for i in range(1 + (c[0] == ''), len(c) + 1):
        p = ('/').join(c[:i])
        try:
            os.mkdir(p, mode)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise


def shuffle_Nrep--- This code section failed: ---

 L. 397         0  LOAD_CONST               -1
                3  LOAD_CONST               None
                6  IMPORT_NAME           0  'random'
                9  STORE_FAST            3  'random'

 L. 398        12  LOAD_FAST             1  'n'
               15  LOAD_CONST               0
               18  COMPARE_OP            4  >
               21  POP_JUMP_IF_TRUE     33  'to 33'
               24  LOAD_ASSERT              AssertionError
               27  LOAD_CONST               'Silly!'
               30  RAISE_VARARGS_2       2  None

 L. 399        33  LOAD_GLOBAL           2  'list'
               36  LOAD_FAST             0  'y'
               39  CALL_FUNCTION_1       1  None
               42  STORE_FAST            4  'x'

 L. 400        45  LOAD_FAST             3  'random'
               48  LOAD_ATTR             3  'shuffle'
               51  LOAD_FAST             4  'x'
               54  CALL_FUNCTION_1       1  None
               57  POP_TOP          

 L. 401        58  LOAD_GLOBAL           4  'len'
               61  LOAD_FAST             4  'x'
               64  CALL_FUNCTION_1       1  None
               67  STORE_FAST            5  'm'

 L. 402        70  LOAD_FAST             2  'compare'
               73  LOAD_CONST               None
               76  COMPARE_OP            8  is
               79  POP_JUMP_IF_FALSE    94  'to 94'

 L. 403        82  LOAD_LAMBDA              '<code_object <lambda>>'
               85  MAKE_FUNCTION_0       0  None
               88  STORE_FAST            2  'compare'
               91  JUMP_FORWARD          0  'to 94'
             94_0  COME_FROM            91  '91'

 L. 405        94  LOAD_CONST               0
               97  STORE_FAST            6  'passes'

 L. 406       100  LOAD_CONST               0
              103  STORE_FAST            7  'restart'

 L. 407       106  SETUP_LOOP          371  'to 480'
              109  LOAD_FAST             6  'passes'
              112  LOAD_CONST               1000
              115  COMPARE_OP            0  <
              118  POP_JUMP_IF_FALSE   479  'to 479'

 L. 408       121  LOAD_CONST               None
              124  STORE_FAST            8  'prb'

 L. 409       127  LOAD_CONST               0
              130  STORE_FAST            9  'pstart'

 L. 410       133  LOAD_CONST               0
              136  STORE_FAST           10  'reps'

 L. 413       139  SETUP_LOOP          116  'to 258'
              142  LOAD_GLOBAL           6  'range'
              145  LOAD_GLOBAL           7  'max'
              148  LOAD_CONST               1
              151  LOAD_FAST             7  'restart'
              154  CALL_FUNCTION_2       2  None
              157  LOAD_FAST             5  'm'
              160  CALL_FUNCTION_2       2  None
              163  GET_ITER         
              164  FOR_ITER             90  'to 257'
              167  STORE_FAST           11  'i'

 L. 414       170  LOAD_FAST             2  'compare'
              173  LOAD_FAST             4  'x'
              176  LOAD_FAST            11  'i'
              179  LOAD_CONST               1
              182  BINARY_SUBTRACT  
              183  BINARY_SUBSCR    
              184  LOAD_FAST             4  'x'
              187  LOAD_FAST            11  'i'
              190  BINARY_SUBSCR    
              191  CALL_FUNCTION_2       2  None
              194  POP_JUMP_IF_FALSE   220  'to 220'

 L. 415       197  LOAD_FAST            10  'reps'
              200  LOAD_CONST               1
              203  INPLACE_ADD      
              204  STORE_FAST           10  'reps'

 L. 416       207  LOAD_FAST            11  'i'
              210  LOAD_CONST               1
              213  BINARY_SUBTRACT  
              214  STORE_FAST            9  'pstart'
              217  JUMP_FORWARD         12  'to 232'

 L. 418       220  LOAD_CONST               None
              223  STORE_FAST            9  'pstart'

 L. 419       226  LOAD_CONST               0
              229  STORE_FAST           10  'reps'
            232_0  COME_FROM           217  '217'

 L. 420       232  LOAD_FAST            10  'reps'
              235  LOAD_FAST             1  'n'
              238  COMPARE_OP            5  >=
              241  POP_JUMP_IF_FALSE   164  'to 164'

 L. 422       244  LOAD_FAST            11  'i'
              247  STORE_FAST            8  'prb'

 L. 423       250  BREAK_LOOP       
              251  JUMP_BACK           164  'to 164'
              254  JUMP_BACK           164  'to 164'
              257  POP_BLOCK        
            258_0  COME_FROM           139  '139'

 L. 424       258  LOAD_FAST             8  'prb'
              261  LOAD_CONST               None
              264  COMPARE_OP            8  is
              267  POP_JUMP_IF_FALSE   281  'to 281'

 L. 426       270  LOAD_FAST             4  'x'
              273  LOAD_FAST             0  'y'
              276  STORE_SLICE+0    

 L. 427       277  LOAD_FAST             0  'y'
              280  RETURN_END_IF    
            281_0  COME_FROM           267  '267'

 L. 429       281  LOAD_FAST             8  'prb'
              284  LOAD_CONST               1
              287  BINARY_ADD       
              288  STORE_FAST           12  'k'

 L. 432       291  LOAD_GLOBAL           8  'False'
              294  STORE_FAST           13  'found'

 L. 433       297  SETUP_LOOP           59  'to 359'
              300  LOAD_FAST            12  'k'
              303  LOAD_FAST             5  'm'
              306  COMPARE_OP            0  <
              309  POP_JUMP_IF_FALSE   358  'to 358'

 L. 434       312  LOAD_FAST             2  'compare'
              315  LOAD_FAST             4  'x'
              318  LOAD_FAST             9  'pstart'
              321  BINARY_SUBSCR    
              322  LOAD_FAST             4  'x'
              325  LOAD_FAST            12  'k'
              328  BINARY_SUBSCR    
              329  CALL_FUNCTION_2       2  None
              332  POP_JUMP_IF_TRUE    345  'to 345'

 L. 435       335  LOAD_GLOBAL           9  'True'
              338  STORE_FAST           13  'found'

 L. 436       341  BREAK_LOOP       
              342  JUMP_FORWARD          0  'to 345'
            345_0  COME_FROM           342  '342'

 L. 437       345  LOAD_FAST            12  'k'
              348  LOAD_CONST               1
              351  INPLACE_ADD      
              352  STORE_FAST           12  'k'
              355  JUMP_BACK           300  'to 300'
              358  POP_BLOCK        
            359_0  COME_FROM           297  '297'

 L. 438       359  LOAD_FAST            13  'found'
              362  POP_JUMP_IF_TRUE    405  'to 405'

 L. 442       365  LOAD_FAST             4  'x'
              368  LOAD_ATTR            10  'pop'
              371  LOAD_CONST               0
              374  CALL_FUNCTION_1       1  None
              377  STORE_FAST           14  'tmp'

 L. 443       380  LOAD_FAST             4  'x'
              383  LOAD_ATTR            11  'append'
              386  LOAD_FAST            14  'tmp'
              389  CALL_FUNCTION_1       1  None
              392  POP_TOP          

 L. 444       393  LOAD_CONST               0
              396  STORE_FAST            7  'restart'

 L. 445       399  CONTINUE            109  'to 109'
              402  JUMP_FORWARD          0  'to 405'
            405_0  COME_FROM           402  '402'

 L. 448       405  LOAD_FAST             9  'pstart'
              408  STORE_FAST           15  'a'

 L. 449       411  LOAD_FAST            12  'k'
              414  LOAD_CONST               1
              417  BINARY_ADD       
              418  STORE_FAST           16  'b'

 L. 451       421  LOAD_FAST             4  'x'
              424  LOAD_FAST            15  'a'
              427  LOAD_FAST            16  'b'
              430  SLICE+3          
              431  STORE_FAST           14  'tmp'

 L. 452       434  LOAD_FAST             3  'random'
              437  LOAD_ATTR             3  'shuffle'
              440  LOAD_FAST            14  'tmp'
              443  CALL_FUNCTION_1       1  None
              446  POP_TOP          

 L. 454       447  LOAD_FAST            14  'tmp'
              450  LOAD_FAST             4  'x'
              453  LOAD_FAST            15  'a'
              456  LOAD_FAST            16  'b'
              459  STORE_SLICE+3    

 L. 455       460  LOAD_FAST            15  'a'
              463  STORE_FAST            7  'restart'

 L. 456       466  LOAD_FAST             6  'passes'
              469  LOAD_CONST               1
              472  INPLACE_ADD      
              473  STORE_FAST            6  'passes'
              476  JUMP_BACK           109  'to 109'
              479  POP_BLOCK        
            480_0  COME_FROM           106  '106'

 L. 458       480  LOAD_GLOBAL          12  'RuntimeError'
              483  LOAD_CONST               'Too many passes: cannot avoid repetitions'
              486  RAISE_VARARGS_2       2  None
              489  LOAD_CONST               None
              492  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 489


def testSNR():
    import random
    for i in range(20):
        x = [ i // 10 for i in range(20) ]
        shuffle_Nrep(x, 1)
        for i in range(len(x) - 1):
            if not x[i] != x[(i + 1)]:
                raise AssertionError, 'Whoops: i=%d, %d %d' % (i, x[i], x[(i + 1)])

        x = [ i // 3 for i in range(10000) ]
        random.shuffle(x)
        shuffle_Nrep(x, 1)
        for i in range(len(x) - 1):
            if not x[i] != x[(i + 1)]:
                raise AssertionError, 'Whoops: i=%d, %d %d' % (i, x[i], x[(i + 1)])


class dir_lock(object):

    def __init__(self, lockname):
        self.maxtries = 10
        self.name = lockname
        self.pid = os.getpid()
        self.sleep = 2.0

    def __enter__--- This code section failed: ---

 L. 484         0  LOAD_CONST               0
                3  STORE_FAST            1  'locktries'

 L. 485         6  LOAD_GLOBAL           0  'os'
                9  LOAD_ATTR             1  'path'
               12  LOAD_ATTR             2  'dirname'
               15  LOAD_FAST             0  'self'
               18  LOAD_ATTR             3  'name'
               21  CALL_FUNCTION_1       1  None
               24  STORE_FAST            2  'd'

 L. 486        27  LOAD_FAST             2  'd'
               30  POP_JUMP_IF_TRUE     42  'to 42'

 L. 487        33  LOAD_CONST               '.'
               36  STORE_FAST            2  'd'
               39  JUMP_FORWARD          0  'to 42'
             42_0  COME_FROM            39  '39'

 L. 488        42  LOAD_GLOBAL           0  'os'
               45  LOAD_ATTR             1  'path'
               48  LOAD_ATTR             4  'isdir'
               51  LOAD_FAST             2  'd'
               54  CALL_FUNCTION_1       1  None
               57  POP_JUMP_IF_TRUE     73  'to 73'
               60  LOAD_ASSERT              AssertionError
               63  LOAD_CONST               '%s is not a directory'
               66  LOAD_FAST             2  'd'
               69  BINARY_MODULO    
               70  RAISE_VARARGS_2       2  None

 L. 489        73  LOAD_GLOBAL           0  'os'
               76  LOAD_ATTR             6  'access'
               79  LOAD_FAST             2  'd'
               82  LOAD_GLOBAL           0  'os'
               85  LOAD_ATTR             7  'W_OK'
               88  LOAD_GLOBAL           0  'os'
               91  LOAD_ATTR             8  'X_OK'
               94  BINARY_OR        
               95  CALL_FUNCTION_2       2  None
               98  POP_JUMP_IF_TRUE    114  'to 114'
              101  LOAD_ASSERT              AssertionError
              104  LOAD_CONST               '%s is not writeable'
              107  LOAD_FAST             2  'd'
              110  BINARY_MODULO    
              111  RAISE_VARARGS_2       2  None

 L. 490       114  LOAD_GLOBAL           9  'set'
              117  CALL_FUNCTION_0       0  None
              120  STORE_FAST            3  'errs'

 L. 491       123  SETUP_LOOP          140  'to 266'
              126  LOAD_FAST             1  'locktries'
              129  LOAD_FAST             0  'self'
              132  LOAD_ATTR            10  'maxtries'
              135  COMPARE_OP            0  <
              138  POP_JUMP_IF_FALSE   265  'to 265'

 L. 492       141  SETUP_EXCEPT         20  'to 164'

 L. 493       144  LOAD_GLOBAL           0  'os'
              147  LOAD_ATTR            11  'mkdir'
              150  LOAD_FAST             0  'self'
              153  LOAD_ATTR             3  'name'
              156  CALL_FUNCTION_1       1  None
              159  POP_TOP          
              160  POP_BLOCK        
              161  JUMP_FORWARD         91  'to 255'
            164_0  COME_FROM           141  '141'

 L. 494       164  DUP_TOP          
              165  LOAD_GLOBAL          12  'OSError'
              168  COMPARE_OP           10  exception-match
              171  POP_JUMP_IF_FALSE   254  'to 254'
              174  POP_TOP          
              175  STORE_FAST            4  'x'
              178  POP_TOP          

 L. 495       179  LOAD_FAST             3  'errs'
              182  LOAD_ATTR            13  'add'
              185  LOAD_GLOBAL          14  'str'
              188  LOAD_FAST             4  'x'
              191  CALL_FUNCTION_1       1  None
              194  CALL_FUNCTION_1       1  None
              197  POP_TOP          

 L. 496       198  LOAD_FAST             1  'locktries'
              201  LOAD_CONST               1
              204  INPLACE_ADD      
              205  STORE_FAST            1  'locktries'

 L. 497       208  LOAD_GLOBAL          15  'time'
              211  LOAD_ATTR            16  'sleep'
              214  LOAD_FAST             0  'self'
              217  LOAD_ATTR            16  'sleep'
              220  LOAD_FAST             0  'self'
              223  LOAD_ATTR            17  'pid'
              226  LOAD_CONST               97
              229  LOAD_FAST             1  'locktries'
              232  BINARY_MULTIPLY  
              233  BINARY_ADD       
              234  LOAD_CONST               197
              237  BINARY_MODULO    
              238  LOAD_CONST               197.0
              241  BINARY_DIVIDE    
              242  LOAD_CONST               2
              245  BINARY_POWER     
              246  BINARY_MULTIPLY  
              247  CALL_FUNCTION_1       1  None
              250  POP_TOP          
              251  JUMP_BACK           126  'to 126'
              254  END_FINALLY      
            255_0  COME_FROM           161  '161'

 L. 499       255  LOAD_CONST               None
              258  STORE_FAST            2  'd'

 L. 500       261  BREAK_LOOP       
            262_0  COME_FROM           254  '254'
              262  JUMP_BACK           126  'to 126'
              265  POP_BLOCK        
            266_0  COME_FROM           123  '123'

 L. 501       266  LOAD_FAST             2  'd'
              269  LOAD_CONST               None
              272  COMPARE_OP            9  is-not
              275  POP_JUMP_IF_FALSE   337  'to 337'

 L. 502       278  LOAD_GLOBAL          19  'die'
              281  LOAD_ATTR            20  'warn'
              284  LOAD_CONST               'Could not acquire lock %s in %d tries (%s): continuing anyway.'
              287  LOAD_FAST             0  'self'
              290  LOAD_ATTR             3  'name'
              293  LOAD_FAST             0  'self'
              296  LOAD_ATTR            10  'maxtries'
              299  LOAD_CONST               ','
              302  LOAD_ATTR            21  'join'
              305  LOAD_GLOBAL          22  'sorted'
              308  LOAD_FAST             3  'errs'
              311  CALL_FUNCTION_1       1  None
              314  CALL_FUNCTION_1       1  None
              317  BUILD_TUPLE_3         3 
              320  BINARY_MODULO    
              321  CALL_FUNCTION_1       1  None
              324  POP_TOP          

 L. 503       325  LOAD_CONST               None
              328  LOAD_FAST             0  'self'
              331  STORE_ATTR            3  'name'
              334  JUMP_FORWARD          0  'to 337'
            337_0  COME_FROM           334  '334'

 L. 504       337  LOAD_FAST             0  'self'
              340  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 337

    def __exit__(self, exc_type, exc_value, traceback):
        if self.name:
            os.rmdir(self.name)


def open_nowipe(nm1, nm2, mode='w'):
    """Open a file (typically for writing) but make sure that the
        file doesn't already exist.   The name is constructed from
        nm1, a sequence number, and nm2.   The sequence number gets incremented
        until a name is found that doesn't exist.
        This works by creating a directory as a lock file; it should be safe across
        NFS.
        @note: The directory containing C{nm1} must exist and be writeable.
        @param nm1: the part of the name to the left of the sequence number
        @param nm2: the part of the name to the right of the sequence number
                Typically, nm2 is a suffix like ".wav".  This may not contain a slash.
        @param mode: The way to open the file -- passed to open().
        @type nm1: str
        @type nm2: str
        @type mode: str
        @rtype C{file}
        @return: The opened L{file} object.  (Its name can be gotten from the C{name} attribute.)
        """
    dname = os.path.dirname(nm1)
    lockf = os.path.join(dname, '.gmisclib.gpkmisc.nowipe_lock')
    with dir_lock(lockf):
        i = 0
        try:
            while True:
                nm = '%s%d%s' % (nm1, i, nm2)
                open(nm, 'r')
                i += 1

        except IOError:
            pass

        return open(nm, mode)


def dropfront(prefix, s):
    """Drops the prefix from the string and raises an exception
        if it is not there to be dropped.
        """
    if not s.startswith(prefix):
        raise ValueError, "String '%s' must start with '%s'" % (s[:20], prefix)
    return s[len(prefix):]


def open_compressed(fn):
    import g_pipe
    if fn.endswith('.bz2'):
        ci, co = g_pipe.popen2('bzcat', ['bzcat', fn])
        ci.close()
        return co
    if fn.endswith('.gz'):
        ci, co = g_pipe.popen2('zcat', ['zcat', fn])
        ci.close()
        return co
    return open(fn, 'r')


def gammaln(x):
    raise RuntimeError, 'Please import gammaln from gmisclib.stats'


_a_factor_cache = {1: 1, 2: 2, 3: 3}

def a_factor(n):
    """Finds the smallest prime factor of a number."""
    try:
        return _a_factor_cache[n]
    except KeyError:
        pass

    for p in primes():
        if p * p > n:
            f = n
            break
        if n % p == 0:
            f = p
            break

    _a_factor_cache[n] = f
    return f


_primes = [
 2, 3]

def primes():
    """This is a generator that produces an infinite list of primes.
        """
    for p in _primes:
        yield p

    i = _primes[(-1)] + 2
    while True:
        for p in primes():
            if p * p > i:
                if p > _primes[(-1)]:
                    _primes.append(i)
                yield i
            if i % p == 0:
                i += 2
                break


_factor_cache = {}

def factor(n):
    """Factor a number into a list of prime factors,
        in increasing order.
        @param n: input number
        @type n: int
        @return: prime factors
        @rtype: list
        """
    try:
        return _factor_cache[n]
    except KeyError:
        pass

    f = a_factor(n)
    if f == n:
        tmp = [
         n]
    else:
        tmp = [
         f] + factor(n // f)
    _factor_cache[n] = tmp[:]
    return tmp


def test_primes():
    assert factor(11) == [11]
    assert factor(16) == [2, 2, 2, 2]
    assert factor(100) == [2, 2, 5, 5]
    assert factor(2) == [2]
    assert factor(97) == [97]
    assert factor(55) == [5, 11]
    assert gcd(5, 3) == 1
    assert gcd(14, 21) == 7
    assert gcd(100, 70) == 10


def gcd(a, b):
    """Greatest common factor/denominator.
        @type a: int
        @type b: int
        @rtype: int
        @return: the greatest common factor of a and b.
        """
    assert a >= 0 and b >= 0
    while b != 0:
        tmp = b
        b = a % b
        a = tmp

    return a


def find_in_PATH(progname):
    """Search PATH to find where a program resides.
        @param progname: the program to look for.
        @type progname: str
        @return: the full path name.
        @rtype: str
        """
    for p in os.environ['PATH'].split(':'):
        tmp = os.path.join(p, progname)
        if os.access(tmp, os.R_OK | os.X_OK):
            return tmp

    return


def get_mtime(fn):
    """Paired with L{need_to_recompute}().   These implement something like make,
        where we figure out if we need to compute things based on the age of files.
        This is used to get the age of the pre-requisites.
        @param fn: a filename or a file
        @type fn: str or file
        @return: None (if the file doesn't exist) or its modification time.
        @rtype: None or float
        """
    try:
        if isinstance(fn, file):
            s = os.fstat(fn.fileno())
        else:
            s = os.stat(fn)
    except OSError:
        return

    return s[stat.ST_MTIME]


class PrereqError(ValueError):

    def __init__(self, *s):
        ValueError.__init__(self, *s)

    def repl(self, x):
        self.args = self.args[:-1] + (x,)


def prereq_mtime(*tlist):
    if None in tlist:
        raise PrereqError('Prerequisite has not been computed yet', tlist.index(None))
    return max(tlist)


def need_to_recompute(fn, lazytime, size=-1):
    """Paired with L{get_mtime}().   These implement something like make,
        where we figure out if we need to compute things.
        @param fn: a filename or a file
        @type fn: C{str} or C{file}
        @param lazytime: a time (as obtained from ST_MTIME in os.stat()).
                If the file modification time of C{fn} is older than
                C{lazytime}, recompute.
        @type lazytime: C{None} or C{float}
        @param size: recompute the file if it is smaller than C{size}.
                Normally, this is used to recompute on empty output
                files by setting C{size=0}.
        @type size: int
        @return: True if fn needs to be recomputed or if it doesn not exist.
        @rtype: bool
        """
    if lazytime is None and size < 0:
        return True
    else:
        try:
            if isinstance(fn, file):
                s = os.fstat(fn.fileno())
            else:
                s = os.stat(fn)
        except OSError:
            return True

        if size and s[stat.ST_SIZE] <= size:
            return True
        return s[stat.ST_MTIME] <= lazytime


def truncate(s, maxlen):
    assert maxlen > 3
    if len(s) < maxlen:
        return s
    return s[:maxlen - 3] + '...'


def erf(x):
    """erf(x)=(2/sqrt(pi))*integral{0 to x of exp(-t**2) dt}"""
    sign = 1
    if x < 0:
        sign = -1
        x = -x
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y


def asinh(x):
    """Inverse hyperbolic sine."""
    if x > 0:
        sign = 1
    elif x == 0:
        sign = 0
    else:
        sign = -1
    return sign * math.log(sign * x + math.sqrt(x * x + 1))


def chooseP--- This code section failed: ---

 L. 792         0  LOAD_CONST               -1
                3  LOAD_CONST               None
                6  IMPORT_NAME           0  'random'
                9  STORE_FAST            2  'random'

 L. 793        12  LOAD_CONST               0.0
               15  STORE_FAST            3  'ps'

 L. 794        18  LOAD_FAST             2  'random'
               21  LOAD_ATTR             0  'random'
               24  CALL_FUNCTION_0       0  None
               27  STORE_FAST            4  'r'

 L. 795        30  SETUP_LOOP          114  'to 147'
               33  LOAD_GLOBAL           1  'zip'
               36  LOAD_FAST             0  'x'
               39  LOAD_FAST             1  'p'
               42  CALL_FUNCTION_2       2  None
               45  GET_ITER         
               46  FOR_ITER             97  'to 146'
               49  UNPACK_SEQUENCE_2     2 
               52  STORE_FAST            5  'xx'
               55  STORE_FAST            6  'pp'

 L. 796        58  LOAD_FAST             3  'ps'
               61  LOAD_FAST             6  'pp'
               64  INPLACE_ADD      
               65  STORE_FAST            3  'ps'

 L. 797        68  LOAD_CONST               0
               71  LOAD_FAST             6  'pp'
               74  DUP_TOP          
               75  ROT_THREE        
               76  COMPARE_OP            1  <=
               79  JUMP_IF_FALSE_OR_POP    91  'to 91'
               82  LOAD_CONST               1.0
               85  COMPARE_OP            1  <=
               88  JUMP_FORWARD          2  'to 93'
             91_0  COME_FROM            79  '79'
               91  ROT_TWO          
               92  POP_TOP          
             93_0  COME_FROM            88  '88'
               93  POP_JUMP_IF_FALSE   108  'to 108'
               96  LOAD_FAST             3  'ps'
               99  LOAD_CONST               1.0
              102  COMPARE_OP            1  <=
            105_0  COME_FROM            93  '93'
              105  POP_JUMP_IF_TRUE    117  'to 117'
              108  LOAD_ASSERT              AssertionError
              111  LOAD_CONST               'Bad probabilities'
              114  RAISE_VARARGS_2       2  None

 L. 798       117  LOAD_FAST             6  'pp'
              120  LOAD_FAST             4  'r'
              123  COMPARE_OP            4  >
              126  POP_JUMP_IF_FALSE   133  'to 133'

 L. 799       129  LOAD_FAST             5  'xx'
              132  RETURN_END_IF    
            133_0  COME_FROM           126  '126'

 L. 801       133  LOAD_FAST             4  'r'
              136  LOAD_FAST             6  'pp'
              139  INPLACE_SUBTRACT 
              140  STORE_FAST            4  'r'
              143  JUMP_BACK            46  'to 46'
              146  POP_BLOCK        
            147_0  COME_FROM            30  '30'

 L. 802       147  LOAD_GLOBAL           2  'AssertionError'
              150  LOAD_CONST               'Probabilities sum to %g, not 1.0'
              153  LOAD_FAST             3  'ps'
              156  BINARY_MODULO    
              157  RAISE_VARARGS_2       2  None

Parse error at or near `POP_BLOCK' instruction at offset 146


def misc_mode(lx):
    """@return: The most common object from a list of arbitrary objects.
        @param lx: a sequence of hashable objects.
        """
    from gmisclib import dictops
    c = dictops.dict_of_accums()
    for x in lx:
        c.add(x, 1)

    vmax = 0
    kmax = None
    for k, v in c.items():
        if v > vmax:
            kmax = k
            vmax = v

    if not vmax > 0:
        raise ValueError, 'Empty list'
    return kmax


def distrib(key):
    """
        @return: The release name of the linux distribution that you're running.
        @rtype: str
        """
    fname = '/etc/lsb-release'
    for l in open(fname, 'r'):
        l = l.strip()
        x = l.split('=')
        if len(x) == 2 and x[0] == 'DISTRIB_%s' % key:
            return x[1].strip()

    raise KeyError, 'Cannot find DISTRIB_%s in %s' % (key, fname)


if __name__ == '__main__':
    testCM()
    testSNR()
    test_primes()