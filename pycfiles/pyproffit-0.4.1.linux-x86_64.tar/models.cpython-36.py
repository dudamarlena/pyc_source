# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyproffit/models.py
# Compiled at: 2019-11-11 09:06:49
# Size of source mod 2**32: 2326 bytes
import numpy as np

def BetaModel(x, beta, rc, norm, bkg):
    n2 = np.power(10.0, norm)
    c2 = np.power(10.0, bkg)
    out = n2 * np.power(1.0 + (x / rc) ** 2, -3.0 * beta + 0.5) + c2
    return out


def DoubleBeta(x, beta, rc1, rc2, ratio, norm, bkg):
    comp1 = np.power(1.0 + (x / rc1) ** 2, -3.0 * beta + 0.5)
    comp2 = np.power(1.0 + (x / rc2) ** 2, -3.0 * beta + 0.5)
    n2 = np.power(10.0, norm)
    c2 = np.power(10.0, bkg)
    out = n2 * (comp1 + ratio * comp2) + c2
    return out


def PowerLaw(x, alpha, norm, pivot, bkg):
    n2 = np.power(10.0, norm)
    c2 = np.power(10.0, bkg)
    out = n2 * np.power(x / pivot, -alpha) + c2
    return out


def Const(x, bkg):
    out = np.power(10.0, bkg) * np.ones(len(x))
    return out


def Vikhlinin(x, beta, rc, alpha, rs, epsilon, gamma, norm, bkg):
    term1 = np.power(x / rc, -alpha) * np.power(1.0 + (x / rc) ** 2, -3 * beta)
    term2 = np.power(1.0 + (x / rs) ** gamma, -epsilon / gamma)
    n2 = np.power(10.0, norm)
    b2 = np.power(10.0, bkg)
    return n2 * term1 * term2 + b2


def IntFunc(omega, rf, alpha, xmin, xmax):
    nb = 100
    logmin = np.log10(xmin)
    logmax = np.log10(xmax)
    x = np.logspace(logmin, logmax, nb + 1)
    z = (x[:nb] + np.roll(x, (-1), axis=0)[:nb]) / 2.0
    width = np.roll(x, (-1), axis=0)[:nb] - x[:nb]
    term1 = (omega ** 2 + z ** 2) / rf ** 2
    term2 = np.power(term1, -alpha)
    intot = np.sum((term2 * width), axis=0)
    return intot


def BknPow(x, alpha1, alpha2, rf, norm, jump, bkg):
    A1 = np.power(10.0, norm)
    A2 = A1 / jump ** 2
    out = np.empty(len(x))
    inreg = np.where(x < rf)
    term1 = IntFunc(x[inreg], rf, alpha1, 0.01 * np.ones(len(x[inreg])), np.sqrt(rf ** 2 - x[inreg] ** 2))
    term2 = IntFunc(x[inreg], rf, alpha2, np.sqrt(rf ** 2 - x[inreg] ** 2), 1000.0 * np.ones(len(x[inreg])))
    out[inreg] = A1 * term1 + A2 * term2
    outreg = np.where(x >= rf)
    term = IntFunc(x[outreg], rf, alpha2, 0.01 * np.ones(len(x[outreg])), 1000.0 * np.ones(len(x[outreg])))
    out[outreg] = A2 * term
    c2 = np.power(10.0, bkg)
    return out + c2


class Model:

    def __init__(self, model, vals=None):
        self.model = model
        if vals is not None:
            self.params = vals
        else:
            self.params = None

    def SetParameters(self, vals):
        self.params = vals

    def SetErrors(self, vals):
        self.errors = vals