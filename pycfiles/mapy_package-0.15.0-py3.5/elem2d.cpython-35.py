# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\elements\elem2d.py
# Compiled at: 2017-04-20 23:21:09
# Size of source mod 2**32: 1503 bytes
import alg3dpy
from mapy.model.elements import Elements

class Elem2D(Elements):
    __slots__ = [
     'plane']

    def __init__(self):
        super(Elem2D, self).__init__()
        self.xvec = None
        self.yvec = None
        self.zvec = None

    def rebuild(self):
        Elements.rebuild(self)
        self.grids = []
        g1 = self.model.griddict[int(self.g1)]
        g2 = self.model.griddict[int(self.g2)]
        g3 = self.model.griddict[int(self.g3)]
        self.grids = [g1, g2, g3]
        if getattr(self, 'g4', False) is not False:
            g4 = self.model.griddict[int(self.g4)]
            self.grids.append(g4)
            diag1 = g3 - g1
            diag2 = g2 - g4
            self.xvec = diag1 + diag2
        else:
            self.xvec = alg3dpy.vec2points(g1, g2)
        for grid in self.grids:
            grid.elements[self.id] = self

        self.calc_vecs()

    def calc_vecs(self):
        grids = self.grids
        self.plane = alg3dpy.plane3points(grids[0], grids[1], grids[2])
        self.zvec = self.plane.normal
        self.yvec = alg3dpy.ortvec2vecs(self.zvec, self.xvec)