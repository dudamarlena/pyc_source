# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\elements\elem1d.py
# Compiled at: 2017-04-12 19:32:03
# Size of source mod 2**32: 777 bytes
from mapy.model.elements import Elements

class Elem1D(Elements):
    __doc__ = 'Elem1D include methods and attributes for all one dimensional \n    elements.\n    '

    def __init__(self):
        Elements.__init__(self)

    def rebuild(self):
        Elements.rebuild(self)
        self.grids = []
        g1 = self.model.griddict[int(self.g1)]
        g2 = self.model.griddict[int(self.g2)]
        self.grids = [g1, g2]
        self.calc_xvec()
        self.L = self.grids[0].distfrom(self.grids[1])

    def calc_xvec(self):
        g1 = self.grids[0]
        g2 = self.grids[1]
        self.xvec = g2 - g1

    def calc_vecs(self):
        self.zvec = self.xvec.cross(self.ovec)
        self.yvec = self.zvec.cross(self.xvec)