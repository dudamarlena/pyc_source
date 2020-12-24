# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Utilities/Symmetry.py
# Compiled at: 2019-02-16 11:53:59
# Size of source mod 2**32: 1906 bytes
"""
This modules provides methods to perform symmetry operations on a pdbparser instance atoms.

.. inheritance-diagram:: pdbparser.Utilities.Symmetry
    :parts: 2
"""
from __future__ import print_function
import numpy as np
from pdbparser.Utilities.Geometry import *
from pdbparser.Utilities.Information import *
from pdbparser.Utilities.Collection import get_orthonormal_axes

def inverte(indexes, pdb, vector, inversionCenter=None):
    if inversionCenter is None:
        multiply(indexes, pdb, [-1, -1, -1])
    else:
        translate(indexes, pdb, -1 * np.array(inversionCenter))
        multiply(indexes, pdb, [-1, -1, -1])
        translate(indexes, pdb, np.array(inversionCenter))


def mirror(indexes, pdb, plane=None, origin=None):
    if plane is None:
        plane = [
         [
          1, 0, 0], [0, 1, 0]]
    else:
        assert isinstance(plane, (list, tuple))
        plane = list(plane)
        assert len(plane) == 2
        plane = [np.array(item) for item in plane]
        assert plane[0].shape in ((3,), (3, 1))
        if not plane[1].shape in ((3,), (3, 1)):
            raise AssertionError
        elif origin is None:
            origin = np.array([0, 0, 0])
        else:
            assert isinstance(origin, (list, tuple, np.ndarray))
            origin = np.array(origin)
            assert origin.shape in ((3,), (3, 1))
        axes = get_orthonormal_axes((plane[0]), (plane[1]), force=False)
        axes = np.array(axes)
        inversedAxes = np.linalg.inv(axes)
        translate(indexes, pdb, -1.0 * origin)
        rotate(indexes, pdb, inversedAxes)
        multiply(indexes, pdb, [1, 1, -1])
        rotate(indexes, pdb, axes)
        return pdb