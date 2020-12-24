# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\spiral_old.py
# Compiled at: 2019-10-06 18:45:45
# Size of source mod 2**32: 10305 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk
from picwriter.components.waveguide import Waveguide

class Spiral(gdspy.Cell):
    __doc__ = " Standard Spiral Cell class (subclass of gdspy.Cell).  The desired length of the spiral is first set, along with maximum heights and widths of the bounding box for the spiral.  Then, the exact spiral shape is automatically calculated, or an error is returned if the spiral cannot be generated from the input parameters.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **width** (float): MAX width of the outermost part of the spiral\n           * **height** (float): MAX height of the outermost part of the spiral\n           * **length** (float): desired length of the waveguide\n\n        Keyword Args:\n           * **spacing** (float): distance between parallel waveguides\n           * **parity** (int): If 1 spiral on right side, if -1 spiral on left side (mirror flip)\n           * **port** (tuple): Cartesian coordinate of the input port\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output'] = {'port': (x2, y2), 'direction': 'dir2'}\n\n        Where in the above (x1,y1) are the first elements of the spiral trace, (x2, y2) are the last elements of the spiral trace, and 'dir1', 'dir2' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n    "

    def __init__(self, wgt, width, height, length, spacing=None, parity=1, port=(0, 0), direction='NORTH'):
        gdspy.Cell.__init__(self, tk.getCellName('SpiralOLD'))
        self.portlist = {}
        self.width = width
        self.height = height
        self.length = length
        self.parity = parity
        self.port = port
        self.spacing = 3 * wgt.clad_width if spacing == None else spacing
        self.resist = wgt.resist
        self.wgt = wgt
        self.bend_radius = wgt.bend_radius
        self.direction = direction
        self.build_cell()
        self.build_ports()

    def get_dh(self, corner_dl, n):
        from scipy.optimize import fsolve
        func = lambda h0: self.length - self.spiral_length(h0, corner_dl, n)
        hnew = fsolve(func, self.height)
        return hnew[0]

    def get_number_of_spirals(self, corner_dl):
        nmax = 0
        lengthmin = 0
        for n in range(50):
            n = n + 1
            ml = self.spiral_length(self.height, corner_dl, n)
            print('For spiral with n=' + str(n) + ' loops, minimum length in constrained area is ' + str(ml) + 'um long')
            if n == 1:
                lengthmin = ml
            if self.length <= ml:
                nmax = n
                break

        if nmax == 0:
            raise ValueError('max_length appears to be greater than length.  Either length is too large or program is broken.')
        return (nmax, lengthmin)

    def spiral_length(self, h, corner_dl, n):
        w = self.width
        s = self.spacing
        c = corner_dl
        length = w + 2 * (w - s) + sum([2 * (w - s - 2 * (i + 1) * s) for i in range(n - 1)]) + (w - 2 * n * s)
        length += h + (h - s) + sum([2 * (h - 2 * (i + 1) * s) for i in range(n)]) + (h - s - 2 * n * s)
        length = length - 6 * c - 4 * n * c
        return length

    def build_cell(self):
        width = self.width
        height = self.height
        length = self.length
        bend_radius = self.wgt.bend_radius
        spacing = self.spacing
        corner_dl = 2 * bend_radius - 0.25 * (2 * np.pi * bend_radius)
        n, lengthmin = self.get_number_of_spirals(corner_dl)
        print('Desired length=' + str(length) + ' obtained with n=' + str(n) + ' loops')
        if length < lengthmin:
            raise ValueError('Spiral length is too small for desired spiral width/height.  Please specify either (1) smaller height/width or (2) larger spiral length inputs.')
        else:
            hnew = self.get_dh(corner_dl, n)
            height = hnew
            if self.parity == 1:
                x0, y0 = 0, height / 2.0
            else:
                x0, y0 = 0, height / 2.0
        y0 = y0 - hnew / 2.0
        h, w, s = height, width, spacing
        p = self.parity
        start_points = [
         (
          x0, y0),
         (
          x0, y0 + h - s),
         (
          x0 + p * (w - s), y0 + h - s),
         (
          x0 + p * (w - s), y0 + s)]
        end_points = [
         (
          x0 + p * s, y0 + h - 2 * s),
         (
          x0 + p * s, y0),
         (
          x0 + p * w, y0),
         (
          x0 + p * w, y0 + h),
         (
          x0, y0 + h),
         (
          x0, y0 + h + self.bend_radius)]
        mid_points = []
        x0p, y0p, hp, wp = (
         x0 + p * s, y0 + s, h - 3 * s, w - 2 * s)
        cur_point = (x0p + p * wp, y0p)
        for i in range(int(n - 1)):
            i = i + 1
            if i % 2 == 1:
                cur_point = (
                 cur_point[0] - p * (wp + s - 2 * i * s), cur_point[1])
                mid_points.append(cur_point)
                cur_point = (cur_point[0], cur_point[1] + (hp + s - 2 * i * s))
                mid_points.append(cur_point)
            elif i % 2 == 0:
                cur_point = (
                 cur_point[0] + p * (wp + s - 2 * i * s), cur_point[1])
                mid_points.append(cur_point)
                cur_point = (cur_point[0], cur_point[1] - (hp + s - 2 * i * s))
                mid_points.append(cur_point)

        if n % 2 == 1:
            cur_point = (
             x0p + p * wp / 2.0, cur_point[1])
            mid_points.append(cur_point)
            cur_point = (x0p + p * wp / 2.0, cur_point[1] + (hp - (n - 1) * 2 * s))
            mid_points.append(cur_point)
        else:
            if n % 2 == 0:
                cur_point = (
                 x0p + p * wp / 2.0, cur_point[1])
                mid_points.append(cur_point)
                cur_point = (x0p + p * wp / 2.0, cur_point[1] - (hp - (n - 1) * 2 * s))
                mid_points.append(cur_point)
            cur_point = (x0p, y0p + hp)
            mid_points2 = []
            for i in range(int(n - 1)):
                i = i + 1
                if i % 2 == 1:
                    cur_point = (
                     cur_point[0] + p * (wp + s - 2 * i * s), cur_point[1])
                    mid_points2.append(cur_point)
                    cur_point = (cur_point[0], cur_point[1] - (hp + s - 2 * i * s))
                    mid_points2.append(cur_point)
                elif i % 2 == 0:
                    cur_point = (
                     cur_point[0] - p * (wp + s - 2 * i * s), cur_point[1])
                    mid_points2.append(cur_point)
                    cur_point = (cur_point[0], cur_point[1] + (hp + s - 2 * i * s))
                    mid_points2.append(cur_point)

            mid_points2.reverse()
            waypoints = start_points + mid_points + mid_points2 + end_points
            wg = Waveguide(waypoints, self.wgt)
            dist = h + self.bend_radius
        if self.direction == 'WEST':
            wgr = gdspy.CellReference(wg, rotation=90)
            self.portlist_output = (self.port[0] - dist, self.port[1])
        else:
            if self.direction == 'SOUTH':
                wgr = gdspy.CellReference(wg, rotation=180)
                self.portlist_output = (self.port[0], self.port[1] - dist)
            else:
                if self.direction == 'EAST':
                    wgr = gdspy.CellReference(wg, rotation=(-90))
                    self.portlist_output = (self.port[0] + dist, self.port[1])
                else:
                    if self.direction == 'NORTH':
                        wgr = gdspy.CellReference(wg)
                        self.portlist_output = (self.port[0], self.port[1] + dist)
                    else:
                        if isinstance(self.direction, float):
                            wgr = gdspy.CellReference(wg,
                              rotation=(self.direction * 180 / np.pi - 90.0))
                            self.portlist_output = (
                             self.port[0] + dist * np.cos(self.direction),
                             self.port[1] + dist * np.sin(self.direction))
                        wgr.translate(self.port[0], self.port[1])
                        self.add(wgr)

    def build_ports(self):
        self.portlist['input'] = {'port':self.port, 
         'direction':tk.flip_direction(self.direction)}
        self.portlist['output'] = {'port':self.portlist_output, 
         'direction':self.direction}


if __name__ == '__main__':
    from picwriter.components.waveguide import WaveguideTemplate
    top = gdspy.Cell('top')
    wgt = WaveguideTemplate(bend_radius=50, resist='-')
    sp1 = Spiral(wgt, 500.0, 1000.0, 10000.0, port=(100, 200), direction=(np.pi / 4.0))
    tk.add(top, sp1)
    gdspy.LayoutViewer()