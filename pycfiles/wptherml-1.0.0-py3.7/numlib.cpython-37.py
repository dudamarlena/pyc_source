# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wptherml/numlib/numlib.py
# Compiled at: 2019-07-23 16:27:58
# Size of source mod 2**32: 853 bytes


def Integrate(y, x, a, b):
    som = 0.0
    keep = 1
    idx = 0
    if x[(len(x) - 1)] - x[0] < 0:
        xnew = x[::-1]
        x = xnew
        ynew = y[::-1]
        y = ynew
    for i in range(0, len(x)):
        if x[i] > b:
            break

    return som