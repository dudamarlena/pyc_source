# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\math\Vector3.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 3550 bytes
from math import sqrt

class Vector3:
    X: float
    Y: float
    Z: float

    def __init__(self, *args):
        if len(args) == 3 or len(args) == 1 and isinstance(args[0], (tuple, list)):
            self.X, self.Y, self.Z = args
        elif len(args) == 1:
            self.__dict__ = args[0].__dict__

    def length(self) -> float:
        return sqrt(self.X ** 2 + self.Y ** 2 + self.Z ** 2)

    def normalize(self):
        length = self.length()
        invNorm = 1.0 / length
        self.X *= invNorm
        self.Y *= invNorm
        self.Z *= invNorm