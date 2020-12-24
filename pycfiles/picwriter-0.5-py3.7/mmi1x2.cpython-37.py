# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\mmi1x2.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 12021 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk
from picwriter.components.ebend import EulerSBend
from picwriter.components.taper import Taper

class MMI1x2(tk.Component):
    __doc__ = " 1x2 multi-mode interfereomter (MMI) Cell class.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **length** (float): Length of the MMI region (along direction of propagation)\n           * **width** (float): Width of the MMI region (perpendicular to direction of propagation)\n\n        Keyword Args:\n           * **wg_sep** (float): Separation between waveguides on the 2-port side (defaults to width/3.0).  Defaults to None (width/3.0).\n           * **taper_width** (float): Ending width of the taper region (default = wg_width from wg_template).  Defaults to None (waveguide width).\n           * **taper_length** (float): Length of the input taper leading up to the MMI (single-port side).  Defaults to None (no input taper, port right against the MMI region).\n           * **output_length** (float): Length (along x-direction) of the output bends, made with Euler S-Bends.  Defaults to None (no output bend, ports right up againt the MMI region).\n           * **output_wg_sep** (float): Distance (along y-direction) between the two output bends, made with Euler S-Bends.  Defaults to None (no output bend, ports right up againt the MMI region).\n           * **output_width** (float): Starting width of the output waveguide.  Defaults to None (no change from regular wg_width).\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output_top'] = {'port': (x2, y2), 'direction': 'dir2'}\n           * portlist['output_bot'] = {'port': (x3, y3), 'direction': 'dir3'}\n\n        Where in the above (x1,y1) is the input port, (x2, y2) is the top output port, (x3, y3) is the bottom output port, and 'dir1', 'dir2', 'dir3' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n    "

    def __init__(self, wgt, length, width, wg_sep=None, taper_width=None, taper_length=None, output_length=None, output_wg_sep=None, output_width=None, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'MMI1x2', locals())
        self.port = port
        self.direction = direction
        self.portlist = {}
        self.wgt = wgt
        self.length = length
        self.width = width
        self.totlength = length
        if output_length != None and output_wg_sep != None:
            self.output_length = output_length
            self.output_wg_sep = output_wg_sep
            self.output_width = wgt.wg_width if output_width == None else output_width
            self.draw_outputs = True
            self.totlength += self.output_length
        else:
            if output_length == None:
                if output_wg_sep == None:
                    self.draw_outputs = False
                    self.output_wg_sep = wg_sep
                else:
                    raise ValueError('Warning! One of the two output values was None, and the other was provided.  Both must be provided *OR* omitted.')
            elif taper_width != None and taper_length != None:
                self.taper_width = taper_width
                self.taper_length = taper_length
                self.draw_input = True
                self.totlength += taper_length
            else:
                if taper_width == None and taper_length == None:
                    self.draw_input = False
                else:
                    raise ValueError('Warning! One of the two input values was None, and the other was provided.  Both must be provided *OR* omitted.')
            self.wg_sep = width / 3.0 if wg_sep == None else wg_sep
            self.resist = wgt.resist
            self.wg_spec = {'layer':wgt.wg_layer,  'datatype':wgt.wg_datatype}
            self.clad_spec = {'layer':wgt.clad_layer,  'datatype':wgt.clad_datatype}
            self.input_port = (0, 0)
            self.output_port_top = (self.totlength, self.output_wg_sep / 2.0)
            self.output_port_bot = (self.totlength, -self.output_wg_sep / 2.0)
            self._MMI1x2__type_check_values()
            self._MMI1x2__build_cell()
            self._MMI1x2__build_ports()
            self._auto_transform_()

    def __type_check_values(self):
        if self.wg_sep > self.width - self.taper_width:
            raise ValueError('Warning! Waveguide separation is larger than the max value (width - taper_width)')
        else:
            if self.wg_sep < self.taper_width:
                raise ValueError('Warning! Waveguide separation is smaller than the minimum value (taper_width)')
            if self.draw_outputs and self.output_length < (self.output_wg_sep - self.wg_sep) / 2.0:
                raise ValueError('Warning! The output length must be greater than half the output wg separation')

    def __build_cell(self):
        x, y = (0, 0)
        if self.draw_input:
            tp = Taper((self.wgt),
              (self.taper_length),
              (self.taper_width),
              port=(
             x, y),
              direction='EAST')
            self.add(tp)
            x, y = tp.portlist['output']['port']
        mmi = gdspy.Path(self.width, (x, y))
        (mmi.segment)(self.length, direction='+x', **self.wg_spec)
        self.add(mmi)
        clad_pts = [
         (
          0.0, -self.wgt.wg_width / 2.0 - self.wgt.clad_width),
         (
          self.taper_length, -self.width / 2.0 - self.wgt.clad_width),
         (
          self.taper_length + self.length, -self.width / 2.0 - self.wgt.clad_width),
         (
          2 * self.taper_length + self.length,
          -self.wg_sep / 2.0 - self.wgt.wg_width / 2.0 - self.wgt.clad_width),
         (
          2 * self.taper_length + self.length,
          self.wg_sep / 2.0 + self.wgt.wg_width / 2.0 + self.wgt.clad_width),
         (
          self.taper_length + self.length, self.width / 2.0 + self.wgt.clad_width),
         (
          self.taper_length, self.width / 2.0 + self.wgt.clad_width),
         (
          0.0, self.wgt.wg_width / 2.0 + self.wgt.clad_width)]
        clad = (gdspy.Polygon)(clad_pts, **self.clad_spec)
        self.add(clad)
        x, y = x + self.length, y
        if self.draw_outputs:
            dy = (self.output_wg_sep - self.wg_sep) / 2.0
            esb_top = EulerSBend((self.wgt),
              (self.output_length),
              dy,
              (self.output_width),
              end_width=(self.wgt.wg_width),
              port=(
             x, y + self.wg_sep / 2.0))
            self.add(esb_top)
            esb_bot = EulerSBend((self.wgt),
              (self.output_length),
              (-dy),
              (self.output_width),
              end_width=(self.wgt.wg_width),
              port=(
             x, y - self.wg_sep / 2.0))
            self.add(esb_bot)

    def __build_ports(self):
        self.portlist['input'] = {'port':self.input_port, 
         'direction':'WEST'}
        self.portlist['output_top'] = {'port':self.output_port_top, 
         'direction':'EAST'}
        self.portlist['output_bot'] = {'port':self.output_port_bot, 
         'direction':'EAST'}


if __name__ == '__main__':
    from . import *
    top = gdspy.Cell('top')
    wgt = WaveguideTemplate(bend_radius=50, wg_width=1.0, resist='+')
    mmi = MMI1x2(wgt,
      length=20,
      width=7,
      taper_length=10.0,
      taper_width=2.0,
      wg_sep=3.5,
      output_wg_sep=10.0,
      output_length=20.0,
      output_width=2.0)
    mmi.addto(top)
    gdspy.LayoutViewer()