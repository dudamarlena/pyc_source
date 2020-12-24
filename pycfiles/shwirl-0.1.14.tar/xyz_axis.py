# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/visuals/xyz_axis.py
# Compiled at: 2016-11-03 01:40:19
import numpy as np
from .line import LineVisual

class XYZAxisVisual(LineVisual):
    """
    Simple 3D axis for indicating coordinate system orientation. Axes are
    x=red, y=green, z=blue.
    """

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