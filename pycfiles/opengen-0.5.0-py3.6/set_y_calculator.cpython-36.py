# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opengen/builder/set_y_calculator.py
# Compiled at: 2020-05-07 20:26:31
# Size of source mod 2**32: 1351 bytes
from ..constraints.rectangle import Rectangle
from ..constraints.ball_inf import BallInf

class SetYCalculator:
    LARGE_NUM = 1000000000000.0

    def __init__(self, set_c):
        self._SetYCalculator__set_c = set_c

    def __obtain_y_with_c_compact(self):
        return BallInf(None, SetYCalculator.LARGE_NUM)

    def __obtain_y_with_c_rectangle(self):
        c = self._SetYCalculator__set_c
        xmin = c.xmin
        xmax = c.xmax
        if xmin is not None:
            n = len(xmin)
        else:
            if xmax is not None:
                n = len(xmax)
            else:
                raise Exception('Fatal error: both xmin and xmax are None')
            if xmin is None:
                ymin = [
                 0.0] * n
            else:
                ymin = [
                 -SetYCalculator.LARGE_NUM] * n
                for i in range(n):
                    if xmin[i] == float('-inf'):
                        ymin[i] = 0.0

            if xmax is None:
                ymax = [
                 0.0] * n
            else:
                ymax = [
                 SetYCalculator.LARGE_NUM] * n
                for i in range(n):
                    if xmax[i] == float('inf'):
                        ymax[i] = 0.0

        return Rectangle(ymin, ymax)

    def obtain(self):
        if isinstance(self._SetYCalculator__set_c, Rectangle):
            return self._SetYCalculator__obtain_y_with_c_rectangle()
        if self._SetYCalculator__set_c.is_compact():
            return self._SetYCalculator__obtain_y_with_c_compact()
        raise NotImplementedError()