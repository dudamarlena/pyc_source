# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\math\Vector4.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 4309 bytes


class Vector4:
    X: float
    Y: float
    Z: float
    W: float

    def __init__(self, *args):
        if len(args) == 4:
            self.X = args[0]
            self.Y = args[1]
            self.Z = args[2]
            self.W = args[3]
        elif len(args) == 2:
            self.X = args[0].X
            self.Y = args[0].Y
            self.Z = args[0].Z
            self.W = args[1]