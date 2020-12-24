# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/sella/optimize/restricted_step.py
# Compiled at: 2020-01-27 19:12:33
# Size of source mod 2**32: 5821 bytes
import numpy as np, inspect
from .stepper import get_stepper, BaseStepper, NaiveStepper

class BaseRestrictedStep:
    synonyms = None

    def __init__(self, pes, order, delta, method='qn', tol=1e-15, maxiter=1000, d1=None):
        self.pes = pes
        self.delta = delta
        self.d1 = d1
        g0 = self.pes.get_g()
        self.scons = self.pes.get_scons()
        g = g0 + self.pes.get_H() @ self.scons
        if inspect.isclass(method):
            if issubclass(method, BaseStepper):
                stepper = method
            else:
                stepper = get_stepper(method.lower())
        else:
            if self.cons(self.scons) - self.delta > 1e-08:
                self.P = self.pes.get_Unred().T
                dx = self.P @ self.scons
                self.stepper = NaiveStepper(dx)
                self.scons[:] *= 0
            else:
                self.P = self.pes.get_Ufree().T @ self.pes.get_W()
                d1 = self.d1
                if d1 is not None:
                    d1 = np.linalg.lstsq((self.P.T), d1, rcond=None)[0]
                self.stepper = stepper((self.P @ g), (self.pes.get_HL().project(self.P.T)),
                  order,
                  d1=d1)
        self.tol = tol
        self.maxiter = maxiter

    def cons(self, s, dsda=None):
        raise NotImplementedError

    def eval(self, alpha):
        s, dsda = self.stepper.get_s(alpha)
        stot = self.P.T @ s + self.scons
        val, dval = self.cons(stot, self.P.T @ dsda)
        return (stot, val, dval)

    def get_s(self):
        alpha = self.stepper.alpha0
        s, val, dval = self.eval(alpha)
        if val < self.delta:
            assert val > 0.0
            return (
             s, val)
        else:
            err = val - self.delta
            lower = self.stepper.alphamin
            upper = self.stepper.alphamax
            for niter in range(self.maxiter):
                if abs(err) <= self.tol:
                    break
                else:
                    if np.nextafter(lower, upper) >= upper:
                        break
                    else:
                        if err * self.stepper.slope > 0:
                            upper = alpha
                        else:
                            lower = alpha
                    a1 = alpha - err / dval
                    if np.isnan(a1) or a1 <= lower or a1 >= upper or niter > 4:
                        a2 = (lower + upper) / 2.0
                        if np.isinf(a2):
                            alpha = alpha + max(1, 0.5 * alpha) * np.sign(a2)
                        else:
                            alpha = a2
                    else:
                        alpha = a1
                s, val, dval = self.eval(alpha)
                err = val - self.delta
            else:
                raise RuntimeError('Restricted step failed to converge!')

            assert val > 0
            return (s, self.delta)

    @classmethod
    def match(cls, name):
        return name in cls.synonyms


class TrustRegion(BaseRestrictedStep):
    synonyms = [
     'tr', 'trust region', 'trust-region', 'trust radius',
     'trust-radius']

    def cons(self, s, dsda=None):
        val = np.linalg.norm(s)
        if dsda is None:
            return val
        else:
            dval = dsda @ s / val
            return (val, dval)


class IRCTrustRegion(TrustRegion):
    synonyms = []

    def __init__(self, *args, sqrtm=None, **kwargs):
        if not sqrtm is not None:
            raise AssertionError
        else:
            self.sqrtm = sqrtm
            (TrustRegion.__init__)(self, *args, **kwargs)
            assert self.d1 is not None

    def cons(self, s, dsda=None):
        s = (s + self.d1) * self.sqrtm
        if dsda is not None:
            dsda = dsda * self.sqrtm
        return TrustRegion.cons(self, s, dsda)


class RestrictedAtomicStep(BaseRestrictedStep):
    synonyms = [
     'ras', 'restricted atomic step']

    def __init__(self, pes, *args, **kwargs):
        if pes.int is not None:
            raise ValueError('Internal coordinates are not compatible with the {} trust region method.'.format(self.__class__.__name__))
        (BaseRestrictedStep.__init__)(self, pes, *args, **kwargs)

    def cons(self, s, dsda=None):
        s_mat = s.reshape((-1, 3))
        s_norms = np.linalg.norm(s_mat, axis=1)
        index = np.argmax(s_norms)
        val = s_norms[index]
        if dsda is None:
            return val
        else:
            dsda_mat = dsda.reshape((-1, 3))
            dval = dsda_mat[index] @ s_mat[index] / val
            return (val, dval)


class MaxInternalStep(BaseRestrictedStep):
    synonyms = [
     'mis', 'max internal step']

    def __init__(self, pes, *args, wx=1.0, wb=1.0, wa=1.0, wd=1.0, **kwargs):
        if pes.int is None:
            raise ValueError('Internal coordinates are required for the {} trust region method'.format(self.__class__.__name__))
        self.wx = wx
        self.wb = wb
        self.wa = wa
        self.wd = wd
        (BaseRestrictedStep.__init__)(self, pes, *args, **kwargs)

    def cons(self, s, dsda=None):
        w = np.array([
         self.wx] * self.pes.int.ncart + [self.wb] * self.pes.int.nbonds + [self.wa] * self.pes.int.nangles + [self.wd] * self.pes.int.ndihedrals + [self.wa] * self.pes.int.nangle_sums + [self.wa] * self.pes.int.nangle_diffs)
        assert len(w) == len(s)
        sw = np.abs(s * w)
        idx = np.argmax(np.abs(sw))
        val = sw[idx]
        if dsda is None:
            return val
        else:
            return (
             val, np.sign(s[idx]) * dsda[idx] * w[idx])


_all_restricted_step = [
 TrustRegion, RestrictedAtomicStep, MaxInternalStep]

def get_restricted_step(name):
    for rs in _all_restricted_step:
        if rs.match(name):
            return rs

    raise ValueError('Unknown restricted step name: {}'.format(name))