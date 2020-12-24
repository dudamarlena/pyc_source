# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/xyz_axis.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 830 bytes
import numpy as np
from .line import LineVisual

class XYZAxisVisual(LineVisual):
    __doc__ = '\n    Simple 3D axis for indicating coordinate system orientation. Axes are\n    x=red, y=green, z=blue.\n    '

    def __init__(self, **kwargs):
        verts = np.array([[0, 0, 0],
         [
          1, 0, 0],
         [
          0, 0, 0],
         [
          0, 1, 0],
         [
          0, 0, 0],
         [
          0, 0, 1]])
        color = np.array([[1, 0, 0, 1],
         [
          1, 0, 0, 1],
         [
          0, 1, 0, 1],
         [
          0, 1, 0, 1],
         [
          0, 0, 1, 1],
         [
          0, 0, 1, 1]])
        LineVisual.__init__(self, pos=verts, color=color, connect='segments', method='gl', **kwargs)