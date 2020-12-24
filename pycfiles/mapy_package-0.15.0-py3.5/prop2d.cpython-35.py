# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\properties\prop2d.py
# Compiled at: 2017-04-12 19:32:03
# Size of source mod 2**32: 808 bytes
from mapy.reader import user_setattr
from mapy.model.properties import Properties

class Prop2D(Properties):

    def __init__(self):
        super(Prop2D, self).__init__()


class PropShell(Prop2D):

    def __init__(self, inputs):
        super(PropShell, self).__init__()
        self = user_setattr(self, inputs)

    def build_C(self):
        import scipy
        Emat = self.matobj.e
        if self.matobj.nu:
            Gmat = Emat / (2.0 * (1 + self.matobj.nu))
        else:
            Gmat = self.matobj.g
            self.matobj.nu = Emat / Gmat / 2.0 - 1
        nu = self.matobj.nu
        self.C = Emat / (1 - nu ** 2) * scipy.array([
         [
          1, nu, 0],
         [
          nu, 1, 0],
         [
          0, 0, (1 - nu) / 2]])