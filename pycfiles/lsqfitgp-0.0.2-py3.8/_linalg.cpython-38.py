# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/lsqfitgp/_linalg.py
# Compiled at: 2020-04-26 18:08:00
# Size of source mod 2**32: 14050 bytes
import abc
from autograd import numpy as np
from autograd.scipy import linalg
from autograd import extend
import scipy.sparse as slinalg
__doc__ = '\n\nDecompositions of positive definite matrices. A decomposition object is\ninitialized with a matrix and then can solve linear systems for that matrix.\nThese classes never check for infs/nans in the matrices.\n\nClasses\n-------\nDecompMeta :\n    Metaclass that adds autograd support.\nDecomposition :\n    Abstract base class.\nDiag :\n    Diagonalization.\nEigCutFullRank :\n    Diagonalization rounding up small eigenvalues.\nEigCutLowRank :\n    Diagonalization removing small eigenvalues.\nReduceRank :\n    Partial diagonalization with higher eigenvalues only.\nChol :\n    Cholesky decomposition.\nCholMaxEig :\n    Cholesky regularized using the maximum eigenvalue.\nCholGersh :\n    Cholesky regularized using an estimate of the maximum eigenvalue.\nBlockDecomp :\n    Decompose a block matrix.\n\n'

def noautograd(x):
    """
    Unpack an autograd numpy array.
    """
    if isinstance(x, np.numpy_boxes.ArrayBox):
        return noautograd(x._value)
    return x


def asinexact(dtype):
    """
    Return dtype if it is inexact, else float64.
    """
    if np.issubdtype(dtype, np.inexact):
        return dtype
    return np.float64


class DecompMeta(abc.ABCMeta):
    __doc__ = '\n    Metaclass for adding autograd support to subclasses of Decomposition.\n    '

    def __init__(cls, *args):
        old__init__ = cls.__init__

        def __init__(self, K, **kw):
            old__init__(self, (noautograd(K)), **kw)
            self._K = K

        cls.__init__ = __init__
        oldsolve = cls.solve
        if not hasattr(oldsolve, '_autograd'):

            @extend.primitive
            def solve_autograd(self, K, b):
                return oldsolve(self, b)

            def solve_vjp_K(ans, self, K, b):
                assert ans.shape == b.shape
                assert b.shape[0] == K.shape[0] == K.shape[1]

                def vjp(g):
                    assert g.shape[-len(b.shape):] == b.shape
                    g = np.moveaxis(g, -len(b.shape), 0)
                    A = solve_autograd(self, K, g)
                    B = np.moveaxis(ans, 0, -1)
                    AB = np.tensordot(A, B, len(b.shape) - 1)
                    AB = np.moveaxis(AB, 0, -2)
                    assert AB.shape == g.shape[:-len(b.shape)] + K.shape
                    return -AB

                return vjp

            def solve_vjp_b(ans, self, K, b):
                assert ans.shape == b.shape
                assert b.shape[0] == K.shape[0] == K.shape[1]

                def vjp(g):
                    assert g.shape[-len(b.shape):] == b.shape
                    g = np.moveaxis(g, -len(b.shape), 0)
                    gj = solve_autograd(self, K, g)
                    gj = np.moveaxis(gj, 0, -len(b.shape))
                    assert gj.shape == g.shape
                    return gj

                return vjp

            extend.defvjp(solve_autograd,
              solve_vjp_K,
              solve_vjp_b,
              argnums=[
             1, 2])

            def solve(self, b):
                return solve_autograd(self, self._K, b)

            solve._autograd = solve_autograd
            cls.solve = solve
        oldquad = cls.quad
        if not hasattr(oldquad, '_autograd'):

            def quad(self, b):
                if isinstance(self._K, np.numpy_boxes.ArrayBox):
                    return b.T @ self.solve(b)
                return oldquad(self, b)

            quad._autograd = True
            cls.quad = quad
        oldlogdet = cls.logdet
        if not hasattr(oldlogdet, '_autograd'):

            @extend.primitive
            def logdet_autograd(self, K):
                return oldlogdet(self)

            def logdet_vjp(ans, self, K):
                assert ans.shape == ()
                assert K.shape[0] == K.shape[1]

                def vjp(g):
                    invK = self.solve._autograd(self, K, np.eye(len(K)))
                    return g[(Ellipsis, None, None)] * invK

                return vjp

            extend.defvjp(logdet_autograd,
              logdet_vjp,
              argnums=[
             1])

            def logdet_jvp(ans, self, K):
                assert ans.shape == ()
                assert K.shape[0] == K.shape[1]

                def jvp(g):
                    assert g.shape[:2] == K.shape
                    return np.trace(solve_autograd(self, K, g))

                return jvp

            extend.defjvp(logdet_autograd,
              logdet_jvp,
              argnums=[
             1])

            def logdet(self):
                return logdet_autograd(self, self._K)

            logdet._autograd = True
            cls.logdet = logdet


class Decomposition(metaclass=DecompMeta):
    __doc__ = '\n    \n    Abstract base class for positive definite symmetric matrices decomposition.\n    \n    Methods\n    -------\n    solve\n    usolve\n    quad\n    logdet\n    \n    '

    @abc.abstractmethod
    def __init__(self, K):
        """
        Decompose matrix K.
        """
        pass

    @abc.abstractmethod
    def solve(self, b):
        """
        Solve the linear system K @ x = b.
        """
        pass

    @abc.abstractmethod
    def usolve(self, ub):
        """
        Solve the linear system K @ x = b where b is possibly an array of
        `gvar`s.
        """
        pass

    def quad(self, b):
        """
        Compute the quadratic form b.T @ inv(K) @ b.
        """
        return b.T @ self.solve(b)

    @abc.abstractmethod
    def logdet(self):
        """
        Compute log(det(K)).
        """
        pass


class Diag(Decomposition):
    __doc__ = '\n    Diagonalization.\n    '

    def __init__(self, K):
        self._w, self._V = linalg.eigh(K, check_finite=False)

    def solve(self, b):
        return self._V / self._w @ (self._V.T @ b)

    usolve = solve

    def quad(self, b):
        VTb = self._V.T @ b
        return VTb.T / self._w @ VTb

    def logdet(self):
        return np.sum(np.log(self._w))

    def _eps--- This code section failed: ---

 L. 242         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _w
                4  STORE_FAST               'w'

 L. 243         6  LOAD_FAST                'eps'
                8  LOAD_CONST               None
               10  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE    40  'to 40'

 L. 244        14  LOAD_GLOBAL              len
               16  LOAD_FAST                'w'
               18  CALL_FUNCTION_1       1  ''
               20  LOAD_GLOBAL              np
               22  LOAD_METHOD              finfo
               24  LOAD_GLOBAL              asinexact
               26  LOAD_FAST                'w'
               28  LOAD_ATTR                dtype
               30  CALL_FUNCTION_1       1  ''
               32  CALL_METHOD_1         1  ''
               34  LOAD_ATTR                eps
               36  BINARY_MULTIPLY  
               38  STORE_FAST               'eps'
             40_0  COME_FROM            12  '12'

 L. 245        40  LOAD_GLOBAL              np
               42  LOAD_METHOD              isscalar
               44  LOAD_FAST                'eps'
               46  CALL_METHOD_1         1  ''
               48  POP_JUMP_IF_FALSE    72  'to 72'
               50  LOAD_CONST               0
               52  LOAD_FAST                'eps'
               54  DUP_TOP          
               56  ROT_THREE        
               58  COMPARE_OP               <=
               60  POP_JUMP_IF_FALSE    70  'to 70'
               62  LOAD_CONST               1
               64  COMPARE_OP               <
               66  POP_JUMP_IF_TRUE     76  'to 76'
               68  JUMP_FORWARD         72  'to 72'
             70_0  COME_FROM            60  '60'
               70  POP_TOP          
             72_0  COME_FROM            68  '68'
             72_1  COME_FROM            48  '48'
               72  LOAD_GLOBAL              AssertionError
               74  RAISE_VARARGS_1       1  'exception instance'
             76_0  COME_FROM            66  '66'

 L. 246        76  LOAD_FAST                'eps'
               78  LOAD_GLOBAL              np
               80  LOAD_METHOD              max
               82  LOAD_FAST                'w'
               84  CALL_METHOD_1         1  ''
               86  BINARY_MULTIPLY  
               88  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 88


class EigCutFullRank(Diag):
    __doc__ = '\n    Diagonalization. Eigenvalues below `eps` are set to `eps`, where `eps` is\n    relative to the largest eigenvalue.\n    '

    def __init__(self, K, eps=None, **kw):
        (super().__init__)(K, **kw)
        eps = self._eps(eps)
        self._w[self._w < eps] = eps


class EigCutLowRank(Diag):
    __doc__ = '\n    Diagonalization. Eigenvalues below `eps` are removed, where `eps` is\n    relative to the largest eigenvalue.\n    '

    def __init__(self, K, eps=None, **kw):
        (super().__init__)(K, **kw)
        eps = self._eps(eps)
        subset = slice(np.sum(self._w < eps), None)
        self._w = self._w[subset]
        self._V = self._V[:, subset]


class ReduceRank(Diag):
    __doc__ = '\n    Keep only the first `rank` higher eigenmodes.\n    '

    def __init__(self, K, rank=1):
        if not (isinstance(rank, (int, np.integer)) and rank >= 1):
            raise AssertionError
        self._w, self._V = slinalg.eigsh(K, k=rank, which='LM')


def solve_triangular(a, b, lower=False):
    """
    Pure python implementation of scipy.linalg.solve_triangular for when
    a or b are object arrays.
    """
    x = np.copy(b)
    a = a.reshape(a.shape + (1, ) * len(x.shape[1:]))
    if lower:
        x[0] /= a[(0, 0)]
        for i in range(1, len(x)):
            x[i:] -= x[(i - 1)] * a[i:, i - 1]
            x[i] /= a[(i, i)]

    else:
        x[(-1)] /= a[(-1, -1)]
        for i in range(len(x) - 1, 0, -1):
            x[:i] -= x[i] * a[:i, i]
            x[(i - 1)] /= a[(i - 1, i - 1)]
        else:
            return x


def grad_chol(L):
    """
    Inverse of the Jacobian of the cholesky factor respect to the decomposed
    matrix, reshaped as a 2D matrix. It should actually work for any
    decomposition of the type A = L @ L.T, whatever is L. (Not tested.)
    """
    n = len(L)
    I = np.eye(n)
    s1 = I[:, None, :, None] * L[None, :, None, :]
    s2 = I[None, :, :, None] * L[:, None, None, :]
    return (s1 + s2).reshape(2 * (n ** 2,))


class Chol(Decomposition):
    __doc__ = '\n    Cholesky decomposition.\n    '

    def __init__(self, K):
        self._L = linalg.cholesky(K, lower=True, check_finite=False)

    def solve(self, b):
        invLb = linalg.solve_triangular((self._L), b, lower=True)
        return linalg.solve_triangular((self._L.T), invLb, lower=False)

    def usolve(self, b):
        invLb = solve_triangular((self._L), b, lower=True)
        return solve_triangular((self._L.T), invLb, lower=False)

    def quad(self, b):
        invLb = linalg.solve_triangular((self._L), b, lower=True)
        return invLb.T @ invLb

    def logdet(self):
        return 2 * np.sum(np.log(np.diag(self._L)))

    def _eps--- This code section failed: ---

 L. 340         0  LOAD_FAST                'eps'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    34  'to 34'

 L. 341         8  LOAD_GLOBAL              len
               10  LOAD_FAST                'K'
               12  CALL_FUNCTION_1       1  ''
               14  LOAD_GLOBAL              np
               16  LOAD_METHOD              finfo
               18  LOAD_GLOBAL              asinexact
               20  LOAD_FAST                'K'
               22  LOAD_ATTR                dtype
               24  CALL_FUNCTION_1       1  ''
               26  CALL_METHOD_1         1  ''
               28  LOAD_ATTR                eps
               30  BINARY_MULTIPLY  
               32  STORE_FAST               'eps'
             34_0  COME_FROM             6  '6'

 L. 342        34  LOAD_GLOBAL              np
               36  LOAD_METHOD              isscalar
               38  LOAD_FAST                'eps'
               40  CALL_METHOD_1         1  ''
               42  POP_JUMP_IF_FALSE    66  'to 66'
               44  LOAD_CONST               0
               46  LOAD_FAST                'eps'
               48  DUP_TOP          
               50  ROT_THREE        
               52  COMPARE_OP               <=
               54  POP_JUMP_IF_FALSE    64  'to 64'
               56  LOAD_CONST               1
               58  COMPARE_OP               <
               60  POP_JUMP_IF_TRUE     70  'to 70'
               62  JUMP_FORWARD         66  'to 66'
             64_0  COME_FROM            54  '54'
               64  POP_TOP          
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            42  '42'
               66  LOAD_GLOBAL              AssertionError
               68  RAISE_VARARGS_1       1  'exception instance'
             70_0  COME_FROM            60  '60'

 L. 343        70  LOAD_FAST                'eps'
               72  LOAD_FAST                'maxeigv'
               74  BINARY_MULTIPLY  
               76  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 76


class CholMaxEig(Chol):
    __doc__ = '\n    Cholesky decomposition. The matrix is corrected for numerical roundoff\n    by adding to the diagonal a small number relative to the maximum eigenvalue.\n    `eps` multiplies this number.\n    '

    def __init__(self, K, eps=None, **kw):
        w = slinalg.eigsh(K, k=1, which='LM', return_eigenvectors=False)
        eps = self._eps(eps, K, w[0])
        (super().__init__)((K + np.diag(np.full(len(K), eps))), **kw)


class CholGersh(Chol):
    __doc__ = '\n    Cholesky decomposition. The matrix is corrected for numerical roundoff\n    by adding to the diagonal a small number relative to the maximum eigenvalue.\n    `eps` multiplies this number. The maximum eigenvalue is estimated\n    with the Gershgorin theorem.\n    '

    def __init__(self, K, eps=None, **kw):
        maxeigv = _gershgorin_eigval_bound(K)
        eps = self._eps(eps, K, maxeigv)
        (super().__init__)((K + np.diag(np.full(len(K), eps))), **kw)


def _gershgorin_eigval_bound(K):
    """
    Upper bound on the largest magnitude eigenvalue of the matrix.
    """
    return np.max(np.sum((np.abs(K)), axis=1))


class BlockDecomp:
    __doc__ = '\n    Decomposition of a 2x2 symmetric block matrix using decompositions of the\n    diagonal blocks.\n    \n    Reference: Gaussian Processes for Machine Learning, A.3, p. 201.\n    '

    def __init__(self, P_decomp, S, Q, S_decomp_class):
        """
        The matrix to be decomposed is
        
        A = [[P,   Q]
             [Q.T, S]]
        
        Parameters
        ----------
        P_decomp : Decomposition
            An instantiated decomposition of P.
        S, Q : matrices
            The other blocks.
        S_decomp_class : DecompMeta
            A subclass of Decomposition used to decompose S - Q.T P^-1 Q.
        """
        self._Q = Q
        self._invP = P_decomp
        self._tildeS = S_decomp_class(S - P_decomp.quad(Q))

    def solve(self, b):
        invP = self._invP
        tildeS = self._tildeS
        Q = self._Q
        f = b[:len(Q)]
        g = b[len(Q):]
        y = tildeS.solve(g - Q.T @ invP.solve(f))
        x = invP.solve(f - Q @ y)
        return np.concatenate([x, y])

    def usolve(self, b):
        invP = self._invP
        tildeS = self._tildeS
        Q = self._Q
        f = b[:len(Q)]
        g = b[len(Q):]
        y = tildeS.usolve(g - Q.T @ invP.usolve(f))
        x = invP.usolve(f - Q @ y)
        return np.concatenate([x, y])

    def quad(self, b):
        invP = self._invP
        tildeS = self._tildeS
        Q = self._Q
        f = b[:len(Q)]
        g = b[len(Q):]
        QTinvPf = Q.T @ invP.solve(f)
        fTinvPQtildeSg = QTinvPf.T @ tildeS.solve(g)
        return invP.quad(f) + tildeS.quad(QTinvPf) - fTinvPQtildeSg - fTinvPQtildeSg.T + tildeS.quad(g)

    def logdet(self):
        return self._invP.logdet() + self._tildeS.logdet()