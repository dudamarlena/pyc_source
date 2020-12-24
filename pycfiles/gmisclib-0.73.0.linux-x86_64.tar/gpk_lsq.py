# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/gpk_lsq.py
# Compiled at: 2011-05-11 14:58:46
import math, numpy, gmisclib.Numeric_gpk as NG
_Float = numpy.dtype('float')

class lls_base(object):

    def __init__(self, a, copy=True):
        self.ginv = None
        self._fit = None
        self._x = None
        self._hatdiag = None
        self._y = None
        self.a = numpy.array(a, _Float, copy=copy)
        if self.a.ndim != 2:
            raise ValueError, 'a needs to be 2-dimensional: shape=%s' % str(self.a.shape)
        self.m, self.n = self.a.shape
        self.q = None
        return

    def set_y(self, y, copy=True):
        if y is None:
            return
        else:
            self._fit = None
            self._x = None
            self._y = numpy.array(y, _Float, copy=copy)
            if self._y.ndim == 1:
                self.vector = True
                self._y = self._y.reshape((self._y.shape[0], 1))
            elif self._y.ndim > 2:
                raise ValueError, 'y needs to be 1- or 2-dimensional: shape=%s' % str(self._y.shape)
            else:
                self.vector = False
            if self._y.shape[0] != self.m:
                raise ValueError, 'Matrix sizes do not match: (%d,%d) and %s' % (
                 self.m, self.n, str(self._y.shape))
            self.q = self._y.shape[1]
            return

    def y(self, copy=True):
        assert self._y.shape == (self.m, self.q)
        if self.vector:
            return numpy.array(self._y[:, 0], copy=copy)
        return numpy.array(self._y, copy=copy)

    def _solve(self):
        raise RuntimeError, 'Virtual Function'

    def hat(self, copy=True):
        raise RuntimeError, 'Virtual Function'

    def x--- This code section failed: ---

 L.  62         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'set_y'
                6  LOAD_FAST             1  'y'
                9  CALL_FUNCTION_1       1  None
               12  POP_TOP          

 L.  63        13  LOAD_FAST             0  'self'
               16  LOAD_ATTR             1  '_y'
               19  LOAD_CONST               None
               22  COMPARE_OP            9  is-not
               25  POP_JUMP_IF_TRUE     37  'to 37'
               28  LOAD_ASSERT              AssertionError
               31  LOAD_CONST               'Y not yet set'
               34  RAISE_VARARGS_2       2  None

 L.  64        37  LOAD_FAST             0  'self'
               40  LOAD_ATTR             4  '_x'
               43  LOAD_CONST               None
               46  COMPARE_OP            8  is
               49  POP_JUMP_IF_FALSE    70  'to 70'

 L.  65        52  LOAD_FAST             0  'self'
               55  LOAD_ATTR             5  '_solve'
               58  CALL_FUNCTION_0       0  None
               61  LOAD_FAST             0  'self'
               64  STORE_ATTR            4  '_x'
               67  JUMP_FORWARD          0  'to 70'
             70_0  COME_FROM            67  '67'

 L.  66        70  LOAD_FAST             0  'self'
               73  LOAD_ATTR             6  'vector'
               76  POP_JUMP_IF_FALSE   117  'to 117'

 L.  67        79  LOAD_GLOBAL           7  'numpy'
               82  LOAD_ATTR             8  'array'
               85  LOAD_FAST             0  'self'
               88  LOAD_ATTR             4  '_x'
               91  LOAD_CONST               None
               94  LOAD_CONST               None
               97  BUILD_SLICE_2         2 
              100  LOAD_CONST               0
              103  BUILD_TUPLE_2         2 
              106  BINARY_SUBSCR    
              107  LOAD_CONST               'copy'
              110  LOAD_FAST             2  'copy'
              113  CALL_FUNCTION_257   257  None
              116  RETURN_END_IF    
            117_0  COME_FROM            76  '76'

 L.  68       117  LOAD_GLOBAL           7  'numpy'
              120  LOAD_ATTR             8  'array'
              123  LOAD_FAST             0  'self'
              126  LOAD_ATTR             4  '_x'
              129  LOAD_CONST               'copy'
              132  LOAD_FAST             2  'copy'
              135  CALL_FUNCTION_257   257  None
              138  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_257' instruction at offset 135

    def fit(self, copy=False):
        """
                @except numpy.linalg.linalg.LinAlgError: when the matrix is singular.
                """
        if self._fit is None:
            if self._x is None:
                self._x = self._solve()
            self._fit = numpy.dot(self.a, self._x)
        assert self._fit.shape == (self.m, self.q)
        if self.vector:
            return numpy.array(self._fit[:, 0], copy=copy)
        else:
            return numpy.array(self._fit, copy=copy)

    def residual(self):
        tmp = self.y(copy=False) - self.fit(copy=False)
        assert tmp.shape[0] == self.m
        return tmp

    def variance_about_fit(self):
        """Returns the estimator of the standard deviation
                of the data about the fit.
                @return: L{numpy.ndarray} with shape=(q,).   Each entry corresponds
                        to one of the C{q} sets of equations that are being fit.
                """
        r2 = numpy.sum(numpy.square(self.residual()), axis=0)
        assert self.vector and r2.shape == () or not self.vector and r2.shape == (self.q,)
        return r2 / (self.m - self.n)

    def eff_n(self):
        """Returns something like the number of data, except that it looks at their
                weighting and the structure of the problem.  It counts how many data have a
                relatively large effect on the solution, and if a datum has little influence,
                it doesn't count for much.
                @rtype: float
                """
        return _perplexity(self.hat())

    def eff_rank(self):
        """Returns something like the rank of the solution, but rather than counting
                how many dimensions can be solved at all, it reports how many dimensions can be
                solved with a relatively good accuracy.
                @rtype: float
                """
        raise RuntimeError, 'Virtual Method'


def _perplexity(p):
    numpy.divide(p, numpy.sum(p), p)
    p = numpy.compress(numpy.greater(p, 0.0), p)
    return math.exp(-numpy.sum(p * numpy.log(p)))


class linear_least_squares(lls_base):

    def __init__(self, a, y=None, minsv=None, minsvr=None, copy=True):
        """This solves the set of linear equations a*x = y,
                and allows you to get properties of the fit via methods.
                Normally, a.shape==(m,n) and y.shape==(m,q),
                and the returned x.shape==(n,q).
                where m is the number of constraints provided by the data,
                n is the number of parameters to use in a fit
                (equivalently, the number of basis functions),
                and q is the number of separate sets of equations
                that you are fitting.
                Then, C{self.x()} has shape (n,q) and C{self.the_fit()} has shape (m,q).
                Interpreting this as a linear regression, there are n
                parameters in the model, and m measurements.
                Q is the number of times you apply the model to a
                different data set; each on yields a different solution.
        
                The procedure uses a singular value decomposition algorithm,
                and treats all singular values that are smaller than minsv
                as zero (i.e. drops them). 
                If minsvr is specified, it treates all singular values that
                are smaller than minsvr times the largest s.v. as zero.
                The returned rank is the
                rank of the solution, which is normally the number of
                nonzero elements in x.
                Note that the shape of the solution vector or matrix
                is defined by a and y, and the rank can be smaller
                than m.
        
                @note: Y may be a 1-D matrix (a vector), in which case
                        the fit is a vector.    This is the normal
                        case where you are fitting one equation.
                        If y is a 2-D matrix,
                        each column (second index) in y is a separate fit, and
                        each column in the solution is a separate result.
                """
        lls_base.__init__(self, a, copy=copy)
        self.set_y(y, copy=copy)
        assert minsv is None or minsv >= 0.0
        assert minsvr is None or 0.0 <= minsvr <= 1.0
        r = min(self.m, self.n)
        if self.n > 0:
            u, self.s, vh = numpy.linalg.svd(self.a, full_matrices=False)
        else:
            u = numpy.zeros((self.m, r))
            vh = numpy.zeros((r, self.n))
            self.s = numpy.zeros((r,))
        assert u.shape == (self.m, r)
        assert vh.shape == (r, self.n)
        assert self.s.shape == (r,)
        if minsv is not None and minsvr is not None:
            svrls = max(minsv, minsvr * self.s[numpy.argmax(self.s)])
        elif minsv is not None:
            svrls = minsv
        elif minsvr is not None and self.s.shape[0] > 0:
            svrls = minsvr * self.s[numpy.argmax(self.s)]
        else:
            svrls = 0.0
        self.sim = numpy.greater(self.s, svrls)
        isi = numpy.where(self.sim, 1.0 / numpy.where(self.sim, self.s, 1.0), 0.0)
        ur = u[:, :r]
        numpy.multiply(ur, isi, ur)
        self.ginv = numpy.dot(ur, vh[:r]).transpose()
        return

    def _solve(self):
        return numpy.dot(self.ginv, self._y)

    def sv(self):
        return self.s

    def rank(self):
        return self.sim.sum()

    def hat(self, copy=True):
        """Hat Matrix Diagonal
                Data points that are far from the centroid of the X-space are potentially influential.
                A measure of the distance between a data point, xi,
                and the centroid of the X-space is the data point's associated diagonal
                element hi in the hat matrix. Belsley, Kuh, and Welsch (1980) propose a cutoff of
                2 p/n for the diagonal elements of the hat matrix, where n is the number
                of observations used to fit the model, and p is the number of parameters in the model.
                Observations with hi values above this cutoff should be investigated.
                For linear models, the hat matrix

                C{H = X inv(X'X) X'}

                can be used as a projection matrix.
                The hat matrix diagonal variable contains the diagonal elements
                of the hat matrix

                C{hi = xi inv(X'X) xi'}
                """
        if self._hatdiag is None:
            aainv = numpy.dot(self.ginv, self.ginv.transpose())
            hatdiag = numpy.zeros((self.a.shape[0],), _Float)
            for i in range(hatdiag.shape[0]):
                hatdiag[i] = NG.qform(self.a[i, :], aainv)
                assert -0.001 < hatdiag[i] < 1.001

            self._hatdiag = hatdiag
        return numpy.array(self._hatdiag, copy=copy)

    def x_variances(self):
        """Estimated standard deviations of the solution.
                This is the diagonal of the solution covariance matrix.
                """
        aainv = numpy.dot(self.ginv, self.ginv.transpose())
        vaf = self.variance_about_fit()
        rv = numpy.outer(aainv.diagonal(), vaf)
        assert rv.shape == self._x.shape
        assert rv.shape == (self.n, self.q)
        if self.vector:
            return rv[0, :]
        return rv

    def eff_rank(self):
        return _perplexity(self.sv())


class reg_linear_least_squares(lls_base):

    def __init__--- This code section failed: ---

 L. 288         0  LOAD_GLOBAL           0  'lls_base'
                3  LOAD_ATTR             1  '__init__'
                6  LOAD_FAST             0  'self'
                9  LOAD_FAST             1  'a'
               12  LOAD_CONST               'copy'
               15  LOAD_FAST             6  'copy'
               18  CALL_FUNCTION_258   258  None
               21  POP_TOP          

 L. 289        22  LOAD_FAST             0  'self'
               25  LOAD_ATTR             2  'set_y'
               28  LOAD_FAST             2  'y'
               31  LOAD_CONST               'copy'
               34  LOAD_FAST             6  'copy'
               37  CALL_FUNCTION_257   257  None
               40  POP_TOP          

 L. 291        41  LOAD_FAST             4  'regtgt'
               44  LOAD_CONST               None
               47  COMPARE_OP            8  is
               50  POP_JUMP_IF_FALSE    86  'to 86'

 L. 292        53  LOAD_GLOBAL           4  'numpy'
               56  LOAD_ATTR             5  'zeros'
               59  LOAD_FAST             0  'self'
               62  LOAD_ATTR             6  'n'
               65  LOAD_FAST             0  'self'
               68  LOAD_ATTR             7  'q'
               71  BUILD_TUPLE_2         2 
               74  CALL_FUNCTION_1       1  None
               77  LOAD_FAST             0  'self'
               80  STORE_ATTR            8  'regtgt'
               83  JUMP_FORWARD         27  'to 113'

 L. 294        86  LOAD_GLOBAL           4  'numpy'
               89  LOAD_ATTR             9  'array'
               92  LOAD_FAST             4  'regtgt'
               95  LOAD_GLOBAL          10  '_Float'
               98  LOAD_CONST               'copy'
              101  LOAD_FAST             6  'copy'
              104  CALL_FUNCTION_258   258  None
              107  LOAD_FAST             0  'self'
              110  STORE_ATTR            8  'regtgt'
            113_0  COME_FROM            83  '83'

 L. 295       113  LOAD_FAST             0  'self'
              116  LOAD_ATTR            11  'vector'
              119  POP_JUMP_IF_FALSE   186  'to 186'

 L. 296       122  LOAD_FAST             4  'regtgt'
              125  LOAD_ATTR            12  'ndim'
              128  LOAD_CONST               1
              131  COMPARE_OP            3  !=
              134  POP_JUMP_IF_FALSE   149  'to 149'

 L. 297       137  LOAD_GLOBAL          13  'ValueError'
              140  LOAD_CONST               'regtgt must be a vector if y is a vector.'
              143  RAISE_VARARGS_2       2  None
              146  JUMP_FORWARD          0  'to 149'
            149_0  COME_FROM           146  '146'

 L. 298       149  LOAD_FAST             0  'self'
              152  LOAD_ATTR             8  'regtgt'
              155  LOAD_ATTR            14  'reshape'
              158  LOAD_FAST             4  'regtgt'
              161  LOAD_ATTR            15  'shape'
              164  LOAD_CONST               0
              167  BINARY_SUBSCR    
              168  LOAD_CONST               1
              171  BUILD_TUPLE_2         2 
              174  CALL_FUNCTION_1       1  None
              177  LOAD_FAST             0  'self'
              180  STORE_ATTR            8  'regtgt'
              183  JUMP_FORWARD          0  'to 186'
            186_0  COME_FROM           183  '183'

 L. 300       186  LOAD_FAST             0  'self'
              189  LOAD_ATTR             8  'regtgt'
              192  LOAD_ATTR            12  'ndim'
              195  LOAD_CONST               2
              198  COMPARE_OP            2  ==
              201  POP_JUMP_IF_TRUE    223  'to 223'
              204  LOAD_ASSERT              AssertionError
              207  LOAD_CONST               'Bad dimensionality for regtgt: %d'
              210  LOAD_FAST             0  'self'
              213  LOAD_ATTR             8  'regtgt'
              216  LOAD_ATTR            12  'ndim'
              219  BINARY_MODULO    
              220  RAISE_VARARGS_2       2  None

 L. 301       223  LOAD_FAST             0  'self'
              226  LOAD_ATTR             8  'regtgt'
              229  LOAD_ATTR            15  'shape'
              232  LOAD_CONST               0
              235  BINARY_SUBSCR    
              236  LOAD_FAST             0  'self'
              239  LOAD_ATTR             6  'n'
              242  COMPARE_OP            3  !=
              245  POP_JUMP_IF_FALSE   260  'to 260'

 L. 302       248  LOAD_GLOBAL          13  'ValueError'
              251  LOAD_CONST               'Regtgt shape must match the shape of a'
              254  RAISE_VARARGS_2       2  None
              257  JUMP_FORWARD          0  'to 260'
            260_0  COME_FROM           257  '257'

 L. 304       260  LOAD_GLOBAL           4  'numpy'
              263  LOAD_ATTR            17  'asarray'
              266  LOAD_FAST             3  'regstr'
              269  LOAD_GLOBAL          10  '_Float'
              272  CALL_FUNCTION_2       2  None
              275  STORE_FAST            3  'regstr'

 L. 305       278  LOAD_FAST             3  'regstr'
              281  LOAD_ATTR            12  'ndim'
              284  LOAD_CONST               0
              287  COMPARE_OP            2  ==
              290  POP_JUMP_IF_FALSE   318  'to 318'

 L. 306       293  LOAD_GLOBAL           4  'numpy'
              296  LOAD_ATTR            18  'identity'
              299  LOAD_FAST             0  'self'
              302  LOAD_ATTR             6  'n'
              305  CALL_FUNCTION_1       1  None
              308  LOAD_FAST             3  'regstr'
              311  BINARY_MULTIPLY  
              312  STORE_FAST            3  'regstr'
              315  JUMP_FORWARD          0  'to 318'
            318_0  COME_FROM           315  '315'

 L. 307       318  LOAD_FAST             3  'regstr'
              321  LOAD_ATTR            12  'ndim'
              324  LOAD_CONST               2
              327  COMPARE_OP            2  ==
              330  POP_JUMP_IF_TRUE    349  'to 349'
              333  LOAD_ASSERT              AssertionError
              336  LOAD_CONST               'Wrong dimensionality for regstr: %d'
              339  LOAD_FAST             3  'regstr'
              342  LOAD_ATTR            12  'ndim'
              345  BINARY_MODULO    
              346  RAISE_VARARGS_2       2  None

 L. 308       349  LOAD_FAST             3  'regstr'
              352  LOAD_ATTR            15  'shape'
              355  LOAD_CONST               1
              358  BINARY_SUBSCR    
              359  LOAD_FAST             0  'self'
              362  LOAD_ATTR             6  'n'
              365  COMPARE_OP            2  ==
              368  POP_JUMP_IF_TRUE    377  'to 377'
              371  LOAD_ASSERT              AssertionError
              374  RAISE_VARARGS_1       1  None

 L. 310       377  LOAD_GLOBAL           4  'numpy'
              380  LOAD_ATTR            19  'dot'
              383  LOAD_FAST             3  'regstr'
              386  LOAD_ATTR            20  'transpose'
              389  CALL_FUNCTION_0       0  None
              392  LOAD_FAST             3  'regstr'
              395  CALL_FUNCTION_2       2  None
              398  LOAD_FAST             0  'self'
              401  STORE_ATTR           21  'rr'

 L. 311       404  LOAD_GLOBAL           4  'numpy'
              407  LOAD_ATTR            19  'dot'
              410  LOAD_FAST             0  'self'
              413  LOAD_ATTR            22  'a'
              416  LOAD_ATTR            20  'transpose'
              419  CALL_FUNCTION_0       0  None
              422  LOAD_FAST             0  'self'
              425  LOAD_ATTR            22  'a'
              428  CALL_FUNCTION_2       2  None
              431  LOAD_FAST             0  'self'
              434  STORE_ATTR           23  'aa'

 L. 312       437  LOAD_FAST             5  'rscale'
              440  LOAD_CONST               None
              443  COMPARE_OP            8  is
              446  POP_JUMP_IF_FALSE   461  'to 461'

 L. 313       449  LOAD_CONST               1.0
              452  LOAD_FAST             0  'self'
              455  STORE_ATTR           24  'scale'
              458  JUMP_FORWARD         35  'to 496'

 L. 315       461  LOAD_FAST             5  'rscale'
              464  LOAD_FAST             0  'self'
              467  LOAD_ATTR            23  'aa'
              470  LOAD_ATTR            25  'trace'
              473  CALL_FUNCTION_0       0  None
              476  BINARY_MULTIPLY  
              477  LOAD_FAST             0  'self'
              480  LOAD_ATTR            21  'rr'
              483  LOAD_ATTR            25  'trace'
              486  CALL_FUNCTION_0       0  None
              489  BINARY_DIVIDE    
              490  LOAD_FAST             0  'self'
              493  STORE_ATTR           24  'scale'
            496_0  COME_FROM           458  '458'

 L. 322       496  LOAD_FAST             0  'self'
              499  LOAD_ATTR            23  'aa'
              502  LOAD_FAST             0  'self'
              505  LOAD_ATTR            21  'rr'
              508  LOAD_FAST             0  'self'
              511  LOAD_ATTR            24  'scale'
              514  BINARY_MULTIPLY  
              515  BINARY_ADD       
              516  LOAD_FAST             0  'self'
              519  STORE_ATTR           26  'aareg'
              522  LOAD_CONST               None
              525  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 522

    def _solve(self):
        """
                @except numpy.linalg.linalg.LinAlgError: when the matrix is singular.
                """
        ayreg = numpy.dot(self.a.transpose(), self._y) + numpy.dot(self.rr, self.regtgt) * self.scale
        return numpy.linalg.solve(self.aareg, ayreg)

    def sv_reg(self):
        """Singular values of the regularized problem."""
        return numpy.sqrt(numpy.linalg.eigvalsh(self.aareg))

    def sv_unreg(self):
        """Singular values of the unregularized problem."""
        return numpy.sqrt(numpy.linalg.eigvalsh(self.aa))

    def eff_rank(self):
        return _perplexity(self.sv_reg())

    def hat(self, copy=True):
        """Hat Matrix Diagonal
                Data points that are far from the centroid of the X-space are potentially influential.
                A measure of the distance between a data point, xi,
                and the centroid of the X-space is the data point's associated diagonal
                element hi in the hat matrix. Belsley, Kuh, and Welsch (1980) propose a cutoff of
                2 p/n for the diagonal elements of the hat matrix, where n is the number
                of observations used to fit the model, and p is the number of parameters in the model.
                Observations with hi values above this cutoff should be investigated.
                For linear models, the hat matrix

                C{H = X (X'X)-1 X' }

                can be used as a projection matrix.
                The hat matrix diagonal variable contains the diagonal elements
                of the hat matrix

                C{hi = xi (X'X)-1 xi' }
                """
        if self._hatdiag is None:
            hatdiag = numpy.zeros((self.aa.shape[0],), _Float)
            iaareg = numpy.linalg.inv(self.aareg)
            for i in range(hatdiag.shape[0]):
                hatdiag[i] = NG.qform(self.a[i, :], iaareg)
                assert -0.001 < hatdiag[i] < 1.001

            self._hatdiag = hatdiag
        return numpy.array(self._hatdiag, copy=copy)


def test_svd():
    a0 = numpy.array([[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
     [
      0, 0, 0, 0, 0, 0, 0, -3, -2, -1, 0, 1, 2, 3, 0, 0, 0, 0, 0],
     [
      0, 0, 0, 0, 0, 0, 0, 1, -1, 1, -1, 1, -1, 1, 0, 0, 0, 0, 0]], _Float)
    a1 = numpy.array([[1, 1, 1],
     [
      -3, -2, -1],
     [
      1, -1, 1]], _Float)
    a2 = numpy.array([[1, 1, 1], [-3, -2, -1], [1, -1, 1], [0, 0, 2.2], [2, 0, 0], [0, 1, 0]], _Float)
    for a in [a0, a1, a2]:
        u, s, vh = numpy.linalg.svd(a)
        r = min(a.shape)
        assert numpy.alltrue(s >= 0.0)
        err = numpy.sum(numpy.square(numpy.dot(u[:, :r] * s, vh[:r]) - a))
        assert err < 1e-06


def all_between(a, vec, b):
    return numpy.alltrue(numpy.greater_equal(vec, a) * numpy.greater_equal(b, vec))


def test0():
    y = numpy.array([0, 1, 2, 3, 4, 5], numpy.float)
    basis = numpy.zeros((6, 0))
    soln = linear_least_squares(basis, y, 1e-06)
    assert numpy.absolute(soln.fit()).sum() < 0.0001
    assert numpy.absolute(soln.residual() - y).sum() < 0.0001
    assert soln.rank() == 0
    assert soln.x().shape == (0, )


def test_vec():
    basis = numpy.transpose([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    y = numpy.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], _Float)
    soln = linear_least_squares(basis, y, 1e-06)
    hat = soln.hat()
    assert numpy.alltrue(hat > 1.0 / y.shape[0])
    assert numpy.alltrue(hat < 4.0 / y.shape[0])
    assert soln.rank() == 2
    print 'fitshape=', soln.fit().shape, y.shape
    print 'y=', y
    print 'fit=', soln.fit()
    err = numpy.sum(numpy.square(soln.fit() - y))
    assert 0.0 <= err < 1e-06
    print 'soln.residual=', soln.residual()
    assert all_between(-1e-06, soln.residual(), 1e-06)
    assert soln.sv().shape == (2, )
    assert abs(soln.x()[0] - 1) < 1e-06
    assert abs(soln.x()[1] + 1) < 1e-06
    assert numpy.absolute(numpy.dot(basis, soln.x()) - soln.fit()).sum() < 1e-06


def test_vec2():
    basis = numpy.transpose([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
     [
      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    y = numpy.array([0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0], _Float)
    soln = linear_least_squares(basis, y, 1e-06)
    assert soln.rank() == 2
    err = numpy.sum((soln.fit() - y) ** 2)
    avg = 10.0 / 11.0
    epred = 6.0 * avg ** 2 + 5.0 * (2 - avg) ** 2
    assert soln.sv().shape == (2, )
    assert abs(soln.x()[1] - avg) < 1e-06
    assert abs(soln.x()[0]) < 1e-06
    assert abs(err - epred) < 0.0001


def test_m1():
    basis = numpy.transpose([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    y = numpy.transpose([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]])
    assert y.shape[1] == 1
    soln = linear_least_squares(basis, y, 1e-06)
    assert soln.x().shape[1] == 1
    assert soln.fit().shape[1] == 1
    assert soln.rank() == 2
    err = soln.residual() ** 2
    assert all_between(0, err, 1e-06)
    assert soln.sv().shape == (2, )
    assert abs(soln.x()[(0, 0)] - 1) < 1e-06
    assert abs(soln.x()[(1, 0)] + 1) < 1e-06
    assert numpy.absolute(numpy.ravel(numpy.dot(basis, soln.x()) - y)).sum() < 1e-06


def test_m2():
    basis = numpy.transpose([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    y = numpy.transpose([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]])
    assert y.shape[1] == 2
    soln = linear_least_squares(basis, y, 1e-06)
    assert soln.x().shape[1] == 2
    assert soln.fit().shape[1] == 2
    assert soln.rank() == 2
    err = numpy.sum((soln.fit() - y) ** 2, axis=0)
    assert err.shape[0] == 2
    assert all_between(0.0, err, 1e-06)
    assert soln.sv().shape == (2, )
    assert abs(soln.x()[(0, 0)] - 1) < 1e-06
    assert abs(soln.x()[(1, 0)] + 1) < 1e-06
    assert abs(soln.x()[(0, 1)] + 1) < 1e-06
    assert abs(soln.x()[(1, 1)] - 10) < 1e-06
    assert numpy.absolute(numpy.ravel(numpy.dot(basis, soln.x()) - y)).sum() < 1e-06


def test_m2r():
    basis = numpy.transpose([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    y = numpy.transpose([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]])
    assert y.shape[1] == 2
    soln = reg_linear_least_squares(basis, y, numpy.zeros((2, 2), _Float), [[0.0, 0.0], [0.0, 0.0]])
    hat = soln.hat()
    assert numpy.alltrue(hat > 1.0 / y.shape[0])
    assert numpy.alltrue(hat < 4.0 / y.shape[0])
    assert soln.x().shape[1] == 2
    assert soln.fit().shape[1] == 2
    err = numpy.sum((soln.fit() - y) ** 2, axis=0)
    assert err.shape[0] == 2
    assert all_between(0.0, err, 1e-06)
    assert abs(soln.x()[(0, 0)] - 1) < 1e-06
    assert abs(soln.x()[(1, 0)] + 1) < 1e-06
    assert abs(soln.x()[(0, 1)] + 1) < 1e-06
    assert abs(soln.x()[(1, 1)] - 10) < 1e-06
    assert numpy.absolute(numpy.ravel(numpy.dot(basis, soln.x()) - y)).sum() < 1e-06


def test_m2rR():
    basis = numpy.transpose([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    y = numpy.transpose([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]])
    assert y.shape[1] == 2
    soln = reg_linear_least_squares(basis, y, 1000000.0 * numpy.identity(2), [[0.5, 0.5], [0.5, 0.5]])
    assert soln.x().shape[1] == 2
    assert soln.fit().shape[1] == 2
    err = numpy.sum((soln.fit() - y) ** 2, axis=0)
    assert err.shape[0] == 2
    assert all_between(1.0, err, 500.0)
    assert abs(soln.x()[(0, 0)] - 0.5) < 0.001
    assert abs(soln.x()[(1, 0)] - 0.5) < 0.001
    assert abs(soln.x()[(0, 1)] - 0.5) < 0.001
    assert abs(soln.x()[(1, 1)] - 0.5) < 0.001
    soln = reg_linear_least_squares(basis, y, 1000000.0, numpy.zeros((2, 2)))
    print 'soln.x=', soln.x()
    assert abs(soln.x()[(0, 0)]) < 0.001
    assert abs(soln.x()[(1, 0)]) < 0.001
    assert abs(soln.x()[(0, 1)]) < 0.001
    assert abs(soln.x()[(1, 1)]) < 0.001
    soln = reg_linear_least_squares(basis, y, 1, [[0.5, 0.5], [0.5, 0.5]], rscale=1000000.0)
    assert abs(soln.x()[(0, 0)] - 0.5) < 0.001
    assert abs(soln.x()[(1, 0)] - 0.5) < 0.001
    assert abs(soln.x()[(0, 1)] - 0.5) < 0.001
    assert abs(soln.x()[(1, 1)] - 0.5) < 0.001
    print 's', soln.x()
    print 'f', soln.fit()
    print 'r', soln.eff_rank()


def test_hat():
    """Make sure that the hat function meets its definition."""
    basis = numpy.transpose([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    y0 = numpy.transpose([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    s0 = linear_least_squares(basis, y0)
    assert y0.shape[0] > 1
    for i in range(y0.shape[0]):
        y = numpy.array(y0)
        y[i] += 1
        s = linear_least_squares(basis, y)
        ishift = s.fit()[i] - s0.fit()[i]
        assert -0.001 <= ishift <= 1.001
        assert abs(ishift - s0.hat()[i]) < 0.001


if __name__ == '__main__':
    test0()
    test_svd()
    test_vec()
    test_m1()
    test_m2()
    test_vec2()
    test_m2r()
    test_m2rR()
    test_hat()