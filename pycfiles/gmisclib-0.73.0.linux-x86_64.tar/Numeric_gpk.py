# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/Numeric_gpk.py
# Compiled at: 2010-09-12 14:40:21
import numpy, math
pylab = None

def add_overlap(a, astart, b, bstart):
    """Add arrays a and b in the overlap region.
        Return (data, start).
        If a, b are time series, they are assumed to have the
        same sampling rate.
        Astart and Bstart apply to the zeroth index.
        All other indices are assumed to match start and length.
        """
    start = max(astart, bstart)
    end = min(astart + a.shape[0], bstart + b.shape[0])
    out = a[start - astart:end - astart] + b[start - bstart:end - bstart]
    return (
     out, start)


asinh = numpy.arcsinh
acosh = numpy.arccosh

def zero_pad_end(d, padfactor=1):
    if padfactor == 0:
        return numpy.array(d, copy=True)
    if padfactor <= 0:
        raise ValueError, 'pad factor <= 0'
    assert len(d.shape) == 1
    n = d.shape[0]
    npad = int(round(n * padfactor))
    return numpy.concatenate((d, numpy.zeros((npad,), numpy.double)))


def Poisson(nbar):
    """Return a Poisson random integer, whose distribution has
        a mean = nbar.
        """
    import random
    assert nbar >= 0.0
    if nbar < 20.0:
        L = math.exp(-nbar)
        k = -1
        p = 1.0
        while p >= L:
            k += 1
            p *= random.random()

    else:
        lp = 0.0
        lL = -nbar
        k = 0
        chunk = min(int(round(1 + nbar + 3 * math.sqrt(nbar))), 10000)
        while lp >= lL:
            ptmp = numpy.log(numpy.random.uniform(0.0, 1.0, chunk))
            lpp = numpy.add.accumulate(ptmp) + lp
            fsm = numpy.nonzero(numpy.less(lpp, lL))[0]
            if fsm.shape[0] != 0:
                k += fsm[0]
                break
            k += ptmp.shape[0]
            lp = lpp[(-1)]

    return k


def _test_Poisson():
    Nbar = 0.01
    N = int(round(1000 / Nbar))
    s = 0
    for i in range(N):
        s += Poisson(Nbar)

    assert abs(s - N * Nbar) < 5 * math.sqrt(N * Nbar)
    Nbar = 25.0
    N = 1000
    s = 0
    for i in range(N):
        s += Poisson(Nbar)

    assert abs(s - N * Nbar) < 5 * math.sqrt(N * Nbar)


def bevel_concat(a, b, bevel=0, bevel_overlap=1.0, delay=0, ta=None, tb=None):
    """Concatenate two time series.  Bevel the edges,
        and overlap them slightly.

        Bevel_overlap controls the fractional overlap of the two bevels,
        and delay specifies an extra delay for b.

        If ta and/or tb are specified, return a tuple of
        (concatenated_time_series, tma, tmb) where tma and tmb are the locations
        corresponding to ta and tb in the corresponding input arrays.
        """
    assert bevel >= 0
    if bevel > 0:
        bev = (0.5 + numpy.arange(bevel)) / float(bevel)
    else:
        bev = 1
    bc = numpy.array(b, copy=True)
    bev = (0.5 + numpy.arange(bevel)) / float(bevel)
    ans = a.shape[0] - 1
    bns = bc.shape[0] - 1
    bos = a.shape[0] - int(round(bevel_overlap * bevel)) + delay
    boe = bos + bc.shape[0]
    o = numpy.zeros((boe,), numpy.double)
    o[:(a.shape[0])] = a
    if bevel > 0:
        numpy.multiply(o[:bevel], bev, o[:bevel])
        numpy.multiply(o[ans:ans - bevel:-1], bev, o[ans:ans - bevel:-1])
        numpy.multiply(bc[:bevel], bev, bc[:bevel])
        numpy.multiply(bc[bns:bns - bevel:-1], bev, bc[bns:bns - bevel:-1])
    numpy.add(o[bos:boe], bc, o[bos:boe])
    if ta is not None or tb is not None:
        if tb is not None:
            tb += bos
        return (o, ta, tb)
    else:
        return o
        return


def argmax(a):
    i = numpy.argmax(a, axis=None)
    o = []
    for n in reversed(a.shape):
        o.append(i % n)
        i = i // n

    o.reverse()
    return tuple(o)


def _test_argmax():
    x = numpy.array([1, 2, 3, 4, 3])
    assert argmax(x) == (3, )
    x = numpy.array([[1, 2, 3, 4, 3], [0, 1, 0, 1, 0]])
    assert x[argmax(x)] == 4
    x = numpy.array([[1, 2, 3, 4, 3], [0, 1, 0, 5, 0]])
    assert x[argmax(x)] == 5
    x = numpy.array([[1, 2], [3, 4], [5, 6], [0, 1], [0, 5], [0, 7]])
    assert x[argmax(x)] == 7
    x = numpy.zeros((5, 4, 3, 3, 1, 2), numpy.double)
    x[(2, 1, 0, 1, 0, 1)] = 100.0
    assert argmax(x) == (2, 1, 0, 1, 0, 1)
    x[(0, 0, 0, 0, 0, 0)] = 200.0
    assert argmax(x) == (0, 0, 0, 0, 0, 0)
    x[(4, 3, 2, 2, 0, 1)] = 300.0
    assert argmax(x) == (4, 3, 2, 2, 0, 1)
    x[(4, 3, 2, 2, 0, 0)] = 400.0
    assert argmax(x) == (4, 3, 2, 2, 0, 0)
    x[(4, 3, 2, 0, 0, 0)] = 500.0
    assert argmax(x) == (4, 3, 2, 0, 0, 0)


def N_maximum(a):
    assert len(a.shape) == 1
    return a[numpy.argmax(a)].item()


def N_minimum(a):
    assert len(a.shape) == 1
    return a[numpy.argmin(a)].item()


def N_frac_rank--- This code section failed: ---

 L. 180         0  LOAD_CONST               0
                3  LOAD_FAST             1  'fr'
                6  DUP_TOP          
                7  ROT_THREE        
                8  COMPARE_OP            1  <=
               11  JUMP_IF_FALSE_OR_POP    23  'to 23'
               14  LOAD_CONST               1.0
               17  COMPARE_OP            1  <=
               20  JUMP_FORWARD          2  'to 25'
             23_0  COME_FROM            11  '11'
               23  ROT_TWO          
               24  POP_TOP          
             25_0  COME_FROM            20  '20'
               25  POP_JUMP_IF_TRUE     34  'to 34'
               28  LOAD_ASSERT              AssertionError
               31  RAISE_VARARGS_1       1  None

 L. 181        34  LOAD_GLOBAL           1  'numpy'
               37  LOAD_ATTR             2  'sort'
               40  LOAD_FAST             0  'a'
               43  CALL_FUNCTION_1       1  None
               46  STORE_FAST            2  'tmp'

 L. 182        49  LOAD_FAST             2  'tmp'
               52  LOAD_ATTR             3  'shape'
               55  LOAD_CONST               0
               58  BINARY_SUBSCR    
               59  STORE_FAST            3  'n'

 L. 183        62  LOAD_FAST             3  'n'
               65  LOAD_CONST               0
               68  COMPARE_OP            4  >
               71  POP_JUMP_IF_TRUE     83  'to 83'
               74  LOAD_ASSERT              AssertionError
               77  LOAD_CONST               'Zero-sized array: cannot compute rank.'
               80  RAISE_VARARGS_2       2  None

 L. 184        83  LOAD_FAST             2  'tmp'
               86  LOAD_GLOBAL           4  'int'
               89  LOAD_GLOBAL           5  'round'
               92  LOAD_FAST             3  'n'
               95  LOAD_CONST               1
               98  BINARY_SUBTRACT  
               99  LOAD_FAST             1  'fr'
              102  BINARY_MULTIPLY  
              103  CALL_FUNCTION_1       1  None
              106  CALL_FUNCTION_1       1  None
              109  BINARY_SUBSCR    
              110  LOAD_ATTR             6  'item'
              113  CALL_FUNCTION_0       0  None
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 116


def N_mean_ad(a):
    """Mean absolute deviation.   For a multi-dimensional array,
        it takes the MAD along the first axis, so
        N_mean_ad(x)[0]==N_mean_ad(x[:,0]).
        """
    ctr = numpy.median(a)
    diff = numpy.subtract(a, ctr)
    return numpy.sum(numpy.absolute(diff), axis=0) / (diff.shape[0] - 1)


def _test_N_mean_ad():
    x = numpy.zeros((2, 1), numpy.double)
    x[(0, 0)] = 1
    x[(1, 0)] = 0
    assert numpy.allclose(N_mean_ad(x), [1.0])
    x = numpy.zeros((5, 7), numpy.double)
    x[(0, 0)] = 1
    y = N_mean_ad(x)
    assert y.shape == (7, )
    assert numpy.allclose(y, [1.0 / 4.0, 0, 0, 0, 0, 0, 0])
    assert abs(N_mean_ad(x)[0] - N_mean_ad(x[:, 0])) < 0.001


def median_across(list_of_vec):
    """Returns an element-by-element median of a list of Numeric vectors."""
    assert len(list_of_vec[0].shape) == 1
    o = numpy.zeros(list_of_vec[0].shape, numpy.double)
    tmp = numpy.zeros((len(list_of_vec),), numpy.double)
    for t in list_of_vec:
        assert t.shape == o.shape

    for i in range(o.shape[0]):
        for j, v in enumerate(list_of_vec):
            tmp[j] = v[i]

        o[i] = numpy.median(tmp)

    return o


def N_median(a, axis=0):
    """Returns an element-by-element median of a list of Numeric vectors."""
    if len(a.shape) == 1:
        return numpy.median(a)
    assert len(a.shape) == 2
    if axis == 1:
        o = numpy.zeros((a.shape[0],), numpy.double)
        for i in range(o.shape[0]):
            o[i] = numpy.median(a[i])

    o = numpy.zeros((a.shape[1],), numpy.double)
    a = numpy.array(a)
    for i in range(o.shape[0]):
        o[i] = numpy.median(a[:, i])

    return o


def N_median_across(a):
    return N_median(a, axis=0)


variance = numpy.var
stdev = numpy.std
make_diag = numpy.diag

def set_diag(x, a):
    """Set the diagonal of a matrix x to be the vector a.
        If a is shorter than the diagonal of x, just set the beginning."""
    assert len(a.shape) == 1
    assert len(x.shape) == 2
    n = a.shape[0]
    assert x.shape[0] >= n
    assert x.shape[1] >= n
    for i in range(n):
        x[(i, i)] = a[i]


def _test_N_median_across():
    x = numpy.zeros((3, 2), numpy.double)
    x[(0, 0)] = 1
    x[(1, 0)] = 2
    x[(2, 0)] = 3
    y = N_median(x, axis=0)
    print 'median_across=', y
    assert numpy.allclose(y, [2.0, 0.0])


def limit(low, x, high):
    return numpy.clip(x, low, high)


def trimmed_mean_sigma_across(list_of_vec, weights, clip):
    import gpkavg, gpkavg
    assert len(list_of_vec[0].shape) == 1
    om = numpy.zeros(list_of_vec[0].shape, numpy.double)
    osig = numpy.zeros(list_of_vec[0].shape, numpy.double)
    tmp = numpy.zeros((len(list_of_vec),), numpy.double)
    for t in list_of_vec:
        assert t.shape == om.shape

    for i in range(om.shape[0]):
        for j, v in enumerate(list_of_vec):
            tmp[j] = v[i]

        om[i], osig[i] = gpkavg.avg(tmp, weights, clip)

    return (
     om, osig)


def trimmed_mean_across(list_of_vec, weights, clip):
    return trimmed_mean_sigma_across(list_of_vec, weights, clip)[0]


def trimmed_stdev_across(list_of_vec, weights, clip):
    return trimmed_mean_sigma_across(list_of_vec, weights, clip)[1]


def vec_variance(x):
    """Take a component-by-component variance of a list of vectors."""
    n = len(x)
    if n < 2:
        raise ValueError, 'Cannot take variance unless len(x)>1'
    x0 = x[0]
    sh = x0.shape
    s = numpy.zeros(sh, numpy.double)
    ss = numpy.zeros(sh, numpy.double)
    for xi in x:
        assert xi.shape == sh
        tmp = xi - x0
        numpy.add(s, tmp, s)
        numpy.add(ss, numpy.square(tmp), ss)

    return numpy.maximum(ss - numpy.square(s) / n, 0.0) / (n - 1)


def qform(vec, mat):
    """A quadratic form: vec*mat*vec,
        or vecs*mat*transpose(vecs)"""
    if len(vec.shape) != 1 or len(mat.shape) != 2:
        raise ValueError, (': ').join(["Can't handle input",
         'requires vector*matrix(vector)',
         'shapes are %s and %s' % (
          vec.shape, mat.shape)])
    if mat.shape != (vec.shape[0], vec.shape[0]):
        raise ValueError, (': ').join([
         'Matrix must be square and match the length of vector',
         'shapes are %s and %s' % (vec.shape, mat.shape)])
    return numpy.dot(vec, numpy.dot(mat, vec))


def KolmogorovSmirnov--- This code section failed: ---

 L. 344         0  LOAD_GLOBAL           0  'numpy'
                3  LOAD_ATTR             1  'asarray'
                6  LOAD_FAST             0  'd1'
                9  CALL_FUNCTION_1       1  None
               12  STORE_FAST            0  'd1'

 L. 345        15  LOAD_GLOBAL           0  'numpy'
               18  LOAD_ATTR             1  'asarray'
               21  LOAD_FAST             1  'd2'
               24  CALL_FUNCTION_1       1  None
               27  STORE_FAST            1  'd2'

 L. 346        30  LOAD_GLOBAL           2  'len'
               33  LOAD_FAST             0  'd1'
               36  LOAD_ATTR             3  'shape'
               39  CALL_FUNCTION_1       1  None
               42  LOAD_CONST               1
               45  COMPARE_OP            2  ==
               48  POP_JUMP_IF_TRUE     73  'to 73'
               51  LOAD_ASSERT              AssertionError
               54  LOAD_CONST               'd1.shape=%s'
               57  LOAD_GLOBAL           5  'str'
               60  LOAD_FAST             0  'd1'
               63  LOAD_ATTR             3  'shape'
               66  CALL_FUNCTION_1       1  None
               69  BINARY_MODULO    
               70  RAISE_VARARGS_2       2  None

 L. 347        73  LOAD_GLOBAL           2  'len'
               76  LOAD_FAST             1  'd2'
               79  LOAD_ATTR             3  'shape'
               82  CALL_FUNCTION_1       1  None
               85  LOAD_CONST               1
               88  COMPARE_OP            2  ==
               91  POP_JUMP_IF_TRUE    116  'to 116'
               94  LOAD_ASSERT              AssertionError
               97  LOAD_CONST               'd2.shape=%s'
              100  LOAD_GLOBAL           5  'str'
              103  LOAD_FAST             1  'd2'
              106  LOAD_ATTR             3  'shape'
              109  CALL_FUNCTION_1       1  None
              112  BINARY_MODULO    
              113  RAISE_VARARGS_2       2  None

 L. 348       116  LOAD_FAST             2  'w1'
              119  LOAD_CONST               None
              122  COMPARE_OP            8  is
              125  POP_JUMP_IF_FALSE   155  'to 155'

 L. 349       128  LOAD_GLOBAL           0  'numpy'
              131  LOAD_ATTR             7  'ones'
              134  LOAD_FAST             0  'd1'
              137  LOAD_ATTR             3  'shape'
              140  LOAD_GLOBAL           0  'numpy'
              143  LOAD_ATTR             8  'double'
              146  CALL_FUNCTION_2       2  None
              149  STORE_FAST            2  'w1'
              152  JUMP_FORWARD          0  'to 155'
            155_0  COME_FROM           152  '152'

 L. 350       155  LOAD_FAST             3  'w2'
              158  LOAD_CONST               None
              161  COMPARE_OP            8  is
              164  POP_JUMP_IF_FALSE   194  'to 194'

 L. 351       167  LOAD_GLOBAL           0  'numpy'
              170  LOAD_ATTR             7  'ones'
              173  LOAD_FAST             1  'd2'
              176  LOAD_ATTR             3  'shape'
              179  LOAD_GLOBAL           0  'numpy'
              182  LOAD_ATTR             8  'double'
              185  CALL_FUNCTION_2       2  None
              188  STORE_FAST            3  'w2'
              191  JUMP_FORWARD          0  'to 194'
            194_0  COME_FROM           191  '191'

 L. 352       194  LOAD_GLOBAL           0  'numpy'
              197  LOAD_ATTR             9  'sum'
              200  LOAD_FAST             2  'w1'
              203  CALL_FUNCTION_1       1  None
              206  STORE_FAST            4  'ws1'

 L. 353       209  LOAD_GLOBAL           0  'numpy'
              212  LOAD_ATTR             9  'sum'
              215  LOAD_FAST             3  'w2'
              218  CALL_FUNCTION_1       1  None
              221  STORE_FAST            5  'ws2'

 L. 354       224  LOAD_GLOBAL           0  'numpy'
              227  LOAD_ATTR            10  'argsort'
              230  LOAD_FAST             0  'd1'
              233  CALL_FUNCTION_1       1  None
              236  STORE_FAST            6  'i1'

 L. 355       239  LOAD_GLOBAL           0  'numpy'
              242  LOAD_ATTR            10  'argsort'
              245  LOAD_FAST             1  'd2'
              248  CALL_FUNCTION_1       1  None
              251  STORE_FAST            7  'i2'

 L. 356       254  LOAD_CONST               0.0
              257  STORE_FAST            8  'c1'

 L. 357       260  LOAD_CONST               0.0
              263  STORE_FAST            9  'c2'

 L. 358       266  LOAD_CONST               0
              269  STORE_FAST           10  'j1'

 L. 359       272  LOAD_CONST               0
              275  STORE_FAST           11  'j2'

 L. 360       278  LOAD_CONST               0.0
              281  STORE_FAST           12  'maxdiff'

 L. 361       284  SETUP_LOOP          430  'to 717'
              287  LOAD_GLOBAL          11  'True'
              290  POP_JUMP_IF_FALSE   716  'to 716'

 L. 362       293  LOAD_GLOBAL          12  'abs'
              296  LOAD_FAST             8  'c1'
              299  LOAD_FAST             9  'c2'
              302  BINARY_SUBTRACT  
              303  CALL_FUNCTION_1       1  None
              306  LOAD_FAST            12  'maxdiff'
              309  COMPARE_OP            4  >
              312  POP_JUMP_IF_FALSE   334  'to 334'

 L. 363       315  LOAD_GLOBAL          12  'abs'
              318  LOAD_FAST             8  'c1'
              321  LOAD_FAST             9  'c2'
              324  BINARY_SUBTRACT  
              325  CALL_FUNCTION_1       1  None
              328  STORE_FAST           12  'maxdiff'
              331  JUMP_FORWARD          0  'to 334'
            334_0  COME_FROM           331  '331'

 L. 364       334  LOAD_FAST            10  'j1'
              337  LOAD_FAST             6  'i1'
              340  LOAD_ATTR             3  'shape'
              343  LOAD_CONST               0
              346  BINARY_SUBSCR    
              347  LOAD_CONST               1
              350  BINARY_SUBTRACT  
              351  COMPARE_OP            0  <
              354  POP_JUMP_IF_FALSE   573  'to 573'
              357  LOAD_FAST            11  'j2'
              360  LOAD_FAST             7  'i2'
              363  LOAD_ATTR             3  'shape'
              366  LOAD_CONST               0
              369  BINARY_SUBSCR    
              370  LOAD_CONST               1
              373  BINARY_SUBTRACT  
              374  COMPARE_OP            0  <
            377_0  COME_FROM           354  '354'
              377  POP_JUMP_IF_FALSE   573  'to 573'

 L. 365       380  LOAD_FAST             0  'd1'
              383  LOAD_FAST             6  'i1'
              386  LOAD_FAST            10  'j1'
              389  BINARY_SUBSCR    
              390  BINARY_SUBSCR    
              391  LOAD_FAST             1  'd2'
              394  LOAD_FAST             7  'i2'
              397  LOAD_FAST            11  'j2'
              400  BINARY_SUBSCR    
              401  BINARY_SUBSCR    
              402  COMPARE_OP            0  <
              405  POP_JUMP_IF_FALSE   443  'to 443'

 L. 366       408  LOAD_FAST            10  'j1'
              411  LOAD_CONST               1
              414  INPLACE_ADD      
              415  STORE_FAST           10  'j1'

 L. 367       418  LOAD_FAST             8  'c1'
              421  LOAD_FAST             2  'w1'
              424  LOAD_FAST             6  'i1'
              427  LOAD_FAST            10  'j1'
              430  BINARY_SUBSCR    
              431  BINARY_SUBSCR    
              432  LOAD_FAST             4  'ws1'
              435  BINARY_DIVIDE    
              436  INPLACE_ADD      
              437  STORE_FAST            8  'c1'
              440  JUMP_ABSOLUTE       713  'to 713'

 L. 368       443  LOAD_FAST             0  'd1'
              446  LOAD_FAST             6  'i1'
              449  LOAD_FAST            10  'j1'
              452  BINARY_SUBSCR    
              453  BINARY_SUBSCR    
              454  LOAD_FAST             1  'd2'
              457  LOAD_FAST             7  'i2'
              460  LOAD_FAST            11  'j2'
              463  BINARY_SUBSCR    
              464  BINARY_SUBSCR    
              465  COMPARE_OP            4  >
              468  POP_JUMP_IF_FALSE   506  'to 506'

 L. 369       471  LOAD_FAST            11  'j2'
              474  LOAD_CONST               1
              477  INPLACE_ADD      
              478  STORE_FAST           11  'j2'

 L. 370       481  LOAD_FAST             9  'c2'
              484  LOAD_FAST             3  'w2'
              487  LOAD_FAST             7  'i2'
              490  LOAD_FAST            11  'j2'
              493  BINARY_SUBSCR    
              494  BINARY_SUBSCR    
              495  LOAD_FAST             5  'ws2'
              498  BINARY_DIVIDE    
              499  INPLACE_ADD      
              500  STORE_FAST            9  'c2'
              503  JUMP_ABSOLUTE       713  'to 713'

 L. 372       506  LOAD_FAST            10  'j1'
              509  LOAD_CONST               1
              512  INPLACE_ADD      
              513  STORE_FAST           10  'j1'

 L. 373       516  LOAD_FAST             8  'c1'
              519  LOAD_FAST             2  'w1'
              522  LOAD_FAST             6  'i1'
              525  LOAD_FAST            10  'j1'
              528  BINARY_SUBSCR    
              529  BINARY_SUBSCR    
              530  LOAD_FAST             4  'ws1'
              533  BINARY_DIVIDE    
              534  INPLACE_ADD      
              535  STORE_FAST            8  'c1'

 L. 374       538  LOAD_FAST            11  'j2'
              541  LOAD_CONST               1
              544  INPLACE_ADD      
              545  STORE_FAST           11  'j2'

 L. 375       548  LOAD_FAST             9  'c2'
              551  LOAD_FAST             3  'w2'
              554  LOAD_FAST             7  'i2'
              557  LOAD_FAST            11  'j2'
              560  BINARY_SUBSCR    
              561  BINARY_SUBSCR    
              562  LOAD_FAST             5  'ws2'
              565  BINARY_DIVIDE    
              566  INPLACE_ADD      
              567  STORE_FAST            9  'c2'
              570  JUMP_BACK           287  'to 287'

 L. 376       573  LOAD_FAST            10  'j1'
              576  LOAD_FAST             6  'i1'
              579  LOAD_ATTR             3  'shape'
              582  LOAD_CONST               0
              585  BINARY_SUBSCR    
              586  LOAD_CONST               1
              589  BINARY_SUBTRACT  
              590  COMPARE_OP            2  ==
              593  POP_JUMP_IF_FALSE   623  'to 623'
              596  LOAD_FAST            11  'j2'
              599  LOAD_FAST             7  'i2'
              602  LOAD_ATTR             3  'shape'
              605  LOAD_CONST               0
              608  BINARY_SUBSCR    
              609  LOAD_CONST               1
              612  BINARY_SUBTRACT  
              613  COMPARE_OP            2  ==
            616_0  COME_FROM           593  '593'
              616  POP_JUMP_IF_FALSE   623  'to 623'

 L. 377       619  BREAK_LOOP       
              620  JUMP_BACK           287  'to 287'

 L. 378       623  LOAD_FAST            10  'j1'
              626  LOAD_FAST             6  'i1'
              629  LOAD_ATTR             3  'shape'
              632  LOAD_CONST               0
              635  BINARY_SUBSCR    
              636  LOAD_CONST               1
              639  BINARY_SUBTRACT  
              640  COMPARE_OP            0  <
              643  POP_JUMP_IF_FALSE   681  'to 681'

 L. 379       646  LOAD_FAST            10  'j1'
              649  LOAD_CONST               1
              652  INPLACE_ADD      
              653  STORE_FAST           10  'j1'

 L. 380       656  LOAD_FAST             8  'c1'
              659  LOAD_FAST             2  'w1'
              662  LOAD_FAST             6  'i1'
              665  LOAD_FAST            10  'j1'
              668  BINARY_SUBSCR    
              669  BINARY_SUBSCR    
              670  LOAD_FAST             4  'ws1'
              673  BINARY_DIVIDE    
              674  INPLACE_ADD      
              675  STORE_FAST            8  'c1'
              678  JUMP_BACK           287  'to 287'

 L. 382       681  LOAD_FAST            11  'j2'
              684  LOAD_CONST               1
              687  INPLACE_ADD      
              688  STORE_FAST           11  'j2'

 L. 383       691  LOAD_FAST             9  'c2'
              694  LOAD_FAST             3  'w2'
              697  LOAD_FAST             7  'i2'
              700  LOAD_FAST            11  'j2'
              703  BINARY_SUBSCR    
              704  BINARY_SUBSCR    
              705  LOAD_FAST             5  'ws2'
              708  BINARY_DIVIDE    
              709  INPLACE_ADD      
              710  STORE_FAST            9  'c2'
              713  JUMP_BACK           287  'to 287'
              716  POP_BLOCK        
            717_0  COME_FROM           284  '284'

 L. 384       717  LOAD_FAST            12  'maxdiff'
              720  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 717


def _testKS():
    assert KolmogorovSmirnov([1, 2, 3.01, 3, 4, 5], [1, 2, 3.01, 3, 4, 5]) < 0.001
    assert abs(KolmogorovSmirnov([1, 2, 3.01, 3, 4, 5], [1, 2, 3, 4, 5, 6]) - 0.16667) < 0.001
    print KolmogorovSmirnov([1, 2, 3.01, 3, 4, 5], [1, 2, 3, 4, 5])


def interpN(a, t):
    """Interpolate array a to floating point indices, t,
        via nearest-neighbor interpolation.
        Returns a Numeric array.
        """
    ii = numpy.around(t)
    n = a.shape[0]
    if not numpy.alltrue((ii >= 0) * (ii <= n - 1)):
        raise IndexError, 'Index out of range.'
    iii = ii.astype(numpy.int)
    return numpy.take(a, iii, axis=0)


def interp(a, t):
    """Interpolate to a specified time axis.
        This does a linear interpolation.
        A is a Numpy array, and t is an array of times.
        @return: interpolated values
        @rtype: numpy array.
        """
    n = a.shape[0]
    nt = t.shape[0]
    las = len(a.shape)
    if las == 1:
        a = numpy.transpose([a])
    m = a.shape[1]
    ii = numpy.around(t)
    if not ii.shape == t.shape:
        raise AssertionError
        idxmin = numpy.alltrue((ii >= 0) * (ii <= n - 1)) or numpy.argmin(t)
        idxmax = numpy.argmax(t)
        raise IndexError, 'Index out of range: min=%g[index=%d,int=%d] max=%g[index=%d,int=%d] vs. %d' % (t[idxmin], idxmin, ii[idxmin], t[idxmax], idxmax, ii[idxmax], n)
    nearestT = ii.astype(numpy.int)
    assert nearestT.shape == t.shape
    nearestA = numpy.take(a, nearestT, axis=0)
    assert nearestA.shape == (nt, m)
    deltaT = t - nearestT
    assert deltaT.shape == nearestT.shape
    isupport = numpy.where((deltaT >= 0) * (nearestT < n - 1) + (nearestT <= 0), 1, -1) + nearestT
    assert isupport.shape == (nearestA.shape[0],)
    assert isupport.shape == nearestT.shape
    assert isupport.shape == deltaT.shape
    support = numpy.take(a, isupport, axis=0)
    assert support.shape == (nt, m)
    if len(a.shape) > 1:
        assert nearestA.shape == (nt, m)
        deltaA = (deltaT / (isupport - nearestT))[:, numpy.newaxis] * (support - nearestA)
        assert deltaA.shape[1] == a.shape[1]
    else:
        deltaA = deltaT / (isupport - nearestT) * (support - nearestA)
    assert deltaA.shape == nearestA.shape
    rv = nearestA + deltaA
    if las == 1:
        return rv[:, 0]
    return rv


def _test_interp1():
    a = numpy.array([[1.0], [2.0]])
    t = numpy.array([0.5])
    q = interp(a, t)
    assert q.shape == (1, 1)
    assert numpy.sum(numpy.absolute(interp(a, t) - [1.5])) < 0.001


def split_into_clumps(x, threshold, minsize=1):
    """This reports when the signal is above the threshold.
        @param x: a signal
        @type x: L{numpy.ndarray}, one-dimensional.
        @param threshold: a threshold.
        @type threshold: float
        @returns: [(start, stop), ...] for each region ("clump") where C{x>threshold}.
        """
    assert len(x.shape) == 1
    gt = numpy.greater(x, threshold)
    chg = gt[1:] - gt[:-1]
    nz = numpy.nonzero(chg)[0]
    rv = []
    if gt[0]:
        last = 0
    else:
        last = None
    for i in nz:
        if last is None:
            last = i + 1
        else:
            if minsize > 0:
                rv.append((last, i + 1))
            last = None

    if last is not None and gt.shape[0] >= last + minsize:
        rv.append((last, gt.shape[0]))
    return rv


def _test_split_into_clumps():
    tmp = split_into_clumps(numpy.array([0, 0, 0, 1, 0, 0]), 0.5)
    assert tmp == [(3, 4)]
    tmp = split_into_clumps(numpy.array([1, 0, 0]), 0.5)
    assert tmp == [(0, 1)]
    tmp = split_into_clumps(numpy.array([0, 0, 0, 1]), 0.5)
    assert tmp == [(3, 4)]
    tmp = split_into_clumps(numpy.array([1]), 0.5)
    assert tmp == [(0, 1)]
    tmp = split_into_clumps(numpy.array([0]), 0.5)
    assert tmp == []
    tmp = split_into_clumps(numpy.array([1]), 0.5, minsize=2)
    assert tmp == []
    tmp = split_into_clumps(numpy.array([0, 0, 0, 1, 1, 0]), 0.5, minsize=2)
    assert tmp == [(3, 5)]


BLOCK = 8192

def block_stdev(x):
    """This is just a alternative implementation of
        the standard deviation of each channel, but it is designed
        in a block-wise fashion so the total memory usage is
        not large.
        """
    m = (x.shape[0] + BLOCK - 1) // BLOCK
    avg = numpy.zeros((m, x.shape[1]))
    sum2 = numpy.zeros((x.shape[1],))
    nn = numpy.zeros((m,))
    i = 0
    j = 0
    while i < x.shape[0]:
        n = min(BLOCK, x.shape[0] - i)
        tmp = numpy.sum(x[i:i + BLOCK], axis=0) / n
        avg[j, :] = tmp
        numpy.add(sum2, numpy.sum(numpy.square(x[i:i + BLOCK] - tmp), axis=0), sum2)
        nn[j] = n
        i += BLOCK
        j += 1

    assert j == m
    avgavg = numpy.sum(nn[:, numpy.newaxis] * avg, axis=0) / float(x.shape[0])
    for i in range(m):
        numpy.add(sum2, nn[i] * numpy.square(avg[i, :] - avgavg), sum2)

    return numpy.sqrt(sum2 / float(x.shape[0] - 1))


def convolve--- This code section failed: ---

 L. 565         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             1  'kernel'
                6  LOAD_ATTR             1  'shape'
                9  CALL_FUNCTION_1       1  None
               12  LOAD_CONST               1
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     27  'to 27'
               21  LOAD_ASSERT              AssertionError
               24  RAISE_VARARGS_1       1  None

 L. 566        27  LOAD_GLOBAL           0  'len'
               30  LOAD_FAST             0  'x'
               33  LOAD_ATTR             1  'shape'
               36  CALL_FUNCTION_1       1  None
               39  LOAD_CONST               1
               42  COMPARE_OP            2  ==
               45  POP_JUMP_IF_TRUE     57  'to 57'
               48  LOAD_ASSERT              AssertionError
               51  LOAD_CONST               'Have not tried multidimensional data yet.'
               54  RAISE_VARARGS_2       2  None

 L. 567        57  LOAD_FAST             0  'x'
               60  LOAD_ATTR             1  'shape'
               63  LOAD_CONST               0
               66  BINARY_SUBSCR    
               67  LOAD_FAST             1  'kernel'
               70  LOAD_ATTR             1  'shape'
               73  LOAD_CONST               0
               76  BINARY_SUBSCR    
               77  COMPARE_OP            4  >
               80  POP_JUMP_IF_FALSE   102  'to 102'

 L. 568        83  LOAD_GLOBAL           3  'numpy'
               86  LOAD_ATTR             4  'convolve'
               89  LOAD_FAST             0  'x'
               92  LOAD_FAST             1  'kernel'
               95  LOAD_CONST               1
               98  CALL_FUNCTION_3       3  None
              101  RETURN_END_IF    
            102_0  COME_FROM            80  '80'

 L. 569       102  LOAD_FAST             1  'kernel'
              105  LOAD_ATTR             1  'shape'
              108  LOAD_CONST               0
              111  BINARY_SUBSCR    
              112  LOAD_FAST             0  'x'
              115  LOAD_ATTR             1  'shape'
              118  LOAD_CONST               0
              121  BINARY_SUBSCR    
              122  BINARY_SUBTRACT  
              123  LOAD_CONST               1
              126  BINARY_ADD       
              127  STORE_FAST            2  'n'

 L. 570       130  LOAD_GLOBAL           3  'numpy'
              133  LOAD_ATTR             5  'zeros'
              136  LOAD_FAST             2  'n'
              139  BUILD_TUPLE_1         1 
              142  CALL_FUNCTION_1       1  None
              145  STORE_FAST            3  'z'

 L. 571       148  LOAD_GLOBAL           3  'numpy'
              151  LOAD_ATTR             6  'concatenate'
              154  LOAD_FAST             3  'z'
              157  LOAD_FAST             0  'x'
              160  LOAD_FAST             3  'z'
              163  BUILD_TUPLE_3         3 
              166  LOAD_CONST               'axis'
              169  LOAD_CONST               0
              172  CALL_FUNCTION_257   257  None
              175  STORE_FAST            4  'xx'

 L. 572       178  LOAD_GLOBAL           3  'numpy'
              181  LOAD_ATTR             4  'convolve'
              184  LOAD_FAST             4  'xx'
              187  LOAD_FAST             1  'kernel'
              190  LOAD_CONST               1
              193  CALL_FUNCTION_3       3  None
              196  LOAD_FAST             2  'n'
              199  LOAD_FAST             2  'n'
              202  LOAD_FAST             0  'x'
              205  LOAD_ATTR             1  'shape'
              208  LOAD_CONST               0
              211  BINARY_SUBSCR    
              212  BINARY_ADD       
              213  SLICE+3          
              214  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 214


class EdgesTooWide(Exception):

    def __init__(self, *s):
        Exception.__init__(self, *s)


def edge_window(n, eleft, eright, typeleft='linear', typeright='linear', norm=None):
    """Creates a window which is basically flat, but tapers off on the left and
        right edges.  The widths of the tapers can be controlled, as can the shapes.
        @param n: the width of the window
        @type n: C{int}
        @param eleft: the width of the left taper (i.e. at zero index, in samples).
        @type eleft: C{int}
        @param eright: the width of the right taper (i.e. at index near C{n}, in samples).
        @type eright: C{int}
        @param typeleft: what kind of taper on the left? (Defaults to C{"linear"}).
        @type typeleft: C{'linear'} or C{'cos'}
        @param typeright: what kind of taper on the right?  (Defaults to C{"linear"}).
        @type typeright: C{'linear'} or C{'cos'}
        @param norm: How to normalize?  The default is L{None}, which means no normalization.
                Providing a number C{x} will normalize the window so that the average of the
                C{window**x}==1.
        @type norm: L{None} or C{float != 0}.
        """
    if not int(n) >= 0:
        raise AssertionError
        raise eleft <= n and eright <= n or EdgesTooWide, 'n=%d, eleft=%d eright=%d' % (n, eleft, eright)
    o = numpy.ones((n,))
    if eleft > 0:
        frac = (numpy.arange(eleft) + 0.5) / eleft
        if typeleft == 'cos':
            frac = (1.0 - numpy.cos(frac * math.pi)) / 2.0
        o[:eleft] = frac
        del frac
    if eright > 0:
        frac = (eright - numpy.arange(eright) - 0.5) / eright
        if typeright == 'cos':
            frac = (1.0 - numpy.cos(frac * math.pi)) / 2.0
        numpy.multiply(o[n - eright:], frac, o[n - eright:])
    if norm is not None:
        numpy.divide(o, numpy.average(o ** norm) ** (1.0 / norm), o)
    return o


def edge_window_t(t, eleft, eright, typeleft='linear', typeright='linear', norm=None):
    """Computes a window which is basically flat, but tapers off on the left and
        right edges.  The widths of the tapers can be controlled, as can the shapes.
        @param t: an array of time values.  They are required to be monotonically increasing,
                and assumed to be linearly spaced.
        @type t: C{numpy.ndarray}
        @param eleft: the width of the left taper (i.e. at zero index, in time units).
        @type eleft: C{float}
        @param eright: the width of the right taper (i.e. at index near C{n}, in time units).
        @type eright: C{float}
        @param typeleft: what kind of taper on the left? (Defaults to C{"linear"}).
        @type typeleft: C{'linear'} or C{'cos'}
        @param typeright: what kind of taper on the right?  (Defaults to C{"linear"}).
        @type typeright: C{'linear'} or C{'cos'}
        @param norm: How to normalize?  The default is L{None}, which means no normalization.
                Providing a number C{x} will normalize the window so that the average of the
                C{window**x}==1.
        @type norm: L{None} or C{float != 0}.
        """
    if not len(t) > 1:
        raise ValueError, 'Time axis too short: len(t)=%d' % len(t)
    t0 = float(t[0])
    te = float(t[(-1)])
    if not te > t0:
        raise AssertionError, 't=%s' % str(t)
        w = te - t0
        assert w > 0.0
        return eleft <= w and eright <= w or (
         EdgesTooWide, 'eleft=%s eright=%s w=%s' % (eleft, eright, w))
    else:
        o = numpy.ones(t.shape)
        if eleft > 0:
            nedge = int(math.ceil(eleft / w * t.shape[0]))
            wedge = (nedge + 1) * eleft / float(nedge)
            tx = t0 - 0.5 * wedge / (nedge + 1)
            if typeleft == 'cos':
                f = (1.0 - numpy.cos(math.pi / wedge * (t[:nedge] - tx))) / 2.0
            else:
                f = (t[:nedge] - tx) / wedge
            o[:nedge] = f
            del f
        if eright > 0:
            nedge = int(math.ceil(eright / w * t.shape[0]))
            wedge = (nedge + 1) * eright / float(nedge)
            tx = te + 0.5 * wedge / (nedge + 1)
            y = o.shape[0] - nedge
            if typeright == 'cos':
                f = (1.0 - numpy.cos(math.pi / wedge * (tx - t[y:]))) / 2.0
            else:
                f = (tx - t[y:]) / wedge
            numpy.multiply(o[y:], f, o[y:])
        if norm is not None:
            numpy.divide(o, numpy.average(o ** norm) ** (1.0 / norm), o)
        return o


def _test_ew():
    t = 1.0 + 0.1 * numpy.arange(100)
    for i in range(0, 60, 4):
        e = 0.0 + 0.1 * i
        w = edge_window_t(t, e, 1.432 * e, typeright='cos')
        pylab.plot(t, w)

    pylab.show()


if __name__ == '__main__':
    _test_split_into_clumps()
    _test_argmax()
    _test_interp1()
    _test_Poisson()
    _test_N_mean_ad()
    _test_N_median_across()
    _test_split_into_clumps()
    import pylab
    _test_ew()