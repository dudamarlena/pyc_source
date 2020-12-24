# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\properties\prop1d.py
# Compiled at: 2017-04-12 19:32:03
# Size of source mod 2**32: 1122 bytes
from mapy.reader import user_setattr
from mapy.model.properties import Properties

class Prop1D(Properties):

    def __init__(self):
        super(Prop1D, self).__init__()


class PropRod(Prop1D):

    def __init__(self, inputs):
        super(PropRod, self).__init__()
        self = user_setattr(self, inputs)

    def build_C(self):
        pass


class PropBar(Prop1D):

    def __init__(self, inputs):
        super(PropBar, self).__init__()
        self = user_setattr(self, inputs)

    def build_C(self):
        import numpy
        nu = self.matobj.nu
        Emat = self.matobj.e
        A = self.a
        if nu:
            Gmat = Emat / (2.0 * (1 + nu))
        else:
            Gmat = self.matobj.g
            self.matobj.nu = Emat / Gmat / 2.0 - 1
        self.G = Gmat
        kxy = 0.8333333333333334
        kxz = 0.8333333333333334
        GA = Gmat * A
        self.C = A * numpy.array([
         [
          Emat, 0, 0],
         [
          0, GA * kxy, 0],
         [
          0, 0, GA * kxz]])