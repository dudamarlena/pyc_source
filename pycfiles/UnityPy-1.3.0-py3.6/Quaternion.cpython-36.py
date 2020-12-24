# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\math\Quaternion.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 2732 bytes


class Quaternion:
    X: float
    Y: float
    Z: float
    W: float

    def __init__(self, x: float, y: float, z: float, w: float):
        self.X = x
        self.Y = y
        self.Z = z
        self.W = w