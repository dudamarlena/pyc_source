# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\ysplitter.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 9941 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, scipy.interpolate, gdspy
import picwriter.toolkit as tk
from picwriter.components.ebend import EulerSBend
from picwriter.components.taper import Taper

class SplineYSplitter(tk.Component):
    __doc__ = " 1x2 Spline based Y Splitter Cell class.\n        Based on Zhang et al. (2013) A compact and low loss Y-junction for submicron silicon waveguide https://doi.org/10.1364/OE.21.001310\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **length** (float): Length of the splitter region (along direction of propagation)\n           * **widths** (array of floats): Widths of the Spline Curve Splitter region (perpendicular to direction of propagation).  Width values are evenly spaced along the length of the splitter.\n\n        Keyword Args:\n           * **wg_sep** (float): Separation between waveguides on the 2-port side (defaults to be flush with the last width in the splitter region). Defaults to None.\n           * **taper_width** (float): Ending width of the taper region (default = wg_width from wg_template).  Defaults to None (waveguide width).\n           * **taper_length** (float): Length of the input taper leading up to the Y-splitter (single-port side).  Defaults to None (no input taper, port right against the splitter region).\n           * **output_length** (float): Length (along x-direction) of the output bends, made with Euler S-Bends.  Defaults to None (no output bend, ports right up againt the splitter region).\n           * **output_wg_sep** (float): Distance (along y-direction) between the two output bends, made with Euler S-Bends.  Defaults to None (no output bend, ports right up againt the splitter region).\n           * **output_width** (float): Starting width of the output waveguide.  Defaults to None (no change from regular wg_width).\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output_top'] = {'port': (x2, y2), 'direction': 'dir2'}\n           * portlist['output_bot'] = {'port': (x3, y3), 'direction': 'dir3'}\n\n        Where in the above (x1,y1) is the input port, (x2, y2) is the top output port, (x3, y3) is the bottom output port, and 'dir1', 'dir2', 'dir3' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n    "

    def __init__(self, wgt, length, widths, wg_sep=None, taper_width=None, taper_length=None, output_length=None, output_wg_sep=None, output_width=None, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'YSpline1x2', locals())
        self.port = port
        self.direction = direction
        self.portlist = {}
        self.wgt = wgt
        self.length = length
        self.widths = widths
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
            self.wg_sep = widths[(-1)] - self.output_width if wg_sep == None else wg_sep
            self.resist = wgt.resist
            self.wg_spec = {'layer':wgt.wg_layer,  'datatype':wgt.wg_datatype}
            self.clad_spec = {'layer':wgt.clad_layer,  'datatype':wgt.clad_datatype}
            self.input_port = (0, 0)
            self.output_port_top = (self.totlength, self.output_wg_sep / 2.0)
            self.output_port_bot = (self.totlength, -self.output_wg_sep / 2.0)
            self._SplineYSplitter__type_check_values()
            self._SplineYSplitter__build_cell()
            self._SplineYSplitter__build_ports()
            self._auto_transform_()

    def __type_check_values(self):
        if self.wg_sep > self.widths[(-1)] - self.output_width:
            raise ValueError('Warning! Waveguide separation is larger than the max value (width - taper_width)')
        else:
            if self.draw_input:
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
            tp.addto(self)
            x, y = tp.portlist['output']['port']
        x_widths = np.linspace(0, self.length, len(self.widths))
        x_positions = np.linspace(0, self.length, int(self.length // 0.0025))
        spl = scipy.interpolate.CubicSpline(x_widths,
          (self.widths), bc_type='clamped')
        y_positions = spl(x_positions)
        coupler_pts = np.concatenate((
         [
          x_positions, y_positions / 2],
         [
          x_positions[::-1], -y_positions[::-1] / 2]),
          axis=1).T
        coupler_region = (gdspy.Polygon)(coupler_pts, **self.wg_spec)
        self.add(coupler_region)
        x, y = x + self.length, y
        clad_region = (gdspy.Polygon)(
         [
          (
           x_positions[0], y_positions[0] / 2.0 + self.wgt.clad_width),
          (
           x_positions[(-1)], y_positions[(-1)] / 2.0 + self.wgt.clad_width),
          (
           x_positions[(-1)], -y_positions[(-1)] / 2.0 - self.wgt.clad_width),
          (
           x_positions[0], -y_positions[0] / 2.0 - self.wgt.clad_width)], **self.clad_spec)
        self.add(clad_region)
        if self.draw_outputs:
            dy = (self.output_wg_sep - self.wg_sep) / 2.0
            esb_top = EulerSBend((self.wgt),
              (self.output_length),
              dy,
              (self.output_width),
              end_width=(self.wgt.wg_width),
              port=(
             x, y + self.wg_sep / 2.0))
            esb_top.addto(self)
            esb_bot = EulerSBend((self.wgt),
              (self.output_length),
              (-dy),
              (self.output_width),
              end_width=(self.wgt.wg_width),
              port=(
             x, y - self.wg_sep / 2.0))
            esb_bot.addto(self)

    def __build_ports(self):
        self.portlist['input'] = {'port':self.input_port, 
         'direction':'WEST'}
        self.portlist['output_top'] = {'port':self.output_port_top, 
         'direction':'EAST'}
        self.portlist['output_bot'] = {'port':self.output_port_bot, 
         'direction':'EAST'}


if __name__ == '__main__':
    import picwriter.components as pc
    top = gdspy.Cell('top')
    wgt = pc.WaveguideTemplate(bend_radius=50, wg_width=0.5, resist='+')
    spline_widths = [
     0.5, 0.5, 0.6, 0.7, 0.9, 1.26, 1.4, 1.4, 1.4, 1.4, 1.31, 1.2, 1.2]
    ysplitter = SplineYSplitter(wgt,
      length=2,
      widths=spline_widths,
      taper_width=None,
      taper_length=None,
      output_length=10,
      output_wg_sep=5,
      output_width=0.5,
      port=(0, 0),
      direction='EAST')
    wg1 = pc.Waveguide([(-10, 0), ysplitter.portlist['input']['port']], wgt)
    ysplitter.addto(top)
    wg1.addto(top)
    gdspy.LayoutViewer()