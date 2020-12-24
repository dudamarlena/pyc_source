# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\alignmentmarker.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 6654 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk

class AlignmentCross(tk.Component):
    __doc__ = ' Cross Cell class, used for alignment\n\n        Args:\n           * **cross_length** (float):  Length of each arm of the cross.\n           * **cross_width** (float): Width of the cross arm\n           * **center** (tuple): Coordinate (x1, y1) of the center of the cross\n\n        Keyword Args:\n           * **small_cross_width** (float): If given, sets the width of the small cross in the center of the big cross.  Defaults to 1/4 the value of cross_width\n           * **layer** (int): Layer to place the marker on.  Defaults to 1\n           * **datatype** (int): Datatype to place the marker on.  Defaults to 0\n\n    '

    def __init__(self, cross_length, cross_width, small_cross_width=None, center=(0, 0), layer=1, datatype=0):
        tk.Component.__init__(self, 'AlignmentCross')
        self.cross_length = cross_length
        self.cross_width = cross_width
        self.small_cross_width = cross_width / 4.0 if small_cross_width == None else small_cross_width
        self.layer = layer
        self.datatype = datatype
        self.port = center
        self.direction = 'EAST'
        self.portlist = {}
        self._AlignmentCross__build_cell()
        self._AlignmentCross__build_ports()
        self._auto_transform_()
        self._hash_cell_(cross_length, cross_width, small_cross_width, layer, datatype)

    def __build_cell(self):
        x0, y0 = (0, 0)
        self.add(gdspy.Rectangle((
         x0 - self.cross_length, y0 - self.cross_width / 2.0),
          (
         x0 - self.cross_width / 2.0, y0 + self.cross_width / 2.0),
          layer=(self.layer),
          datatype=(self.datatype)))
        self.add(gdspy.Rectangle((
         x0 + self.cross_length, y0 - self.cross_width / 2.0),
          (
         x0 + self.cross_width / 2.0, y0 + self.cross_width / 2.0),
          layer=(self.layer),
          datatype=(self.datatype)))
        self.add(gdspy.Rectangle((
         x0 - self.cross_width / 2.0, y0 - self.cross_length),
          (
         x0 + self.cross_width / 2.0, y0 - self.cross_width / 2.0),
          layer=(self.layer),
          datatype=(self.datatype)))
        self.add(gdspy.Rectangle((
         x0 - self.cross_width / 2.0, y0 + self.cross_length),
          (
         x0 + self.cross_width / 2.0, y0 + self.cross_width / 2.0),
          layer=(self.layer),
          datatype=(self.datatype)))
        self.add(gdspy.Rectangle((
         x0 - self.cross_width / 2.0, y0 - self.small_cross_width / 2.0),
          (
         x0 + self.cross_width / 2.0, y0 + self.small_cross_width / 2.0),
          layer=(self.layer),
          datatype=(self.datatype)))
        self.add(gdspy.Rectangle((
         x0 - self.small_cross_width / 2.0, y0 - self.cross_width / 2.0),
          (
         x0 + self.small_cross_width / 2.0, y0 + self.cross_width / 2.0),
          layer=(self.layer),
          datatype=(self.datatype)))

    def __build_ports(self):
        self.portlist['center'] = {'port':(0, 0), 
         'direction':'WEST'}


class AlignmentTarget(tk.Component):
    __doc__ = ' Standard Target Cell class, used for alignment.  Set of concentric circles\n\n        Args:\n           * **diameter** (float):  Total diameter of the target marker\n           * **ring_width** (float): Width of each ring\n\n        Keyword Args:\n           * **num_rings** (float): Number of concentric rings in the target.  Defaults to 10\n           * **center** (tuple): Coordinate (x1, y1) of the center of the cross.  Defaults to (0,0)\n           * **layer** (int): Layer to place the marker on.  Defaults to 1\n           * **datatype** (int): Datatype to place the marker on.  Defaults to 0\n\n    '

    def __init__(self, diameter, ring_width, num_rings=10, center=(0, 0), layer=1, datatype=0):
        tk.Component.__init__(self, 'AlignmentTarget', locals())
        self.diameter = diameter
        self.ring_width = ring_width
        self.num_rings = num_rings
        self.layer = layer
        self.datatype = datatype
        self.port = center
        self.direction = 'EAST'
        self.portlist = {}
        self.build_cell()
        self._AlignmentTarget__build_ports()
        self._auto_transform_()

    def build_cell(self):
        x0, y0 = (0, 0)
        spacing = self.diameter / (4.0 * self.num_rings)
        for i in range(self.num_rings):
            self.add(gdspy.Round((
             x0, y0),
              (2 * (i + 1) * spacing),
              (2 * (i + 1) * spacing - self.ring_width),
              layer=(self.layer),
              datatype=(self.datatype),
              number_of_points=0.1))

    def __build_ports(self):
        self.portlist['center'] = {'port':(0, 0), 
         'direction':'WEST'}


if __name__ == '__main__':
    from . import *
    top = gdspy.Cell('top')
    mark1 = AlignmentTarget(200, 3, num_rings=10)
    mark2 = AlignmentTarget(200, 3, num_rings=11, center=(200, 300))
    tk.add(top, mark1)
    tk.add(top, mark2)
    gdspy.LayoutViewer()