# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/tensor.py
# Compiled at: 2016-11-29 20:56:28
"""

Read-only/writable TensorData classes.

Kisuk Lee <kisuklee@mit.edu>, 2015-2016
"""
import math, numpy as np
from box import *
from vector import *

class TensorData(object):
    """Read-only tensor data.

    The 1st dimension is regarded as parallel channels, and arbitrary access
    along this dimension is not allowed. Threfore, every data access should be
    made through 3D vector, not 4D.

    Attributes:
        _data:   numpy 4D array (channel,z,y,x)
        _dim:    Dimension of each channel
        _offset: Coordinate offset from the origin
        _bb:     Bounding box
        _fov:    Patch size
        _rg:     Range (update dep.: dim, offset, fov)
    """

    def __init__(self, data, fov=(0, 0, 0), offset=(0, 0, 0)):
        """
        Initialize a TensorData object.
        """
        self._data = self._check_data(data)
        self._dim = Vec3d(self._data.shape[1:])
        self._offset = Vec3d(offset)
        self._bb = Box((0, 0, 0), self._dim)
        self._bb.translate(self._offset)
        self.set_fov(fov)

    def set_fov(self, fov):
        """
        Set a nonnegative field of view (FoV), i.e., patch size.
        """
        fov = Vec3d(fov)
        if fov == (0, 0, 0):
            fov = Vec3d(self._dim)
        assert fov == minimum(maximum(fov, (0, 0, 0)), self._dim)
        self._fov = fov
        self._set_range()

    def get_patch(self, pos):
        """
        Extract a patch of size _fov centered on pos.
        """
        assert self._rg.contains(pos)
        loc = pos - self._offset
        box = centered_box(loc, self._fov)
        vmin = box.min()
        vmax = box.max()
        return np.copy(self._data[:, vmin[0]:vmax[0],
         vmin[1]:vmax[1],
         vmin[2]:vmax[2]])

    def get_data(self):
        return self._data

    def shape(self):
        """Return data shape (c,z,y,x)."""
        return self._data.shape

    def dim(self):
        """Return channel shape (z,y,x)."""
        return Vec3d(self._dim)

    def fov(self):
        return Vec3d(self._fov)

    def offset(self):
        return Vec3d(self._offset)

    def bounding_box(self):
        return Box(self._bb)

    def range(self):
        return Box(self._rg)

    def _check_data(self, data):
        assert isinstance(data, np.ndarray)
        assert data.ndim == 3 or data.ndim == 4
        if data.ndim == 3:
            data = data[(np.newaxis, ...)]
        return data

    def _set_range(self):
        """Set a valid range for extracting patches."""
        top = self._fov / 2
        btm = self._fov - top - (1, 1, 1)
        vmin = self._offset + top
        vmax = self._offset + self._dim - btm
        self._rg = Box(vmin, vmax)

    def __str__(self):
        return '<TensorData>\nshape: %s\ndim: %s\nFoV: %s\noffset: %s\n' % (
         self.shape(), self._dim, self._fov, self._offset)


class WritableTensorData(TensorData):
    """
    Writable tensor data.
    """

    def __init__(self, data_or_shape, fov=(0, 0, 0), offset=(0, 0, 0)):
        """
        Initialize a writable tensor data, or create a new tensor of zeros.
        """
        if isinstance(data_or_shape, np.ndarray):
            TensorData.__init__(self, data_or_shape, fov, offset)
        else:
            data = np.zeros(data_or_shape, dtype='float32')
            TensorData.__init__(self, data, fov, offset)

    def set_patch(self, pos, patch, op=None):
        """
        Write a patch of size _fov centered on pos.
        """
        assert self._rg.contains(pos)
        patch = self._check_data(patch)
        dim = patch.shape[1:]
        assert dim == self._fov
        box = centered_box(pos, dim)
        box.translate(-self._offset)
        vmin = box.min()
        vmax = box.max()
        lval = 'self._data[:,vmin[0]:vmax[0],vmin[1]:vmax[1],vmin[2]:vmax[2]]'
        rval = 'patch'
        if op is None:
            exec ('{}={}').format(lval, rval)
        else:
            exec ('{}={}({},{})').format(lval, op, lval, rval)
        return


class WritableTensorDataWithMask(WritableTensorData):
    """
    Writable tensor data with blending mask.
    """

    def __init__(self, data_or_shape, fov=(0, 0, 0), offset=(0, 0, 0)):
        """
        Initialize a writable tensor data, or create a new tensor of zeros.
        """
        WritableTensorData.__init__(self, data_or_shape, fov, offset)
        self._norm = WritableTensorData(self.shape(), fov, offset)

    def set_patch(self, pos, patch, op='np.add', mask=None):
        """
        Write a patch of size _fov centered on pos.
        """
        if mask is None:
            mask = np.ones(patch.shape, dtype='float32')
        WritableTensorData.set_patch(self, pos, mask * patch, op)
        self._norm.set_patch(pos, mask, op='np.add')
        return

    def get_norm(self):
        return self._norm._data

    def get_data(self):
        self._data = np.divide(self._data, self._norm._data, self._data)
        return self._data

    def get_unnormalized_data(self):
        return WritableTensorData.get_data(self)


if __name__ == '__main__':
    import unittest

    class UnitTestTensorData(unittest.TestCase):

        def setup(self):
            pass

        def testCreation(self):
            data = np.zeros((4, 4, 4, 4))
            T = TensorData(data, (3, 3, 3), (1, 1, 1))
            self.assertTrue(T.shape() == (4, 4, 4, 4))
            self.assertTrue(T.offset() == (1, 1, 1))
            self.assertTrue(T.fov() == (3, 3, 3))
            bb = T.bounding_box()
            rg = T.range()
            self.assertTrue(bb == Box((1, 1, 1), (5, 5, 5)))
            self.assertTrue(rg == Box((2, 2, 2), (4, 4, 4)))

        def testGetPatch(self):
            data = np.random.rand(4, 4, 4)
            T = TensorData(data, (3, 3, 3))
            p = T.get_patch((2, 2, 2))
            self.assertTrue(np.array_equal(data[1:, 1:, 1:], p[(0, Ellipsis)]))
            T.set_fov((2, 2, 2))
            p = T.get_patch((2, 2, 2))
            self.assertTrue(np.array_equal(data[1:3, 1:3, 1:3], p[(0, Ellipsis)]))


    class UnitTestWritableTensorData(unittest.TestCase):

        def setup(self):
            pass

        def testCreation(self):
            data = np.zeros((1, 4, 4, 4))
            T = WritableTensorData(data, (3, 3, 3), (1, 1, 1))
            self.assertTrue(T.shape() == (1, 4, 4, 4))
            self.assertTrue(T.offset() == (1, 1, 1))
            self.assertTrue(T.fov() == (3, 3, 3))
            bb = T.bounding_box()
            rg = T.range()
            self.assertTrue(bb == Box((1, 1, 1), (5, 5, 5)))
            self.assertTrue(rg == Box((2, 2, 2), (4, 4, 4)))

        def testSetPatch(self):
            T = WritableTensorData(np.zeros((1, 5, 5, 5)), (3, 3, 3), (1, 1, 1))
            p = np.random.rand(1, 3, 3, 3)
            self.assertFalse(np.array_equal(p, T.get_patch((4, 4, 4))))
            T.set_patch((4, 4, 4), p)
            self.assertTrue(np.array_equal(p, T.get_patch((4, 4, 4))))


    unittest.main()