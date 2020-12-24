# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\elements\elemrod.py
# Compiled at: 2017-04-12 19:32:03
# Size of source mod 2**32: 1478 bytes
from mapy.model.elements.elem1d import Elem1D
from mapy.reader import user_setattr
from mapy.constants import FLOAT, INT

class ElemRod(Elem1D):
    __doc__ = 'Defines a rod element, which is a truss including the axial\n    torsion.\n    '

    def __init__(self, inputs):
        Elem1D.__init__(self)
        self = user_setattr(self, inputs)

    def rebuild(self):
        Elem1D.rebuild(self)
        self.A = self.pobj.a
        self.E = self.pobj.matobj.e
        self.calc_Rmatrix()
        self.build_kelem()

    def build_kelem(self):
        import scipy, scipy.sparse as ss
        A = self.A
        E = self.E
        L = self.L
        eal = E * A / L
        data = scipy.array([eal, -eal, -eal, eal], dtype=FLOAT)
        row = scipy.array([0, 6, 0, 6], dtype=INT)
        col = scipy.array([0, 0, 6, 6], dtype=INT)
        self.kelem = ss.coo_matrix((data, (row, col)), shape=(12, 12))

    def calc_out_vecs(self):
        self.out_vecs = {}
        tmp = {}
        for sub in self.model.subcases.values():
            E = self.E
            A = self.A
            L = self.L
            ub = self.displ[sub.id](6)
            ua = self.displ[sub.id](0)
            tmp['axial_stress'] = (ub - ua) * (E / L)
            tmp['axial_force'] = A * tmp['axial_stress']
            self.out_vecs[sub.id] = tmp