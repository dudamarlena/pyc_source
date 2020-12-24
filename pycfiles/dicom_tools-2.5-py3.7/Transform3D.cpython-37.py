# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/Transform3D.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1107 bytes
from .Qt import QtCore, QtGui
from . import functions as fn
import numpy as np

class Transform3D(QtGui.QMatrix4x4):
    __doc__ = '\n    Extension of QMatrix4x4 with some helpful methods added.\n    '

    def __init__(self, *args):
        (QtGui.QMatrix4x4.__init__)(self, *args)

    def matrix(self, nd=3):
        if nd == 3:
            return np.array(self.copyDataTo()).reshape(4, 4)
        if nd == 2:
            m = np.array(self.copyDataTo()).reshape(4, 4)
            m[2] = m[3]
            m[:, 2] = m[:, 3]
            return m[:3, :3]
        raise Exception("Argument 'nd' must be 2 or 3")

    def map(self, obj):
        """
        Extends QMatrix4x4.map() to allow mapping (3, ...) arrays of coordinates
        """
        if isinstance(obj, np.ndarray):
            if obj.ndim >= 2:
                if obj.shape[0] in (2, 3):
                    return fn.transformCoordinates(self, obj)
        return QtGui.QMatrix4x4.map(self, obj)

    def inverted(self):
        inv, b = QtGui.QMatrix4x4.inverted(self)
        return (Transform3D(inv), b)