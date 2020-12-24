# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/Vector.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2927 bytes
"""
Vector.py -  Extension of QVector3D which adds a few missing methods.
Copyright 2010  Luke Campagnola
Distributed under MIT/X11 license. See license.txt for more infomation.
"""
from .Qt import QtGui, QtCore, USE_PYSIDE
import numpy as np

class Vector(QtGui.QVector3D):
    __doc__ = 'Extension of QVector3D which adds a few helpful methods.'

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], QtCore.QSizeF):
                QtGui.QVector3D.__init__(self, float(args[0].width()), float(args[0].height()), 0)
                return
                if isinstance(args[0], QtCore.QPoint) or isinstance(args[0], QtCore.QPointF):
                    QtGui.QVector3D.__init__(self, float(args[0].x()), float(args[0].y()), 0)
            elif hasattr(args[0], '__getitem__'):
                vals = list(args[0])
                if len(vals) == 2:
                    vals.append(0)
                if len(vals) != 3:
                    raise Exception('Cannot init Vector with sequence of length %d' % len(args[0]))
                (QtGui.QVector3D.__init__)(self, *vals)
                return
        else:
            if len(args) == 2:
                QtGui.QVector3D.__init__(self, args[0], args[1], 0)
                return
            (QtGui.QVector3D.__init__)(self, *args)

    def __len__(self):
        return 3

    def __add__(self, b):
        if USE_PYSIDE:
            if isinstance(b, QtGui.QVector3D):
                b = Vector(b)
        return QtGui.QVector3D.__add__(self, b)

    def __getitem__(self, i):
        if i == 0:
            return self.x()
        if i == 1:
            return self.y()
        if i == 2:
            return self.z()
        raise IndexError('Point has no index %s' % str(i))

    def __setitem__(self, i, x):
        if i == 0:
            return self.setX(x)
        if i == 1:
            return self.setY(x)
        if i == 2:
            return self.setZ(x)
        raise IndexError('Point has no index %s' % str(i))

    def __iter__(self):
        yield self.x()
        yield self.y()
        yield self.z()

    def angle(self, a):
        """Returns the angle in degrees between this vector and the vector a."""
        n1 = self.length()
        n2 = a.length()
        if n1 == 0.0 or n2 == 0.0:
            return
        ang = np.arccos(np.clip(QtGui.QVector3D.dotProduct(self, a) / (n1 * n2), -1.0, 1.0))
        return ang * 180.0 / np.pi

    def __abs__(self):
        return Vector(abs(self.x()), abs(self.y()), abs(self.z()))