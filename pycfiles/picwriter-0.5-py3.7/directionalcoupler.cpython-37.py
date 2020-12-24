# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\directionalcoupler.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 8202 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk
from picwriter.components.waveguide import Waveguide

class DirectionalCoupler(tk.Component):
    __doc__ = " Directional Coupler Cell class.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **length** (float): Length of the coupling region.\n           * **gap** (float): Distance between the two waveguides.\n\n        Keyword Args:\n           * **angle** (float): Angle in radians (between 0 and pi/2) at which the waveguide bends towards the coupling region.  Default=pi/6.\n           * **parity** (integer -1 or 1): If -1, mirror-flips the structure so that the input port is actually the *bottom* port.  Default = 1.\n           * **port** (tuple): Cartesian coordinate of the input port (AT TOP if parity=1, AT BOTTOM if parity=-1).  Defaults to (0,0).\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians).  Defaults to 'EAST'.\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input_top'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['input_bot'] = {'port': (x2,y2), 'direction': 'dir1'}\n           * portlist['output_top'] = {'port': (x3, y3), 'direction': 'dir3'}\n           * portlist['output_bot'] = {'port': (x4, y4), 'direction': 'dir4'}\n\n        Where in the above (x1,y1) (or (x2,y2) if parity=-1) is the same as the input 'port', (x3, y3), and (x4, y4) are the two output port locations.  Directions 'dir1', 'dir2', etc. are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n    "

    def __init__(self, wgt, length, gap, angle=np.pi / 6.0, parity=1, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'DirectionalCoupler', locals())
        self.portlist = {}
        self.port = port
        self.direction = direction
        if angle > np.pi / 2.0 or angle < 0:
            raise ValueError('Warning! Improper angle specified (' + str(angle) + '). Must be between 0 and pi/2.0.')
        self.angle = angle
        if parity != 1:
            if parity != -1:
                raise ValueError('Warning! Parity input *must* be 1 or -1. Received parity=' + str(parity) + ' instead.')
        self.parity = parity
        self.length = length
        self.gap = gap
        self.wgt = wgt
        self.wg_spec = {'layer':wgt.wg_layer,  'datatype':wgt.wg_datatype}
        self.clad_spec = {'layer':wgt.clad_layer,  'datatype':wgt.clad_datatype}
        self._DirectionalCoupler__build_cell()
        self._DirectionalCoupler__build_ports()
        self._auto_transform_()

    def __build_cell(self):
        x0, y0 = (0, 0)
        dlx = abs(self.wgt.bend_radius * np.tan(self.angle / 2.0))
        padding = 0.01
        angle_x_dist = 2.0 * (dlx + padding) * np.cos(self.angle)
        angle_y_dist = 2.0 * (dlx + padding) * np.sin(self.angle) * self.parity
        tracelist_top = [
         (
          x0, y0),
         (
          x0 + dlx + padding, y0),
         (
          x0 + dlx + padding + angle_x_dist, y0 - angle_y_dist),
         (
          x0 + 3 * dlx + padding + angle_x_dist + self.length, y0 - angle_y_dist),
         (
          x0 + 3 * dlx + padding + 2 * angle_x_dist + self.length, y0),
         (
          x0 + 4 * dlx + 2 * padding + 2 * angle_x_dist + self.length, y0)]
        wg_top = Waveguide(tracelist_top, self.wgt)
        y_bot_start = y0 - (2 * abs(angle_y_dist) + self.gap + self.wgt.wg_width) * self.parity
        tracelist_bot = [
         (
          x0, y_bot_start),
         (
          x0 + dlx + padding, y_bot_start),
         (
          x0 + dlx + padding + angle_x_dist, y_bot_start + angle_y_dist),
         (
          x0 + 3 * dlx + padding + angle_x_dist + self.length,
          y_bot_start + angle_y_dist),
         (
          x0 + 3 * dlx + padding + 2 * angle_x_dist + self.length, y_bot_start),
         (
          x0 + 4 * dlx + 2 * padding + 2 * angle_x_dist + self.length, y_bot_start)]
        wg_bot = Waveguide(tracelist_bot, self.wgt)
        distx = 4 * dlx + 2 * angle_x_dist + self.length
        disty = (2 * abs(angle_y_dist) + self.gap + self.wgt.wg_width) * self.parity
        self.add(wg_top)
        self.add(wg_bot)
        self.portlist_input = (0, 0)
        self.portlist_output_straight = (distx, 0.0)
        self.portlist_output_cross = (distx, -disty)
        self.portlist_input_cross = (0.0, -disty)

    def __build_ports(self):
        if self.parity == 1:
            self.portlist['input_top'] = {'port':self.portlist_input,  'direction':'WEST'}
            self.portlist['input_bot'] = {'port':self.portlist_input_cross, 
             'direction':'WEST'}
            self.portlist['output_top'] = {'port':self.portlist_output_straight, 
             'direction':'EAST'}
            self.portlist['output_bot'] = {'port':self.portlist_output_cross, 
             'direction':'EAST'}
        else:
            if self.parity == -1:
                self.portlist['input_top'] = {'port':self.portlist_input_cross,  'direction':'WEST'}
                self.portlist['input_bot'] = {'port':self.portlist_input, 
                 'direction':'WEST'}
                self.portlist['output_top'] = {'port':self.portlist_output_cross, 
                 'direction':'EAST'}
                self.portlist['output_bot'] = {'port':self.portlist_output_straight, 
                 'direction':'EAST'}


if __name__ == '__main__':
    from . import *
    from picwriter.components.waveguide import WaveguideTemplate
    top = gdspy.Cell('top')
    wgt = WaveguideTemplate(bend_radius=100, resist='+')
    wg1 = Waveguide([(0, 0), (100, 0)], wgt)
    tk.add(top, wg1)
    dc1 = DirectionalCoupler(
 wgt, 10.0, 0.5, angle=np.pi / 6.0, parity=1, **wg1.portlist['output'])
    dc2 = DirectionalCoupler(
 wgt, 10.0, 0.5, angle=np.pi / 6.0, parity=-1, **dc1.portlist['output_top'])
    dc3 = DirectionalCoupler(
 wgt, 10.0, 0.5, angle=np.pi / 6.0, parity=1, **dc1.portlist['output_bot'])
    dc4 = DirectionalCoupler(
 wgt, 10.0, 0.5, angle=np.pi / 6.0, parity=1, **dc2.portlist['output_bot'])
    dc5 = DirectionalCoupler(
 wgt, 10.0, 0.5, angle=np.pi / 6.0, parity=-1, **dc2.portlist['output_top'])
    dc6 = DirectionalCoupler(
 wgt, 10.0, 0.5, angle=np.pi / 6.0, parity=1, **dc3.portlist['output_bot'])
    tk.add(top, dc1)
    tk.add(top, dc2)
    tk.add(top, dc3)
    tk.add(top, dc4)
    tk.add(top, dc5)
    tk.add(top, dc6)
    print(top.area())
    gdspy.LayoutViewer()