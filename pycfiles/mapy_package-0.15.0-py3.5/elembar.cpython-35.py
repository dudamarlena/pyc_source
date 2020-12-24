# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\elements\elembar.py
# Compiled at: 2017-04-20 23:18:48
# Size of source mod 2**32: 5188 bytes
import alg3dpy
from mapy.model.elements.elem1d import Elem1D
from mapy.reader import user_setattr

class ElemBar(Elem1D):

    def __init__(self, inputs):
        Elem1D.__init__(self)
        self = user_setattr(self, inputs)

    def rebuild(self):
        Elem1D.rebuild(self)
        self.calc_ovec()
        self.calc_vecs()
        self.calc_Rmatrix()
        self.build_kelem()

    def calc_ovec(self):
        if self.x2 == '' or self.x3 == '':
            gref = self.model.griddict[int(self.x1)]
            self.ovec = alg3dpy.Vec([gref.x1 - self.grids[0].x1,
             gref.x2 - self.grids[0].x2,
             gref.x3 - self.grids[0].x3])
        else:
            self.ovec = alg3dpy.Vec(self.x1, self.x2, self.x3)

    def test_build_kelem(self):
        return
        import scipy, numpy as np
        x2 = self.L
        C = self.pobj.C
        E = self.pobj.matobj.e
        G = self.pobj.G
        Izz = self.pobj.i1
        Iyy = self.pobj.i2
        kelem = scipy.ones((12, 12))
        pts = [
         0.0]
        for r in pts:
            h1 = (1 - r) / 2.0
            h1r = -0.5
            h2 = (1 + r) / 2.0
            h2r = 0.5
            J = x2 / 2.0
            Bi = 1.0 / J * scipy.array([
             [
              h1r, 0, 0, 0, 0, 0, h2r, 0, 0, 0, 0, 0],
             [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
            kelem += np.dot(np.dot(Bi.transpose(), C), Bi) * J
            Bi = 1.0 / J * scipy.array([[h1r, 0, 0, 0, 0, 0, h2r, 0, 0, 0, 0, 0],
             [
              0, h1r, 0, 0, 0, -h1, 0, h2r, 0, 0, 0, -h2],
             [
              0, 0, h1r, 0, h1, 0, 0, 0, 0, 0, h2, 0]])
            kelem += E * Izz * np.dot(Bi.transpose(), Bi) * J

        print('E', E)
        print('G', G)
        print('Izz', Izz)
        print('Iyy', Iyy)
        self.kelem = kelem * 2.0

    def build_kelem(self):
        import scipy, scipy.sparse as ss
        A = self.A
        E = self.E
        L = self.L
        data1 = scipy.array([E * A / L, -E * A / L, -E * A / L, E * A / L])
        row1 = scipy.array([0, 6, 0, 6])
        col1 = scipy.array([0, 0, 6, 6])
        EI_L = E * self.Izz / self.L
        k1 = 12 * EI_L / L ** 2
        k2 = 6 * EI_L / L
        k3 = 4 * EI_L
        k4 = 2 * EI_L
        data2 = [k1, k2, -k1, k2, k3, -k2, k4, k1, -k2, k3, k2, -k1, -k2, k2, k4, -k2]
        row2 = [1, 1, 1, 1, 5, 5, 5, 7, 7, 11, 5, 7, 7, 11, 11, 11]
        col2 = [1, 5, 7, 11, 5, 7, 11, 7, 11, 11, 1, 1, 5, 1, 5, 7]
        data1.extend(data2)
        row1.extend(row2)
        col1.extend(col2)
        data = scipy.array(data1, dtype='float64')
        row = scipy.array(row1, dtype='int8')
        col = scipy.array(col1, dtype='int8')
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