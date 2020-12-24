# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\materials\matlamina.py
# Compiled at: 2017-04-20 23:14:08
# Size of source mod 2**32: 9804 bytes
import numpy as np
from mapy.model.materials import Materials
from mapy.reader import user_setattr
from mapy.constants import ZER, FLOAT

class MatLamina(Materials):
    __doc__ = '\n    Defines a lamina material.\n\n    Attributes:\n    ____________________________________________________________________________\n    card       the card name (NASTRAN etc)\n    entryclass path to the class name\n    id         material id\n    e1         Young Modulus in direction 1\n    e2         Young Modulus in direction 2\n    g12        in-plane shear modulus\n    g13        transverse shear modulus for plane 1-Z\n    g23        transverse shear modulus for plane 2-Z\n    nu12       Poisson\'s ratio 12\n    nu13       Poisson\'s ratio 13\n    nu23       Poisson\'s ratio 23\n    nu21       Poisson\'s ratio 21: use formula nu12/e1 = nu21/e2\n    nu31       Poisson\'s ratio 31: use formula nu31/e3 = nu13/e1\n    nu32       Poisson\'s ratio 32: use formula nu23/e2 = nu32/e3\n    rho        especific mass (mass / volume)\n    a1         thermal expansion coeffiecient in direction 1\n    a2         thermal expansion coeffiecient in direction 2\n    a3         thermal expansion coeffiecient in direction 3\n    tref       reference temperature\n    damp       structural damping coefficient\n    st1,st2    allowable tensile stresses for directions 1 and 2\n    sc1,sc2    allowable compressive stresses for directions 1 and 2\n    ss12       allowable in-plane stress for shear\n    strn       allowable strain for direction 1\n    q11        lamina constitutive constant 11\n    q12        lamina constitutive constant 12\n    q13        lamina constitutive constant 13\n    q21        lamina constitutive constant 21\n    q22        lamina constitutive constant 22\n    q23        lamina constitutive constant 23\n    q31        lamina constitutive constant 31\n    q32        lamina constitutive constant 32\n    q33        lamina constitutive constant 33\n    q44        lamina constitutive constant 44\n    q55        lamina constitutive constant 55\n    q66        lamina constitutive constant 66\n    u          matrix with lamina invariants\n    c          matrix with lamina stiffness coefficients\n    ____________________________________________________________________________\n\n    Note: when the user defines "nu" and "g", the "g" will be recaculated\n          based on equation: e = 2*(1+nu)*g\n    ____________________________________________________________________________\n    '
    __slots__ = ['card', 'entryclass', 'id',
     'e1', 'e2', 'e3', 'g12', 'g13', 'g23',
     'nu12', 'nu13', 'nu21', 'nu23', 'nu31', 'nu32', 'rho',
     'a1', 'a2', 'a3', 'tref', 'damp', 'st1', 'st2', 'sc1', 'sc2',
     'ss12', 'strn',
     'q11', 'q12', 'q13', 'q21', 'q22', 'q23', 'q31', 'q32', 'q33',
     'q44', 'q55', 'q66', 'u', 'c']

    def __init__(self):
        super(MatLamina, self).__init__()
        self.id = None
        self.e1 = None
        self.e2 = None
        self.e3 = ZER
        self.g12 = None
        self.g13 = None
        self.g23 = None
        self.nu12 = None
        self.nu13 = ZER
        self.nu21 = None
        self.nu23 = ZER
        self.nu31 = ZER
        self.nu32 = ZER
        self.rho = None
        self.a1 = None
        self.a2 = None
        self.a3 = None
        self.tref = None
        self.damp = None
        self.st1 = None
        self.st2 = None
        self.sc1 = None
        self.sc2 = None
        self.ss12 = None
        self.strn = None
        self.q11 = None
        self.q12 = None
        self.q13 = None
        self.q21 = None
        self.q22 = None
        self.q23 = None
        self.q31 = None
        self.q32 = None
        self.q33 = None
        self.q44 = None
        self.q55 = None
        self.q66 = None
        self.u = None

    def rebuild(self):
        e1 = self.e1
        e2 = self.e2
        e3 = self.e3
        nu12 = self.nu12
        nu21 = self.nu21
        nu13 = self.nu13
        nu31 = self.nu31
        nu23 = self.nu23
        nu32 = self.nu32
        delta = (1 - nu12 * nu21 - nu23 * nu32 - nu31 * nu13 - 2 * nu21 * nu32 * nu13) / (e1 * e2)
        c11 = (1 - nu23 * nu23) / (delta * e2)
        c12 = (nu21 + nu31 * nu23) / (delta * e2)
        c13 = (nu31 + nu21 * nu32) / (delta * e2)
        c22 = (1 - nu13 * nu31) / (delta * e1)
        c23 = (nu32 + nu12 * nu31) / (delta * e1)
        c33 = e3 * (1 - nu12 * nu21) / (delta * e1 * e2)
        c44 = self.g23
        c55 = self.g13
        c66 = self.g12
        self.c = np.array([
         [
          c11, c12, c13, ZER, ZER, ZER],
         [
          c12, c22, c23, ZER, ZER, ZER],
         [
          c13, c23, c33, ZER, ZER, ZER],
         [
          ZER, ZER, ZER, c44, ZER, ZER],
         [
          ZER, ZER, ZER, ZER, c55, ZER],
         [
          ZER, ZER, ZER, ZER, ZER, c66]], dtype=FLOAT)
        self.c = np.array([
         [
          c11, c12, c13, ZER, ZER, ZER],
         [
          c12, c22, c23, ZER, ZER, ZER],
         [
          c13, c23, c33, ZER, ZER, ZER],
         [
          ZER, ZER, ZER, c44, ZER, ZER],
         [
          ZER, ZER, ZER, ZER, c55, ZER],
         [
          ZER, ZER, ZER, ZER, ZER, c66]], dtype=FLOAT)
        den = 1 - self.nu12 * self.nu21 - self.nu13 * self.nu31 - self.nu23 * self.nu32 - self.nu12 * self.nu23 * self.nu31 - self.nu13 * self.nu21 * self.nu32
        den = np.array(den, dtype=FLOAT)
        self.q11 = self.e1 * (1 - self.nu23 * self.nu32) / den
        self.q12 = self.e1 * (self.nu21 + self.nu23 * self.nu31) / den
        self.q13 = self.e1 * (self.nu31 + self.nu21 * self.nu32) / den
        self.q21 = self.e2 * (self.nu12 + self.nu13 * self.nu32) / den
        self.q22 = self.e2 * (1 - self.nu13 * self.nu31) / den
        self.q23 = self.e2 * (self.nu32 + self.nu12 * self.nu31) / den
        self.q31 = self.e3 * (self.nu13 + self.nu12 * self.nu32) / den
        self.q32 = self.e3 * (self.nu23 + self.nu13 * self.nu21) / den
        self.q33 = self.e3 * (1 - self.nu12 * self.nu21) / den
        self.q44 = self.g12
        self.q55 = self.g23
        self.q66 = self.g13
        u1 = (3 * self.q11 + 3 * self.q22 + 2 * self.q12 + 4 * self.q44) / 8
        u2 = (self.q11 - self.q22) / 2
        u3 = (self.q11 + self.q22 - 2 * self.q12 - 4 * self.q44) / 8
        u4 = (self.q11 + self.q22 + 6 * self.q12 - 4 * self.q44) / 8
        u5 = (u1 - u4) / 2
        u6 = (self.q55 + self.q66) / 2
        u7 = (self.q55 - self.q66) / 2
        self.u = np.array([
         [
          u1, u2, ZER, u3, ZER],
         [
          u1, -u2, ZER, u3, ZER],
         [
          u4, ZER, ZER, -u3, ZER],
         [
          u6, u7, ZER, ZER, ZER],
         [
          u6, -u7, ZER, ZER, ZER],
         [
          ZER, ZER, -u7, ZER, ZER],
         [
          u5, ZER, ZER, -u3, ZER],
         [
          ZER, ZER, u2 / 2, ZER, u3],
         [
          ZER, ZER, u2 / 2, ZER, -u3]], dtype=FLOAT)

    def read_inputs(self, inputs={}):
        if len(inputs) > 0:
            self = user_setattr(self, inputs)
        if not self.nu21:
            nu21 = np.array(self.nu12 * self.e2 / self.e1, dtype=FLOAT)
            self.nu21 = nu21
        if not self.nu12:
            nu12 = np.array(self.nu21 * self.e1 / self.e2, dtype=FLOAT)
            self.nu12 = nu12


def read_laminaprop(laminaprop=None, rebuild=True):
    matlam = MatLamina()
    if laminaprop == None:
        print('ERROR - laminaprop must be a tuple in the following format:')
        print('        (e1, e2, nu12, g12, g13, g23, e3, nu13, nu23)')
    if len(laminaprop) == 3:
        e = laminaprop[0]
        nu = laminaprop[2]
        g = e / (2 * (1 + nu))
        laminaprop = (e, e, nu, g, g, g, e, nu, nu)
    nu12 = laminaprop[2]
    if len(laminaprop) < 9:
        e2 = laminaprop[1]
        laminaprop = tuple(list(laminaprop)[:6] + [e2, nu12, nu12])
    matlam.e1 = laminaprop[0]
    matlam.e2 = laminaprop[1]
    matlam.e3 = laminaprop[6]
    matlam.nu12 = laminaprop[2]
    matlam.nu13 = laminaprop[7]
    matlam.nu23 = laminaprop[8]
    matlam.nu21 = matlam.nu12 * matlam.e2 / matlam.e1
    matlam.nu31 = matlam.nu13 * matlam.e3 / matlam.e1
    matlam.nu32 = matlam.nu23 * matlam.e3 / matlam.e2
    matlam.g12 = laminaprop[3]
    matlam.g13 = laminaprop[4]
    matlam.g23 = laminaprop[5]
    if rebuild:
        matlam.rebuild()
    return matlam