# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/rk5.py
# Compiled at: 2019-01-07 12:53:21
# Size of source mod 2**32: 3554 bytes
import numpy as np
from .State import State
c2, c3, c4, c5, c6, c7 = (0.2, 0.3, 0.8, 0.8888888888888888, 1.0, 1.0)
b1, b2, b3, b4, b5, b6, b7 = (0.09114583333333333, 0.0, 0.44923629829290207, 0.6510416666666666,
                              -0.322376179245283, 0.13095238095238096, 0.0)
b1s, b2s, b3s, b4s, b5s, b6s, b7s = (0.08991319444444444, 0.0, 0.4534890685834082,
                                     0.6140625, -0.2715123820754717, 0.08904761904761904,
                                     0.025)
b1d, b2d, b3d, b4d, b5d, b6d, b7d = (
 b1 - b1s, b2 - b2s, b3 - b3s, b4 - b4s,
 b5 - b5s, b6 - b6s, b7 - b7s)
a21 = 0.2
a31, a32 = (0.075, 0.225)
a41, a42, a43 = (0.9777777777777777, -3.7333333333333334, 3.5555555555555554)
a51, a52, a53, a54 = (2.9525986892242035, -11.595793324188385, 9.822892851699436, -0.2908093278463649)
a61, a62, a63, a64, a65 = (2.8462752525252526, -10.757575757575758, 8.906422717743473,
                           0.2784090909090909, -0.2735313036020583)
a71, a72, a73, a74, a75, a76 = (
 b1, b2, b3, b4, b5, b6)

def rk5(t1, x1, v1, f1, h, output):
    """ Perform a single rk5 step """
    f1 = np.log(f1)
    a1, i1 = State(t1, x1, v1, output)
    t2 = t1 - c2 * h
    x2 = x1 + h * a21 * v1
    v2 = v1 + h * a21 * a1
    f2 = f1 - h * a21 * i1
    a2, i2 = State(t2, x2, v2, output)
    t3 = t1 - c3 * h
    x3 = x1 + h * (a31 * v1 + a32 * v2)
    v3 = v1 + h * (a31 * a1 + a32 * a2)
    f3 = f1 - h * (a31 * i1 + a32 * i2)
    a3, i3 = State(t3, x3, v3, output)
    t4 = t1 - c4 * h
    x4 = x1 + h * (a41 * v1 + a42 * v2 + a43 * v3)
    v4 = v1 + h * (a41 * a1 + a42 * a2 + a43 * a3)
    f4 = f1 - h * (a41 * i1 + a42 * i2 + a43 * i3)
    a4, i4 = State(t4, x4, v4, output)
    t5 = t1 - c5 * h
    x5 = x1 + h * (a51 * v1 + a52 * v2 + a53 * v3 + a54 * v4)
    v5 = v1 + h * (a51 * a1 + a52 * a2 + a53 * a3 + a54 * a4)
    f5 = f1 - h * (a51 * i1 + a52 * i2 + a53 * i3 + a54 * i4)
    a5, i5 = State(t5, x5, v5, output)
    t6 = t1 - c6 * h
    x6 = x1 + h * (a61 * v1 + a62 * v2 + a63 * v3 + a64 * v4 + a65 * v5)
    v6 = v1 + h * (a61 * a1 + a62 * a2 + a63 * a3 + a64 * a4 + a65 * a5)
    f6 = f1 - h * (a61 * i1 + a62 * i2 + a63 * i3 + a64 * i4 + a65 * i5)
    a6, i6 = State(t6, x6, v6, output)
    t7 = t1 - c7 * h
    x7 = x1 + h * (a71 * v1 + a72 * v2 + a73 * v3 + a74 * v4 + a75 * v5 + a76 * v6)
    v7 = v1 + h * (a71 * a1 + a72 * a2 + a73 * a3 + a74 * a4 + a75 * a5 + a76 * a6)
    f7 = f1 - h * (a71 * i1 + a72 * i2 + a73 * i3 + a74 * i4 + a75 * i5 + a76 * i6)
    a7, i7 = State(t7, x7, v7, output)
    deltax = abs(h * (b1d * v1 + b2d * v2 + b3d * v3 + b4d * v4 + b5d * v5 + b6d * v6))
    deltav = abs(h * (b1d * a1 + b2d * a2 + b3d * a3 + b4d * a4 + b5d * a5 + b6d * a6))
    deltaf = abs(h * (b1d * i1 + b2d * i2 + b3d * i3 + b4d * i4 + b5d * i5 + b6d * i6))
    f1 = np.exp(f1)
    f7 = np.exp(f7)
    stuff = (
     t1, x1, v1, f1, a1, i1,
     t2, x2, v2, f2, a2, i2,
     t3, x3, v3, f3, a3, i3,
     t4, x4, v4, f4, a4, i4,
     t5, x5, v5, f5, a5, i5,
     t6, x6, v6, f6, a6, i6,
     t7, x7, v7, f7, a7, i7,
     deltax, deltav, deltaf)
    import pickle
    with open('rk5_py.pkl', 'wb') as (f):
        pickle.dump(stuff, f)
    return (
     t7, x7, v7, f7, deltax, deltav, deltaf)