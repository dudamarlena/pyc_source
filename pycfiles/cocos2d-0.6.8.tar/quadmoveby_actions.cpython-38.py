# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../..\cocos\actions\quadmoveby_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 8186 bytes
"""Implementation of QuadMoveBy actions

These actions modifies the x and y coordinates of fixed-size grid of (1,1).
The z-coordinate is not modified.
"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import math
import cocos.director as director
from cocos.euclid import *
from .basegrid_actions import *
__all__ = [
 'QuadMoveBy',
 'MoveCornerUp',
 'MoveCornerDown',
 'CornerSwap',
 'Flip',
 'FlipX',
 'FlipY',
 'SkewHorizontal',
 'SkewVertical']

class QuadMoveBy(Grid3DAction):
    __doc__ = 'QuadMoveBy moves each vertex of the grid. The size of the grid is (1,1)\n\n    Vertex positions::\n\n        vertex3 --<-- vertex2\n            |            |\n            v            ^\n            |            |\n        vertex0 -->-- vertex1\n\n        The vertices will move from the origin (src parameters) a relative distance (delta parameters) in duration time.\n\n    Example::\n\n       scene.do(QuadMoveBy(src0, src1, src2, src3,\n               delta0, delta1, delta2, delta3,\n               duration))\n\n\n       '

    def init(self, src0=(0, 0), src1=(-1, -1), src2=(-1, -1), src3=(-1, -1), delta0=(0, 0), delta1=(0, 0), delta2=(0, 0), delta3=(0, 0), grid=(1, 1), *args, **kw):
        """Initializes the QuadMoveBy

        :Parameters:
            `src0` : (int, int)
                Initial value for the bottom-left coordinate. Default is (0,0)
            `src1` : (int, int)
                Initial value for the bottom-right coordinate. Default is (win_size_x,0)
            `src2` : (int, int)
                Initial value for the upper-right coordinate. Default is (win_size_x, win_size_y)
            `src3` : (int, int)
                Initial value for the upper-left coordinate. Default is (0, win_size_y)
            `delta0` : (int, int)
                The bottom-left relative coordinate. Default is (0,0)
            `delta1` : (int, int)
                The bottom-right relative coordinate. Default is (0,0)
            `delta2` : (int, int)
                The upper-right relative coordinate. Default is (0,0)
            `delta3` : (int, int)
                The upper-left relative coordinate. Default is (0,0)
        """
        if grid != (1, 1):
            raise GridException('Invalid grid size.')
        (super(QuadMoveBy, self).init)(grid, *args, **kw)
        x, y = director.get_window_size()
        if src1 == (-1, -1):
            src1 = (
             x, 0)
        if src2 == (-1, -1):
            src2 = (
             x, y)
        if src3 == (-1, -1):
            src3 = (
             0, y)
        self.src0 = Point3(src0[0], src0[1], 0)
        self.src1 = Point3(src1[0], src1[1], 0)
        self.src2 = Point3(src2[0], src2[1], 0)
        self.src3 = Point3(src3[0], src3[1], 0)
        self.delta0 = Point3(delta0[0], delta0[1], 0)
        self.delta1 = Point3(delta1[0], delta1[1], 0)
        self.delta2 = Point3(delta2[0], delta2[1], 0)
        self.delta3 = Point3(delta3[0], delta3[1], 0)

    def update(self, t):
        new_pos0 = self.src0 + self.delta0 * t
        new_pos1 = self.src1 + self.delta1 * t
        new_pos2 = self.src2 + self.delta2 * t
        new_pos3 = self.src3 + self.delta3 * t
        self.set_vertex(0, 0, new_pos0)
        self.set_vertex(1, 0, new_pos1)
        self.set_vertex(1, 1, new_pos2)
        self.set_vertex(0, 1, new_pos3)


class MoveCornerUp(QuadMoveBy):
    __doc__ = 'MoveCornerUp moves the bottom-right corner to the upper-left corner in duration time'

    def __init__(self, *args, **kw):
        x, y = director.get_window_size()
        (super(MoveCornerUp, self).__init__)(args, delta1=(-x, y), **kw)


class MoveCornerDown(QuadMoveBy):
    __doc__ = 'MoveCornerDown moves the upper-left corner to the bottom-right corner in duration time'

    def __init__(self, *args, **kw):
        x, y = director.get_window_size()
        (super(MoveCornerDown, self).__init__)(args, delta3=(x, -y), **kw)


class CornerSwap(QuadMoveBy):
    __doc__ = 'CornerSwap moves the upper-left corner to the bottom-right corner in vice-versa in duration time.\n    The resulting effect is a reflection + rotation.\n    '

    def __init__(self, *args, **kw):
        x, y = director.get_window_size()
        (super(CornerSwap, self).__init__)(args, delta1=(-x, y), delta3=(x, -y), **kw)


class Flip(QuadMoveBy):
    __doc__ = 'Flip moves the upper-left corner to the bottom-left corner and vice-versa, and\n    moves the upper-right corner to the bottom-left corner and vice-versa, flipping the\n    window upside-down, and right-left.\n    '

    def __init__(self, *args, **kw):
        x, y = director.get_window_size()
        (super(Flip, self).__init__)(args, delta0=(x, y), delta1=(-x, y), delta2=(-x, -y), delta3=(x, -y), **kw)


class FlipX(QuadMoveBy):
    __doc__ = 'FlipX flips the screen horizontally, moving the left corners to the right, and vice-versa.\n    '

    def __init__(self, *args, **kw):
        x, y = director.get_window_size()
        (super(FlipX, self).__init__)(args, delta0=(x, 0), delta1=(-x, 0), delta2=(-x, 0), delta3=(x, 0), **kw)


class FlipY(QuadMoveBy):
    __doc__ = 'FlipY flips the screen vertically, moving the upper corners to the bottom, and vice-versa.\n    '

    def __init__(self, *args, **kw):
        x, y = director.get_window_size()
        (super(FlipY, self).__init__)(args, delta0=(0, y), delta1=(0, y), delta2=(0, -y), delta3=(0, -y), **kw)


class SkewHorizontal(QuadMoveBy):
    __doc__ = 'SkewHorizontal skews the screen horizontally. default skew: x/3'

    def __init__(self, delta=None, *args, **kw):
        x, y = director.get_window_size()
        if delta is None:
            delta = x // 3
        (super(SkewHorizontal, self).__init__)(args, delta1=(-delta, 0), delta3=(delta, 0), **kw)


class SkewVertical(QuadMoveBy):
    __doc__ = 'SkewVertical skews the screen vertically. default skew: y/3'

    def __init__(self, delta=None, *args, **kw):
        x, y = director.get_window_size()
        if delta is None:
            delta = y // 3
        (super(SkewVertical, self).__init__)(args, delta0=(0, delta), delta2=(0, -delta), **kw)