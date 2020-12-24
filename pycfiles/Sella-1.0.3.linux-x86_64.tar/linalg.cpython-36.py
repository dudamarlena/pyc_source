# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/sella/linalg.py
# Compiled at: 2020-01-27 13:35:52
# Size of source mod 2**32: 6374 bytes
import numpy as np
from sella.hessian_update import update_H
from scipy.sparse.linalg import LinearOperator
from scipy.linalg import eigh

class NumericalHessian(LinearOperator):
    dtype = np.dtype('float64')

    def __init__(self, func, x0, g0, eta, threepoint=False, Uproj=None):
        self.func = func
        self.x0 = x0.copy()
        self.g0 = g0.copy()
        self.eta = eta
        self.threepoint = threepoint
        self.calls = 0
        self.Uproj = Uproj
        self.ntrue = len(self.x0)
        if self.Uproj is not None:
            ntrue, n = self.Uproj.shape
            assert ntrue == self.ntrue
        else:
            n = self.ntrue
        self.shape = (n, n)
        self.Vs = np.empty((self.ntrue, 0), dtype=(self.dtype))
        self.AVs = np.empty((self.ntrue, 0), dtype=(self.dtype))

    def _matvec(self, v):
        self.calls += 1
        if self.Uproj is not None:
            v = self.Uproj @ v.ravel()
        else:
            vdotg = v.ravel() @ self.g0
            vdotx = v.ravel() @ self.x0
            sign = 1.0
            if abs(vdotg) > 0.0001:
                sign = 2.0 * (vdotg < 0) - 1.0
            else:
                if abs(vdotx) > 0.0001:
                    sign = 2.0 * (vdotx < 0) - 1.0
                else:
                    for vi in v.ravel():
                        if vi > 0.0001:
                            sign = 1.0
                            break
                        elif vi < -0.0001:
                            sign = -1.0
                            break

            vnorm = np.linalg.norm(v) * sign
            _, gplus = self.func(self.x0 + self.eta * v.ravel() / vnorm)
            if self.threepoint:
                fminus, gminus = self.func(self.x0 - self.eta * v.ravel() / vnorm)
                Av = vnorm * (gplus - gminus) / (2 * self.eta)
            else:
                Av = vnorm * (gplus - self.g0) / self.eta
        self.Vs = np.hstack((self.Vs, v.reshape((self.ntrue, -1))))
        self.AVs = np.hstack((self.AVs, Av.reshape((self.ntrue, -1))))
        if self.Uproj is not None:
            Av = self.Uproj.T @ Av
        return Av

    def __add__(self, other):
        return MatrixSum(self, other)

    def _transpose(self):
        return self


class MatrixSum(LinearOperator):

    def __init__(self, *matrices):
        self.dtype = sorted([mat.dtype for mat in matrices], reverse=True)[0]
        self.shape = matrices[0].shape
        mnum = None
        self.matrices = []
        for matrix in matrices:
            if not matrix.dtype <= self.dtype:
                raise AssertionError
            elif not matrix.shape == self.shape:
                raise AssertionError((matrix.shape, self.shape))
            if isinstance(matrix, np.ndarray):
                if mnum is None:
                    mnum = np.zeros((self.shape), dtype=(self.dtype))
                mnum += matrix
            else:
                self.matrices.append(matrix)

        if mnum is not None:
            self.matrices.append(mnum)

    def _matvec(self, v):
        w = np.zeros_like(v, dtype=(self.dtype))
        for matrix in self.matrices:
            w += matrix.dot(v)

        return w

    def _transpose(self):
        return MatrixSum(*[mat.T for mat in self.matrices])

    def __add__(self, other):
        return MatrixSum(*self.matrices, *(other,))


class ApproximateHessian(LinearOperator):

    def __init__(self, dim, B0=None, update_method='TS-BFGS', symm=2):
        """A wrapper object for the approximate Hessian matrix."""
        self.dim = dim
        self.shape = (self.dim, self.dim)
        self.dtype = np.float64
        self.update_method = update_method
        self.symm = symm
        self.set_B(B0)

    def set_B(self, target):
        if target is None:
            self.B = None
            self.evals = None
            self.evecs = None
            return
        else:
            if np.isscalar(target):
                target = target * np.eye(self.dim)
            assert target.shape == self.shape
        self.B = target
        self.evals, self.evecs = eigh(self.B)

    def update(self, dx, dg):
        """Perform a quasi-Newton update on B"""
        self.set_B(update_H((self.B), dx, dg, method=(self.update_method), symm=(self.symm),
          lams=(self.evals),
          vecs=(self.evecs)))

    def project(self, U):
        """Project B into the subspace defined by U."""
        m, n = U.shape
        if not m == self.dim:
            raise AssertionError
        else:
            if self.B is None:
                Bproj = None
            else:
                Bproj = U.T @ self.B @ U
        return ApproximateHessian(n, Bproj, self.update_method, self.symm)

    def asarray(self):
        if self.B is not None:
            return self.B
        else:
            return np.eye(self.dim)

    def _matvec(self, v):
        if self.B is None:
            return v
        else:
            return self.B @ v

    def _rmatvec(self, v):
        return self.matvec(v)

    def _matmat(self, X):
        if self.B is None:
            return X
        else:
            return self.B @ X

    def _rmatmat(self, X):
        return self.matmat(X)

    def __add__(self, other):
        if isinstance(other, ApproximateHessian):
            other = other.B
        else:
            if self.B is None or other is None:
                tot = None
            else:
                tot = self.B + other
        return ApproximateHessian(self.dim, tot, self.update_method, self.symm)