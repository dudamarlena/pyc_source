# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/Point.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4434 bytes
__doc__ = '\nPoint.py -  Extension of QPointF which adds a few missing methods.\nCopyright 2010  Luke Campagnola\nDistributed under MIT/X11 license. See license.txt for more infomation.\n'
from .Qt import QtCore
import numpy as np

def clip(x, mn, mx):
    if x > mx:
        return mx
    if x < mn:
        return mn
    return x


class Point(QtCore.QPointF):
    """Point"""

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], QtCore.QSizeF):
                QtCore.QPointF.__init__(self, float(args[0].width()), float(args[0].height()))
                return
            if isinstance(args[0], float) or isinstance(args[0], int):
                QtCore.QPointF.__init__(self, float(args[0]), float(args[0]))
                return
            if hasattr(args[0], '__getitem__'):
                QtCore.QPointF.__init__(self, float(args[0][0]), float(args[0][1]))
                return
        elif len(args) == 2:
            QtCore.QPointF.__init__(self, args[0], args[1])
            return
        (QtCore.QPointF.__init__)(self, *args)

    def __len__(self):
        return 2

    def __reduce__(self):
        return (
         Point, (self.x(), self.y()))

    def __getitem__(self, i):
        if i == 0:
            return self.x()
        if i == 1:
            return self.y()
        raise IndexError('Point has no index %s' % str(i))

    def __setitem__(self, i, x):
        if i == 0:
            return self.setX(x)
        if i == 1:
            return self.setY(x)
        raise IndexError('Point has no index %s' % str(i))

    def __radd__(self, a):
        return self._math_('__radd__', a)

    def __add__(self, a):
        return self._math_('__add__', a)

    def __rsub__(self, a):
        return self._math_('__rsub__', a)

    def __sub__(self, a):
        return self._math_('__sub__', a)

    def __rmul__(self, a):
        return self._math_('__rmul__', a)

    def __mul__(self, a):
        return self._math_('__mul__', a)

    def __rdiv__(self, a):
        return self._math_('__rdiv__', a)

    def __div__(self, a):
        return self._math_('__div__', a)

    def __truediv__(self, a):
        return self._math_('__truediv__', a)

    def __rtruediv__(self, a):
        return self._math_('__rtruediv__', a)

    def __rpow__(self, a):
        return self._math_('__rpow__', a)

    def __pow__(self, a):
        return self._math_('__pow__', a)

    def _math_(self, op, x):
        x = Point(x)
        return Point(getattr(self[0], op)(x[0]), getattr(self[1], op)(x[1]))

    def length(self):
        """Returns the vector length of this Point."""
        return (self[0] ** 2 + self[1] ** 2) ** 0.5

    def norm(self):
        """Returns a vector in the same direction with unit length."""
        return self / self.length()

    def angle(self, a):
        """Returns the angle in degrees between this vector and the vector a."""
        n1 = self.length()
        n2 = a.length()
        if n1 == 0.0 or n2 == 0.0:
            return
        ang = np.arccos(clip(self.dot(a) / (n1 * n2), -1.0, 1.0))
        c = self.cross(a)
        if c > 0:
            ang *= -1.0
        return ang * 180.0 / np.pi

    def dot(self, a):
        """Returns the dot product of a and this Point."""
        a = Point(a)
        return self[0] * a[0] + self[1] * a[1]

    def cross(self, a):
        a = Point(a)
        return self[0] * a[1] - self[1] * a[0]

    def proj(self, b):
        """Return the projection of this vector onto the vector b"""
        b1 = b / b.length()
        return self.dot(b1) * b1

    def __repr__(self):
        return 'Point(%f, %f)' % (self[0], self[1])

    def min(self):
        return min(self[0], self[1])

    def max(self):
        return max(self[0], self[1])

    def copy(self):
        return Point(self)

    def toQPoint(self):
        return (QtCore.QPoint)(*self)