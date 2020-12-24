# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/g_localfit.py
# Compiled at: 2011-03-31 16:40:20
"""Fit a linear transform to a bunch of tt
input/output vectors.

@note: If you compute Pearson's R^2 via 1-localfit()/err_before_fit(), you get the "unadjusted" R^2 value.
        There is also an "adjusted" R^2 value, which is
        Ra^2 = 1-(1-R^2)*(n-1)/(n-p-1) where n is the number of data and p is the number of adjustable
        parameters of the linear regression.
@note: When you are computing Pearson's r^2 by way of localfit()/err_before_fit() the two function calls
        I{MUST} have the same data and flags.  Specifically, C{constant} must be equal in both calls.
"""
import numpy, warnings
from gmisclib import gpk_lsq
from gmisclib import gpk_rlsq
_Float = numpy.dtype('float')

def err_before_fit(data, minsv=None, minsvr=None, constant=True):
    """How much variation did the data have before the fit?
        This is used to compare with the error after the fit, to
        allow a F-test or ANOVA.    Strictly speaking, we compute
        the mean-squared error about a constant.
        @return: Returns the per-coordinate sum-squared-error
                of the output coordinates.
        @rtype: C{numpy.ndarray}
        @param data: See L{pack}.
        @type data: See L{pack}.
        """
    tmp = []
    for ioc in data:
        if len(ioc) == 2:
            ic, oc = ioc
            tmp.append((numpy.zeros((0, ), _Float), oc))
        elif len(ioc) == 3:
            ic, oc, w = ioc
            w = float(w)
            assert w >= 0.0
            tmp.append((numpy.zeros((0, ), _Float), oc, w))

    A, B, errs, sv, rank = localfit(tmp, minsv=minsv, minsvr=minsvr, constant=constant)
    return errs


def pack(data, constant=True):
    """Prepare the data array and (optionally) weight the data.
        @param data: [(input_coordinates, output_coordinates), ...]
                or [(input_coordinates, output_coordinates, weight), ...].
                A list of (in,out) tuples corresponding to the
                independent and dependent parameters of the linear transform.
                Both C{in} and C{out} are one-dimensional
                numpy vectors.   They don't need to have
                the same length, though (obviously) all instances of "in"
                need to have the same length and all instances of "out"
                also need to match one another.
                If C{weight} is given, it must be a scalar.
        @type data: [(L{numpy.ndarray}, L{numpy.ndarray}), ...] or
                [(L{numpy.ndarray}, L{numpy.ndarray}, float), ...]
        """
    nd = len(data)
    if not nd > 0:
        raise ValueError, 'No data: cannot deduce dimensionality.'
    ic, oc = data[0][:2]
    m = len(oc)
    if not m > 0:
        raise ValueError, 'Output coordinates have zero dimension.'
    n = len(ic)
    use_c = bool(constant)
    if not n + use_c > 0:
        warnings.warn('g_localfit: This is a zero-parameter model.')
    i = numpy.zeros((nd, n + use_c), _Float)
    o = numpy.zeros((nd, m), _Float)
    try:
        if use_c and len(data[0]) == 2:
            for j, iow in enumerate(data):
                ic, oc = iow
                o[j, :] = oc
                i[(j, 0)] = 1.0
                i[j, 1:] = ic

        elif use_c and len(data[0]) == 3:
            for j, iow in enumerate(data):
                ic, oc, w = iow
                i[(j, 0)] = 1.0
                i[j, 1:] = ic
                w = float(w)
                numpy.multiply(oc, w, o[j, 1:])

        elif len(data[0]) == 2:
            for j, iow in enumerate(data):
                ic, oc = iow
                o[j, :] = oc
                i[j, :] = ic

        elif len(data[0]) == 3:
            for j, iow in enumerate(data):
                ic, oc, w = iow
                i[j, :] = ic
                w = float(w)
                numpy.multiply(oc, w, o[j, :])

    except ValueError as x:
        if len(iow) != len(data[0]):
            raise ValueError, 'Data must either be uniformly weighted or not: see data[%d]' % j
        if len(oc) != o.shape[1]:
            raise ValueError, 'Output data length must match: got %d on data[%d], expecting %d' % (len(oc), j, o.shape[1])
        if len(ic) != i.shape[1] - use_c:
            raise ValueError, 'Input data length must match: got %d on data[%d], expecting %d' % (len(oc), j, i.shape[1] - use_c)
    except TypeError as x:
        if 'float' in str(x):
            raise TypeError, 'Weight must be convertible to float in data[%d]: %s' % (j, x)

    return (
     i, o, m, n)


def localfit--- This code section failed: ---

 L. 146         0  LOAD_GLOBAL           0  'pack'
                3  LOAD_FAST             0  'data'
                6  LOAD_CONST               'constant'
                9  LOAD_FAST             3  'constant'
               12  CALL_FUNCTION_257   257  None
               15  UNPACK_SEQUENCE_4     4 
               18  STORE_FAST            4  'ii'
               21  STORE_FAST            5  'oo'
               24  STORE_FAST            6  'm'
               27  STORE_FAST            7  'n'

 L. 147        30  DELETE_FAST           0  'data'

 L. 148        33  LOAD_GLOBAL           1  'gpk_lsq'
               36  LOAD_ATTR             2  'linear_least_squares'
               39  LOAD_FAST             4  'ii'
               42  LOAD_FAST             5  'oo'
               45  LOAD_CONST               'minsv'
               48  LOAD_FAST             1  'minsv'
               51  LOAD_CONST               'minsvr'
               54  LOAD_FAST             2  'minsvr'
               57  LOAD_CONST               'copy'
               60  LOAD_GLOBAL           3  'False'
               63  CALL_FUNCTION_770   770  None
               66  STORE_FAST            8  'soln'

 L. 149        69  LOAD_FAST             8  'soln'
               72  LOAD_ATTR             4  'q'
               75  LOAD_FAST             6  'm'
               78  COMPARE_OP            2  ==
               81  POP_JUMP_IF_TRUE     90  'to 90'
               84  LOAD_ASSERT              AssertionError
               87  RAISE_VARARGS_1       1  None

 L. 150        90  DELETE_FAST           4  'ii'

 L. 151        93  DELETE_FAST           5  'oo'

 L. 152        96  LOAD_GLOBAL           6  'numpy'
               99  LOAD_ATTR             7  'sum'
              102  LOAD_GLOBAL           6  'numpy'
              105  LOAD_ATTR             8  'square'
              108  LOAD_FAST             8  'soln'
              111  LOAD_ATTR             9  'residual'
              114  CALL_FUNCTION_0       0  None
              117  CALL_FUNCTION_1       1  None
              120  LOAD_CONST               'axis'
              123  LOAD_CONST               0
              126  CALL_FUNCTION_257   257  None
              129  STORE_FAST            9  'errs'

 L. 153       132  LOAD_FAST             8  'soln'
              135  LOAD_ATTR            10  'sv'
              138  CALL_FUNCTION_0       0  None
              141  STORE_FAST           10  'sv'

 L. 154       144  LOAD_FAST             8  'soln'
              147  LOAD_ATTR            11  'x'
              150  LOAD_CONST               'copy'
              153  LOAD_GLOBAL           3  'False'
              156  CALL_FUNCTION_256   256  None
              159  STORE_FAST           11  'x'

 L. 155       162  LOAD_FAST             8  'soln'
              165  LOAD_ATTR            12  'rank'
              168  CALL_FUNCTION_0       0  None
              171  STORE_FAST           12  'rank'

 L. 156       174  LOAD_FAST            10  'sv'
              177  LOAD_ATTR            13  'shape'
              180  LOAD_CONST               0
              183  BINARY_SUBSCR    
              184  LOAD_FAST            12  'rank'
              187  COMPARE_OP            5  >=
              190  POP_JUMP_IF_FALSE   216  'to 216'
              193  LOAD_FAST            10  'sv'
              196  LOAD_ATTR            13  'shape'
              199  LOAD_CONST               0
              202  BINARY_SUBSCR    
              203  LOAD_FAST             7  'n'
              206  LOAD_CONST               1
              209  BINARY_ADD       
              210  COMPARE_OP            1  <=
            213_0  COME_FROM           190  '190'
              213  POP_JUMP_IF_TRUE    250  'to 250'
              216  LOAD_ASSERT              AssertionError
              219  LOAD_CONST               'sv.shape=%s rank=%d m=%d n=%d'
              222  LOAD_GLOBAL          14  'str'
              225  LOAD_FAST            10  'sv'
              228  LOAD_ATTR            13  'shape'
              231  CALL_FUNCTION_1       1  None
              234  LOAD_FAST            12  'rank'
              237  LOAD_FAST             6  'm'
              240  LOAD_FAST             7  'n'
              243  BUILD_TUPLE_4         4 
              246  BINARY_MODULO    
              247  RAISE_VARARGS_2       2  None

 L. 157       250  LOAD_FAST            12  'rank'
              253  LOAD_CONST               1
              256  LOAD_FAST             7  'n'
              259  BINARY_ADD       
              260  COMPARE_OP            1  <=
              263  POP_JUMP_IF_TRUE    272  'to 272'
              266  LOAD_ASSERT              AssertionError
              269  RAISE_VARARGS_1       1  None

 L. 158       272  LOAD_GLOBAL          15  'len'
              275  LOAD_FAST             9  'errs'
              278  CALL_FUNCTION_1       1  None
              281  LOAD_FAST             6  'm'
              284  COMPARE_OP            2  ==
              287  POP_JUMP_IF_TRUE    296  'to 296'
              290  LOAD_ASSERT              AssertionError
              293  RAISE_VARARGS_1       1  None

 L. 159       296  LOAD_FAST            11  'x'
              299  LOAD_ATTR            16  'ndim'
              302  LOAD_CONST               2
              305  COMPARE_OP            2  ==
              308  POP_JUMP_IF_TRUE    317  'to 317'
              311  LOAD_ASSERT              AssertionError
              314  RAISE_VARARGS_1       1  None

 L. 160       317  LOAD_FAST             3  'constant'
              320  POP_JUMP_IF_FALSE   408  'to 408'

 L. 161       323  LOAD_FAST            11  'x'
              326  LOAD_CONST               1
              329  LOAD_CONST               None
              332  BUILD_SLICE_2         2 
              335  LOAD_CONST               None
              338  LOAD_CONST               None
              341  BUILD_SLICE_2         2 
              344  BUILD_TUPLE_2         2 
              347  BINARY_SUBSCR    
              348  LOAD_ATTR            17  'transpose'
              351  CALL_FUNCTION_0       0  None
              354  LOAD_FAST            11  'x'
              357  LOAD_CONST               0
              360  LOAD_CONST               None
              363  LOAD_CONST               None
              366  BUILD_SLICE_2         2 
              369  BUILD_TUPLE_2         2 
              372  BINARY_SUBSCR    

 L. 162       373  LOAD_FAST             9  'errs'
              376  LOAD_GLOBAL           6  'numpy'
              379  LOAD_ATTR            18  'sort'
              382  LOAD_FAST            10  'sv'
              385  CALL_FUNCTION_1       1  None
              388  LOAD_CONST               None
              391  LOAD_CONST               None
              394  LOAD_CONST               -1
              397  BUILD_SLICE_3         3 
              400  BINARY_SUBSCR    
              401  LOAD_FAST            12  'rank'
              404  BUILD_TUPLE_5         5 
              407  RETURN_END_IF    
            408_0  COME_FROM           320  '320'

 L. 164       408  LOAD_FAST            11  'x'
              411  LOAD_ATTR            17  'transpose'
              414  CALL_FUNCTION_0       0  None
              417  LOAD_CONST               None

 L. 165       420  LOAD_FAST             9  'errs'
              423  LOAD_GLOBAL           6  'numpy'
              426  LOAD_ATTR            18  'sort'
              429  LOAD_FAST            10  'sv'
              432  CALL_FUNCTION_1       1  None
              435  LOAD_CONST               None
              438  LOAD_CONST               None
              441  LOAD_CONST               -1
              444  BUILD_SLICE_3         3 
              447  BINARY_SUBSCR    
              448  LOAD_FAST            12  'rank'
              451  BUILD_TUPLE_5         5 
              454  RETURN_VALUE     

Parse error at or near `BUILD_TUPLE_5' instruction at offset 451


def reg_localfit(data, regstr=0.0, regtgt=None, rscale=None, constant=True):
    """Does a linear fit to data via a singular value decomposition
        algorithm.
        It returns the matrix A and vector B such that
        C{A*input_coordinates+B} is the best fit to C{output_coordinates}.
        @param constant: Do you want a constant built into the linear equations?
        @type constant: Boolean
        @return: (A, B, errs, sv, rank) where
                - A is a 2-D C{numpy.ndarray} matrix.
                - B is a 1-D C{numpy.ndarray} vector (if constant, else C{None}).
                - errs is a C{numpy.ndarray} vector, one value for each output coordinate.
                        It gives the sum of squared residuals.
                - sv are the singular values, sorted into decreasing order.
        @param data: list of tuples.   See L{pack}.
        @type data: See L{pack}.
        """
    ii, oo, m, n = pack(data, constant=constant)
    del data
    soln = gpk_lsq.reg_linear_least_squares(ii, oo, regstr=regstr, regtgt=regtgt, rscale=rscale, copy=False)
    del ii
    del oo
    errs = numpy.sum(numpy.square(soln.residual()), axis=0)
    sv = soln.sv_unreg()
    x = soln.x(copy=False)
    rank = soln.eff_rank()
    assert len(errs) == m
    assert x.ndim == 2
    if constant:
        return (x[1:, :].transpose(), x[0, :],
         errs, numpy.sort(sv)[::-1], rank)
    else:
        return (
         x.transpose(), None,
         errs, numpy.sort(sv)[::-1], rank)


def robust_localfit(data, minsv=None, minsvr=None, constant=True):
    """Data is [ (input_coordinates, output_coordinates), ... ]
        Minsv sets the minimum useable singular value;
        minsvr sets the minimum useable s.v. in terms of the largest s.v..
        It returns the matrix A and vector B such that the best fit
        is A*input_coordinates+B in a tuple
        (A, B, errs, rank).
        errs is a vector, one value for each output coordinate.
        Rank is the minimum rank of the various fits.

        Warning! Not tested.
        """
    ii, oo, m, n = pack(data, constant=constant)
    del data
    errs = []
    rank = None
    const = numpy.zeros((m,), _Float)
    coef = numpy.zeros((n, m), _Float)
    for j in range(m):
        assert oo.shape[1] == m
        soln = gpk_rlsq.robust_linear_fit(ii, oo[:, j], 1, minsv=minsv, minsvr=minsvr, copy=False)
        errs.append(numpy.sum(numpy.square(soln.residual())))
        if rank is None or rank > soln.rank():
            rank = soln.rank()
        const[j] = soln.x()[0]
        coef[:, j] = soln.x()[1:]

    del ii
    del oo
    assert rank <= 1 + n
    assert len(errs) == m
    return (coef.transpose(), const, errs, rank)


def fit_giving_sigmas(data, minsv=None, minsvr=None, constant=True):
    """Does a linear fit to data via a singular value decomposition
        algorithm.
        It returns the matrix A and vector B such that
        C{A*input_coordinates+B} is the best fit to C{output_coordinates}.
        @param minsv: sets the minimum useable singular value;
        @param minsvr: sets the minimum useable s.v. in terms of the largest s.v.
        @type minsv: float or None
        @type minsvr: float or None
        @param constant: Do you want a constant built into the linear equations?
        @type constant: Boolean
        @return: (A, B, sigmaA, sigmaB) where
                - A is a 2-D C{numpy.ndarray} matrix.
                - B is a 1-D C{numpy.ndarray} vector (if constant, else C{None}).
                        )
        @param data: [(input_coordinates, output_coordinates), ...].
                A list of (in,out) tuples corresponding to the
                independent and dependent parameters of the linear transform.
                Both C{in} and C{out} are one-dimensional
                L{numpy vectors<numpy.ndarray>}.   They don't need to have
                the same length, though (obviously) all instances of "in"
                need to have the same length and all instances of "out"
                also need to match one another.
        @type data: [(L{numpy.ndarray}, L{numpy.ndarray}), ...]
        """
    ii, oo, m, n = pack(data, constant=constant)
    del data
    soln = gpk_lsq.linear_least_squares(ii, oo, minsv=minsv, minsvr=minsvr)
    del ii
    del oo
    x = soln.x()
    sigmas = numpy.sqrt(soln.x_variances())
    assert sigmas.shape == x.shape
    assert x.ndim == 2
    if constant:
        return (x[1:, :].transpose(), x[0, :],
         sigmas[1:, :].transpose(), sigmas[0, :])
    else:
        return (
         x.transpose(), None,
         sigmas.transpose(), None)


def leaktest():
    import RandomArray
    while 1:
        d = []
        for i in range(100):
            d.append((RandomArray.standard_normal((30, )),
             RandomArray.standard_normal((1000, ))))

        localfit(d)


def test0():
    d = [(numpy.zeros((0, )), numpy.array((1, ))),
     (
      numpy.zeros((0, )), numpy.array((2, ))),
     (
      numpy.zeros((0, )), numpy.array((3, )))]
    coef, const, errs, sv, rank = localfit(d, constant=False)
    assert const is None
    assert coef.shape == (1, 0)
    assert len(errs) == 1
    assert abs(errs[0] - 14) < 0.0001
    assert rank == 0
    assert abs(err_before_fit(d, constant=False) - errs[0]) < 0.0001
    return


def test_localfit11(r):
    d = [
     (
      numpy.array((0, )), numpy.array((-1, ))),
     (
      numpy.array((1, )), numpy.array((0, ))),
     (
      numpy.array((2, )), numpy.array((1.0000001, ))),
     (
      numpy.array((3, )), numpy.array((2, )))]
    if r:
        coef, const, errs, sv, rank = r_localfit(d)
    else:
        coef, const, errs, sv, rank = localfit(d)
    assert const.shape == (1, )
    assert abs(const[0] - -1) < 1e-06
    assert coef.shape == (1, 1)
    assert abs(coef[(0, 0)] - 1) < 1e-06
    assert len(errs) == 1
    assert errs[0] < 1e-06
    assert len(sv) == 2
    assert rank == 2
    assert numpy.alltrue(err_before_fit(d) >= errs)


def test_localfit11e():
    d = [
     (
      numpy.array((0.0, )), numpy.array((0.0, ))),
     (
      numpy.array((1.0, )), numpy.array((1.0, ))),
     (
      numpy.array((2.0, )), numpy.array((0.0, ))),
     (
      numpy.array((3.0, )), numpy.array((-2.0, ))),
     (
      numpy.array((4.0, )), numpy.array((0.0, ))),
     (
      numpy.array((5.0, )), numpy.array((1.0, ))),
     (
      numpy.array((6.0, )), numpy.array((0.0, )))]
    coef, const, errs, sv, rank = localfit(d)
    print 'coef=', coef
    print 'const=', const
    print 'errs=', errs
    assert const.shape == (1, )
    assert abs(const[0] - 0) < 1e-06
    assert coef.shape == (1, 1)
    assert abs(coef[(0, 0)] - 0) < 1e-06
    assert len(errs) == 1
    assert abs(errs[0] - 6) < 1e-06
    assert len(sv) == 2
    assert rank == 2
    assert numpy.absolute(err_before_fit(d) - errs).sum() < 1e-06


def test_localfit21():
    d = [
     (
      numpy.array((0, 0)), numpy.array((-1, ))),
     (
      numpy.array((1, 2)), numpy.array((0, ))),
     (
      numpy.array((2, -1)), numpy.array((1, )))]
    coef, const, errs, sv, rank = localfit(d)
    assert const.shape == (1, )
    assert abs(const[0] - -1) < 1e-06
    assert coef.shape == (1, 2)
    assert numpy.absolute(coef - [[1, 0]]).sum() < 1e-06
    assert len(errs) == 1
    assert errs[0] < 1e-06
    assert len(sv) == 3
    assert rank == 3
    assert numpy.alltrue(err_before_fit(d) >= errs)


def test_localfit21u():
    d = [
     (
      numpy.array((0, 0)), numpy.array((-1, ))),
     (
      numpy.array((2, -1)), numpy.array((1, )))]
    coef, const, errs, sv, rank = localfit(d)
    assert const.shape == (1, )
    assert abs(const[0] - -1) < 1e-06
    assert abs(const[0] + 2 * coef[(0, 0)] - coef[(0, 1)] - 1) < 1e-06
    assert coef.shape == (1, 2)
    assert len(errs) == 1
    assert errs[0] < 1e-06
    assert len(sv) == 2
    assert rank == 2
    assert numpy.alltrue(err_before_fit(d) >= errs)


def test_localfit22(r):
    d = [
     (
      numpy.array((0, 0)), numpy.array((-1, 0))),
     (
      numpy.array((1, 2)), numpy.array((0, 1.0))),
     (
      numpy.array((-1, 2)), numpy.array((-2, 1.0))),
     (
      numpy.array((-1, 1)), numpy.array((-1.9999999, 0.5000001))),
     (
      numpy.array((2, -1)), numpy.array((1, -0.5)))]
    if r:
        coef, const, errs, sv, rank = r_localfit(d)
    else:
        coef, const, errs, sv, rank = localfit(d)
    print const
    print coef
    print errs
    print sv
    print rank
    assert const.shape == (2, )
    assert numpy.absolute(const - [-1, 0]).sum() < 1e-06
    assert coef.shape == (2, 2)
    assert numpy.absolute(coef[0] - [1, 0]).sum() < 1e-06
    assert numpy.absolute(coef[1] - [0, 0.5]).sum() < 1e-06
    assert len(errs) == 2
    assert errs.sum() < 1e-06
    assert len(sv) == 3
    assert rank == 3
    assert numpy.alltrue(err_before_fit(d) >= errs)


def test_fgs1():
    N = 2000
    DSIG = 10.0
    import random, math
    d = []
    for i in range(N):
        s = random.normalvariate(0.0, DSIG)
        d.append((numpy.array([-1.0]), numpy.array([1 - s])))
        d.append((numpy.array([1.0]), numpy.array([1 + s])))

    coef, const, scoef, sconst = fit_giving_sigmas(d)
    assert abs(coef[0][0]) < 3 * DSIG / math.sqrt(N)
    assert abs(coef[0][0]) > 0.001 * DSIG / math.sqrt(N)
    assert abs(const[0] - 1.0) < DSIG / math.sqrt(N)
    assert sconst[0] < DSIG / math.sqrt(N)
    assert abs(coef[0][0]) < 4 * DSIG / 2.0 / math.sqrt(N)
    assert scoef[0][0] < 1.3 * DSIG / math.sqrt(N)
    assert scoef[0][0] > 0.7 * DSIG / math.sqrt(N)
    print 'FGS1 OK'


def test_wt():
    N = 1000
    DSIG = 1.0
    import random
    d = []
    for i in range(N):
        s = random.normalvariate(0.0, DSIG)
        x = random.normalvariate(0.0, DSIG)
        w = random.expovariate(1.0)
        d.append((numpy.array([-x]), numpy.array([1 - s]), w))
        d.append((numpy.array([x]), numpy.array([1 + s]), w))
        d.append((numpy.array([x]), numpy.array([1 - s]), w))
        d.append((numpy.array([-x]), numpy.array([1 + s]), w))

    var1 = err_before_fit(d)
    A, B, errs, sv, rank = localfit(d)
    assert numpy.absolute(var1 - errs).sum() < 0.1


if __name__ == '__main__':
    test0()
    test_wt()
    test_localfit11(False)
    test_localfit11e()
    test_localfit21()
    test_localfit21u()
    for r in [False]:
        test_localfit11(r)
        test_localfit22(r)

    test_fgs1()