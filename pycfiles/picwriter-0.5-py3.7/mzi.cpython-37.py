# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\mzi.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 54970 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk
from picwriter.components.mmi1x2 import MMI1x2
from picwriter.components.mmi2x2 import MMI2x2
from picwriter.components.waveguide import Waveguide
from picwriter.components.electrical import MetalRoute
from picwriter.components.directionalcoupler import DirectionalCoupler

class MachZehnder(tk.Component):
    __doc__ = " Mach-Zehnder Cell class with thermo-optic option.  It is possible to generate your own Mach-Zehnder from the waveguide and MMI1x2 classes, but this class is simply a shorthand (with some extra type-checking).  Defaults to a *balanced* Mach Zehnder.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **MMIlength** (float): Length of the 1x2 MMI region (along direction of propagation)\n           * **MMIwidth** (float): Width of the 1x2 MMI region (perpendicular to direction of propagation).\n\n        Keyword Args:\n           * **angle** (float): Angle in radians (between 0 and pi/2) at which the waveguide bends towards the coupling region.  Default=pi/6.\n           * **MMItaper_width** (float): Maximum width of the 1x2 MMI taper region (default = wg_width from wg_template).  Defaults to None (waveguide width).\n           * **MMItaper_length** (float): Length of the taper leading up to the 1x2 MMI.  Defaults to None (taper_length=20).\n           * **MMIwg_sep** (float): Separation between waveguides on the 2-port side of the 1x2 MMI (defaults to width/3.0)\n           * **arm1** (float): Additional length of the top arm (when going `'EAST'`).  Defaults to zero.\n           * **arm2** (float): Additional length of the bottom arm (when going `'EAST'`).  Defaults to zero.\n           * **heater** (boolean): If true, adds heater on-top of one MZI arm.  Defaults to False.\n           * **heater_length** (float): Specifies the length of the heater along the waveguide. Doesn't include the length of the 180 degree bend.  Defaults to 400.0.\n           * **mt** (MetalTemplate): If 'heater' is true, must specify a Metal Template that defines heater & heater cladding layers.\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians). Defaults to `'EAST'` (0 radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output'] = {'port': (x2, y2), 'direction': 'dir2'}\n           * portlist['heater_top_in'] = {'port', (x3, y3), 'direction': 'dir3'}\n           * portlist['heater_top_out'] = {'port', (x4, y4), 'direction': 'dir4'}\n           * portlist['heater_bot_in'] = {'port', (x5, y5), 'direction': 'dir5'}\n           * portlist['heater_bot_out'] = {'port', (x6, y6), 'direction': 'dir6'}\n\n        Where in the above (x1,y1) is the input port, (x2, y2) is the output port, and the directions are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n        Four additional ports are created for the heaters if the `heater` argument is True.  Metals are not generated, but should be connected to the specified 'heater' ports.\n\n    "

    def __init__(self, wgt, MMIlength, MMIwidth, angle=np.pi / 6.0, MMItaper_width=None, MMItaper_length=None, MMIwg_sep=None, arm1=0, arm2=0, heater=False, heater_length=400, mt=None, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'MachZehnder', locals())
        self.portlist = {}
        self.wgt = wgt
        self.arm1 = arm1
        self.arm2 = arm2
        if angle > np.pi / 2.0 or angle < 0:
            raise ValueError('Warning! Improper angle specified (' + str(angle) + ').  Must be between 0 and pi/2.0.')
        else:
            self.angle = angle
            self.MMIlength = MMIlength
            self.MMIwidth = MMIwidth
            self.MMItaper_width = wgt.wg_width if MMItaper_width == None else MMItaper_width
            self.MMItaper_length = 20 if MMItaper_length == None else MMItaper_length
            self.MMIwg_sep = MMIwidth / 3.0 if MMIwg_sep == None else MMIwg_sep
            angle_x_dist = 2 * self.wgt.bend_radius * np.sin(self.angle)
            self.mmilength = self.MMIlength + angle_x_dist + self.MMItaper_length
            self.heater = heater
            if heater:
                self.heater_length = heater_length
                self.mt = mt
            else:
                self.heater_length = 0
        self.port = port
        self.direction = direction
        self._MachZehnder__build_cell()
        self._MachZehnder__build_ports()
        self._auto_transform_()

    def __build_cell(self):
        mmi1 = MMI1x2((self.wgt),
          (self.MMIlength),
          (self.MMIwidth),
          angle=(self.angle),
          taper_width=(self.MMItaper_width),
          taper_length=(self.MMItaper_length),
          wg_sep=(self.MMIwg_sep),
          port=(0, 0),
          direction='EAST')
        mmi2 = MMI1x2((self.wgt),
          (self.MMIlength),
          (self.MMIwidth),
          angle=(self.angle),
          taper_width=(self.MMItaper_width),
          taper_length=(self.MMItaper_length),
          wg_sep=(self.MMIwg_sep),
          port=(
         2 * self.mmilength + 4 * self.wgt.bend_radius, 0),
          direction='WEST')
        y_end_top, y_end_bot = mmi2.portlist['output_top']['port'][1], mmi2.portlist['output_bot']['port'][1]
        x0, y0 = mmi1.portlist['output_top']['port']
        trace1 = [
         (
          x0, y0),
         (
          x0 + self.wgt.bend_radius, y0),
         (
          x0 + self.wgt.bend_radius,
          y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
         (
          x0 + 3 * self.wgt.bend_radius,
          y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
         (
          x0 + 3 * self.wgt.bend_radius, y_end_bot),
         (
          x0 + 4 * self.wgt.bend_radius, y_end_bot)]
        wg_top = Waveguide(trace1, self.wgt)
        x1, y1 = mmi1.portlist['output_bot']['port']
        trace2 = [
         (
          x1, y1),
         (
          x1 + self.wgt.bend_radius, y1),
         (
          x1 + self.wgt.bend_radius,
          y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
         (
          x1 + 3 * self.wgt.bend_radius,
          y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
         (
          x1 + 3 * self.wgt.bend_radius, y_end_top),
         (
          x1 + 4 * self.wgt.bend_radius, y_end_top)]
        wg_bot = Waveguide(trace2, self.wgt)
        if self.heater:
            heater_trace1 = [
             (
              x0 + self.wgt.bend_radius,
              y0 + self.arm1 / 2.0 + self.wgt.bend_radius),
             (
              x0 + self.wgt.bend_radius,
              y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y0 + self.arm1 / 2.0 + self.wgt.bend_radius)]
            heater_top = MetalRoute(heater_trace1, self.mt)
            heater_trace2 = [
             (
              x0 + self.wgt.bend_radius,
              y1 - self.arm2 / 2.0 - self.wgt.bend_radius),
             (
              x0 + self.wgt.bend_radius,
              y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y1 - self.arm2 / 2.0 - self.wgt.bend_radius)]
            heater_bot = MetalRoute(heater_trace2, self.mt)
        totallen = 2 * self.mmilength + 4 * self.wgt.bend_radius
        self.port_output = (
         totallen, 0)
        self.htr_top_in_dir = 'WEST'
        self.htr_top_out_dir = 'EAST'
        self.htr_bot_in_dir = 'WEST'
        self.htr_bot_out_dir = 'EAST'
        components = [
         mmi1, mmi2, wg_top, wg_bot]
        if self.heater:
            self.htr_top_in = (x0 + self.wgt.bend_radius,
             y0 + self.arm1 / 2.0 + self.wgt.bend_radius + self.mt.width / 2.0)
            self.htr_top_out = (
             x0 + 3 * self.wgt.bend_radius,
             y0 + self.arm1 / 2.0 + self.wgt.bend_radius + self.mt.width / 2.0)
            self.htr_bot_in = (
             x0 + self.wgt.bend_radius,
             y1 - self.arm2 / 2.0 - self.wgt.bend_radius - self.mt.width / 2.0)
            self.htr_bot_out = (
             x0 + 3 * self.wgt.bend_radius,
             y1 - self.arm2 / 2.0 - self.wgt.bend_radius - self.mt.width / 2.0)
            components.append(heater_top)
            components.append(heater_bot)
        for c in components:
            self.add(c)

    def __build_ports(self):
        self.portlist['input'] = {'port':(0, 0), 
         'direction':'WEST'}
        self.portlist['output'] = {'port':self.port_output,  'direction':'EAST'}
        if self.heater:
            self.portlist['heater_top_in'] = {'port':self.htr_top_in,  'direction':self.htr_top_in_dir}
            self.portlist['heater_top_out'] = {'port':self.htr_top_out, 
             'direction':self.htr_top_out_dir}
            self.portlist['heater_bot_in'] = {'port':self.htr_bot_in, 
             'direction':self.htr_bot_in_dir}
            self.portlist['heater_bot_out'] = {'port':self.htr_bot_out, 
             'direction':self.htr_bot_out_dir}


class MachZehnderSwitch1x2(tk.Component):
    __doc__ = " Standard Mach-Zehnder Optical Switch Cell class with heaters on each arm.  It is possible to generate your own Mach-Zehnder from the waveguide and MMI1x2 classes, but this class is simply a shorthand (with some extra type-checking).  Defaults to a *balanced* Mach Zehnder.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **MMI1x2length** (float): Length of the 1x2 MMI region (along direction of propagation)\n           * **MMI1x2width** (float): Width of the 1x2 MMI region (perpendicular to direction of propagation).\n           * **MMI2x2length** (float): Length of the 2x2 MMI region (along direction of propagation)\n           * **MMI2x2width** (float): Width of the 2x2 MMI region (perpendicular to direction of propagation).\n\n        Keyword Args:\n           * **angle** (float): Angle in radians (between 0 and pi/2) at which the waveguide bends towards the coupling region.  Default=pi/6.\n           * **MMI1x2taper_width** (float): Maximum width of the 1x2 MMI taper region (default = wg_width from wg_template).  Defaults to None (waveguide width).\n           * **MMI1x2taper_length** (float): Length of the taper leading up to the 1x2 MMI.  Defaults to None (taper_length=20).\n           * **MMI1x2wg_sep** (float): Separation between waveguides on the 2-port side of the 1x2 MMI (defaults to width/3.0)\n           * **MMI2x2taper_width** (float): Maximum width of the 2x2 MMI taper region (default = wg_width from wg_template).  Defaults to None (waveguide width).\n           * **MMI2x2wg_sep** (float): Separation between waveguides of the 2x2 MMI (defaults to width/3.0)\n           * **arm1** (float): Additional length of the top arm (when going `'EAST'`).  Defaults to zero.\n           * **arm2** (float): Additional length of the bottom arm (when going `'EAST'`).  Defaults to zero.\n           * **heater** (boolean): If true, adds heater on-top of one MZI arm.  Defaults to False.\n           * **heater_length** (float): Specifies the length of the heater along the waveguide. Doesn't include the length of the 180 degree bend.  Defaults to 400.0.\n           * **mt** (MetalTemplate): If 'heater' is true, must specify a Metal Template that defines heater & heater cladding layers.\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the taper will point *towards*, must be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians).  Defaults to `'EAST'` (0 radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output_top'] = {'port': (x2, y2), 'direction': 'dir2'}\n           * portlist['output_bot'] = {'port': (x3, y3), 'direction': 'dir3'}\n           * portlist['heater_top_in'] = {'port', (x4, y4), 'direction': 'dir4'}\n           * portlist['heater_top_out'] = {'port', (x5, y5), 'direction': 'dir5'}\n           * portlist['heater_bot_in'] = {'port', (x6, y6), 'direction': 'dir6'}\n           * portlist['heater_bot_out'] = {'port', (x7, y7), 'direction': 'dir7'}\n\n        Where in the above (x1,y1) is the input port, (x2, y2) is the top output port, (x3, y3) is the bottom output port, and the directions are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n        Four additional ports are created for the heaters if the `heater` argument is True.  Metals are not generated, but should be connected to the specified 'heater' ports.\n\n    "

    def __init__(self, wgt, MMI1x2length, MMI1x2width, MMI2x2length, MMI2x2width, angle=np.pi / 6.0, MMI1x2taper_width=None, MMI1x2taper_length=None, MMI1x2wg_sep=None, MMI2x2taper_width=None, MMI2x2wg_sep=None, arm1=0, arm2=0, heater=False, heater_length=400, mt=None, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'MachZehnderSwitch1x2', locals())
        self.portlist = {}
        self.wgt = wgt
        self.arm1 = arm1
        self.arm2 = arm2
        if angle > np.pi / 2.0 or angle < 0:
            raise ValueError('Warning! Improper angle specified (' + str(angle) + ').  Must be between 0 and pi/2.0.')
        else:
            self.angle = angle
            self.MMI1x2length = MMI1x2length
            self.MMI1x2width = MMI1x2width
            self.MMI1x2taper_width = wgt.wg_width if MMI1x2taper_width == None else MMI1x2taper_width
            self.MMI1x2taper_length = 20 if MMI1x2taper_length == None else MMI1x2taper_length
            self.MMI1x2wg_sep = MMI1x2width / 3.0 if MMI1x2wg_sep == None else MMI1x2wg_sep
            self.MMI2x2length = MMI2x2length
            self.MMI2x2width = MMI2x2width
            self.MMI2x2taper_width = wgt.wg_width if MMI2x2taper_width == None else MMI2x2taper_width
            self.MMI2x2wg_sep = MMI2x2width / 3.0 if MMI2x2wg_sep == None else MMI2x2wg_sep
            self.angle_x_dist = 2 * self.wgt.bend_radius * np.sin(self.angle)
            self.angle_y_dist = 2 * self.wgt.bend_radius * (1 - np.cos(self.angle))
            self.mmi1x2length = self.MMI1x2length + self.MMI1x2taper_length + self.angle_x_dist
            self.mmi2x2length = self.MMI2x2length + 2 * self.angle_x_dist
            self.heater = heater
            if heater:
                self.heater_length = heater_length
                self.mt = mt
            else:
                self.heater_length = 0
        self.port = port
        self.direction = direction
        self._MachZehnderSwitch1x2__build_cell()
        self._MachZehnderSwitch1x2__build_ports()
        self._auto_transform_()

    def __build_cell(self):
        mmi1 = MMI1x2((self.wgt),
          (self.MMI1x2length),
          (self.MMI1x2width),
          angle=(self.angle),
          taper_width=(self.MMI1x2taper_width),
          taper_length=(self.MMI1x2taper_length),
          wg_sep=(self.MMI1x2wg_sep),
          port=(0, 0),
          direction='EAST')
        mmi2 = MMI2x2((self.wgt),
          (self.MMI2x2length),
          (self.MMI2x2width),
          angle=(self.angle),
          taper_width=(self.MMI2x2taper_width),
          wg_sep=(self.MMI2x2wg_sep),
          port=(
         self.mmi2x2length + self.mmi1x2length + 4 * self.wgt.bend_radius,
         -self.MMI2x2wg_sep / 2.0 - self.angle_y_dist),
          direction='WEST')
        y_end_top, y_end_bot = mmi2.portlist['output_top']['port'][1], mmi2.portlist['output_bot']['port'][1]
        x0, y0 = mmi1.portlist['output_top']['port']
        trace1 = [
         (
          x0, y0),
         (
          x0 + self.wgt.bend_radius, y0),
         (
          x0 + self.wgt.bend_radius,
          y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
         (
          x0 + 3 * self.wgt.bend_radius,
          y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
         (
          x0 + 3 * self.wgt.bend_radius, y_end_bot),
         (
          x0 + 4 * self.wgt.bend_radius, y_end_bot)]
        wg_top = Waveguide(trace1, self.wgt)
        x1, y1 = mmi1.portlist['output_bot']['port']
        trace2 = [
         (
          x1, y1),
         (
          x1 + self.wgt.bend_radius, y1),
         (
          x1 + self.wgt.bend_radius,
          y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
         (
          x1 + 3 * self.wgt.bend_radius,
          y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
         (
          x1 + 3 * self.wgt.bend_radius, y_end_top),
         (
          x1 + 4 * self.wgt.bend_radius, y_end_top)]
        wg_bot = Waveguide(trace2, self.wgt)
        if self.heater:
            heater_trace1 = [
             (
              x0 + self.wgt.bend_radius,
              y0 + self.arm1 / 2.0 + self.wgt.bend_radius),
             (
              x0 + self.wgt.bend_radius,
              y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y0 + self.arm1 / 2.0 + self.wgt.bend_radius)]
            heater_top = MetalRoute(heater_trace1, self.mt)
            heater_trace2 = [
             (
              x0 + self.wgt.bend_radius,
              y1 - self.arm2 / 2.0 - self.wgt.bend_radius),
             (
              x0 + self.wgt.bend_radius,
              y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y1 - self.arm2 / 2.0 - self.wgt.bend_radius)]
            heater_bot = MetalRoute(heater_trace2, self.mt)
        totalxlen = self.mmi2x2length + self.mmi1x2length + 4 * self.wgt.bend_radius
        self.port_output_top = (
         totalxlen, self.MMI2x2wg_sep / 2.0 + self.angle_y_dist)
        self.port_output_bot = (totalxlen, -self.MMI2x2wg_sep / 2.0 - self.angle_y_dist)
        self.htr_top_in_dir = 'WEST'
        self.htr_top_out_dir = 'EAST'
        self.htr_bot_in_dir = 'WEST'
        self.htr_bot_out_dir = 'EAST'
        components = [
         mmi1, mmi2, wg_top, wg_bot]
        if self.heater:
            self.htr_top_in = (x0 + self.wgt.bend_radius,
             y0 + self.arm1 / 2.0 + self.wgt.bend_radius + self.mt.width / 2.0)
            self.htr_top_out = (
             x0 + 3 * self.wgt.bend_radius,
             y0 + self.arm1 / 2.0 + self.wgt.bend_radius + self.mt.width / 2.0)
            self.htr_bot_in = (
             x0 + self.wgt.bend_radius,
             y1 - self.arm2 / 2.0 - self.wgt.bend_radius - self.mt.width / 2.0)
            self.htr_bot_out = (
             x0 + 3 * self.wgt.bend_radius,
             y1 - self.arm2 / 2.0 - self.wgt.bend_radius - self.mt.width / 2.0)
            components.append(heater_top)
            components.append(heater_bot)
        for c in components:
            self.add(c)

    def __build_ports(self):
        self.portlist['input'] = {'port':self.port, 
         'direction':'WEST'}
        self.portlist['output_top'] = {'port':self.port_output_top, 
         'direction':'EAST'}
        self.portlist['output_bot'] = {'port':self.port_output_bot, 
         'direction':'EAST'}
        if self.heater:
            self.portlist['heater_top_in'] = {'port':self.htr_top_in,  'direction':self.htr_top_in_dir}
            self.portlist['heater_top_out'] = {'port':self.htr_top_out, 
             'direction':self.htr_top_out_dir}
            self.portlist['heater_bot_in'] = {'port':self.htr_bot_in, 
             'direction':self.htr_bot_in_dir}
            self.portlist['heater_bot_out'] = {'port':self.htr_bot_out, 
             'direction':self.htr_bot_out_dir}


class MachZehnderSwitchDC1x2(tk.Component):
    __doc__ = " Standard Mach-Zehnder Optical Switch Cell class with heaters on each arm and a directional coupler.  It is possible to generate your own Mach-Zehnder from the other classes, but this class is simply a shorthand (with some extra type-checking).  Defaults to a *balanced* Mach Zehnder.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **MMI1x2length** (float): Length of the 1x2 MMI region (along direction of propagation)\n           * **MMI1x2width** (float): Width of the 1x2 MMI region (perpendicular to direction of propagation).\n           * **DClength** (float): Length of the directional coupler region\n           * **DCgap** (float): Size of the directional coupler gap\n\n        Keyword Args:\n           * **angle** (float): Angle in radians (between 0 and pi/2) at which the waveguide bends towards the coupling region (same for MMI & DC).  Default=pi/6.\n           * **MMI1x2taper_width** (float): Maximum width of the 1x2 MMI taper region (default = wg_width from wg_template).  Defaults to None (waveguide width).\n           * **MMI1x2taper_length** (float): Length of the taper leading up to the 1x2 MMI.  Defaults to None (taper_length=20).\n           * **MMI1x2wg_sep** (float): Separation between waveguides on the 2-port side of the 1x2 MMI (defaults to width/3.0)\n           * **arm1** (float): Additional length of the top arm (when going `'EAST'`).  Defaults to zero.\n           * **arm2** (float): Additional length of the bottom arm (when going `'EAST'`).  Defaults to zero.\n           * **heater** (boolean): If true, adds heater on-top of one MZI arm.  Defaults to False.\n           * **heater_length** (float): Specifies the length of the heater along the waveguide. Doesn't include the length of the 180 degree bend.  Defaults to 400.0.\n           * **mt** (MetalTemplate): If 'heater' is true, must specify a Metal Template that defines heater & heater cladding layers.\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the taper will point *towards*, must be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians).  Defaults to `'EAST'` (0 radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output_top'] = {'port': (x2, y2), 'direction': 'dir2'}\n           * portlist['output_bot'] = {'port': (x3, y3), 'direction': 'dir3'}\n           * portlist['heater_top_in'] = {'port', (x4, y4), 'direction': 'dir4'}\n           * portlist['heater_top_out'] = {'port', (x5, y5), 'direction': 'dir5'}\n           * portlist['heater_bot_in'] = {'port', (x6, y6), 'direction': 'dir6'}\n           * portlist['heater_bot_out'] = {'port', (x7, y7), 'direction': 'dir7'}\n\n        Where in the above (x1,y1) is the input port, (x2, y2) is the top output port, (x3, y3) is the bottom output port, and the directions are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n        Four additional ports are created for the heaters if the `heater` argument is True.  Metals are not generated, but should be connected to the specified 'heater' ports.\n\n    "

    def __init__(self, wgt, MMI1x2length, MMI1x2width, DClength, DCgap, angle=np.pi / 6.0, MMI1x2taper_width=None, MMI1x2taper_length=None, MMI1x2wg_sep=None, arm1=0, arm2=0, heater=False, heater_length=400, mt=None, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'MachZehnderSwitchDC1x2', locals())
        self.portlist = {}
        self.wgt = wgt
        self.arm1 = arm1
        self.arm2 = arm2
        if angle > np.pi / 2.0 or angle < 0:
            raise ValueError('Warning! Improper angle specified (' + str(angle) + ').  Must be between 0 and pi/2.0.')
        else:
            self.angle = angle
            self.MMI1x2length = MMI1x2length
            self.MMI1x2width = MMI1x2width
            self.MMI1x2taper_width = wgt.wg_width if MMI1x2taper_width == None else MMI1x2taper_width
            self.MMI1x2taper_length = 20 if MMI1x2taper_length == None else MMI1x2taper_length
            self.MMI1x2wg_sep = MMI1x2width / 3.0 if MMI1x2wg_sep == None else MMI1x2wg_sep
            self.DClength = DClength
            self.DCgap = DCgap
            self.angle_x_dist = 2 * self.wgt.bend_radius * np.sin(self.angle)
            self.angle_y_dist = 2 * self.wgt.bend_radius * (1 - np.cos(self.angle))
            padding = 0.01
            dlx = abs(self.wgt.bend_radius * np.tan(self.angle / 2.0))
            self.angle_x_distDC = 2 * dlx + 2.0 * (dlx + padding) * np.cos(self.angle)
            self.angle_y_distDC = 2.0 * (dlx + padding) * np.sin(self.angle)
            self.mmi1x2length = self.MMI1x2length + self.MMI1x2taper_length + self.angle_x_dist
            self.dclength = self.DClength + 2 * self.angle_x_distDC
            self.heater = heater
            if heater:
                self.heater_length = heater_length
                self.mt = mt
            else:
                self.heater_length = 0
        self.port = port
        self.direction = direction
        self._MachZehnderSwitchDC1x2__build_cell()
        self._MachZehnderSwitchDC1x2__build_ports()
        self._auto_transform_()

    def __build_cell(self):
        mmi1 = MMI1x2((self.wgt),
          (self.MMI1x2length),
          (self.MMI1x2width),
          angle=(self.angle),
          taper_width=(self.MMI1x2taper_width),
          taper_length=(self.MMI1x2taper_length),
          wg_sep=(self.MMI1x2wg_sep),
          port=(0, 0),
          direction='EAST')
        dc_out = DirectionalCoupler((self.wgt),
          (self.DClength),
          (self.DCgap),
          angle=(self.angle),
          port=(
         self.dclength + self.mmi1x2length + 4 * self.wgt.bend_radius,
         -self.DCgap / 2.0 - self.wgt.wg_width / 2.0 - self.angle_y_distDC),
          direction='WEST')
        y_end_top, y_end_bot = dc_out.portlist['output_top']['port'][1], dc_out.portlist['output_bot']['port'][1]
        x0, y0 = mmi1.portlist['output_top']['port']
        trace1 = [
         (
          x0, y0),
         (
          x0 + self.wgt.bend_radius, y0),
         (
          x0 + self.wgt.bend_radius,
          y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
         (
          x0 + 3 * self.wgt.bend_radius,
          y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
         (
          x0 + 3 * self.wgt.bend_radius, y_end_bot),
         (
          x0 + 4 * self.wgt.bend_radius, y_end_bot)]
        wg_top = Waveguide(trace1, self.wgt)
        x1, y1 = mmi1.portlist['output_bot']['port']
        trace2 = [
         (
          x1, y1),
         (
          x1 + self.wgt.bend_radius, y1),
         (
          x1 + self.wgt.bend_radius,
          y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
         (
          x1 + 3 * self.wgt.bend_radius,
          y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
         (
          x1 + 3 * self.wgt.bend_radius, y_end_top),
         (
          x1 + 4 * self.wgt.bend_radius, y_end_top)]
        wg_bot = Waveguide(trace2, self.wgt)
        if self.heater:
            heater_trace1 = [
             (
              x0 + self.wgt.bend_radius,
              y0 + self.arm1 / 2.0 + self.wgt.bend_radius),
             (
              x0 + self.wgt.bend_radius,
              y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y0 + self.arm1 / 2.0 + self.wgt.bend_radius)]
            heater_top = MetalRoute(heater_trace1, self.mt)
            heater_trace2 = [
             (
              x0 + self.wgt.bend_radius,
              y1 - self.arm2 / 2.0 - self.wgt.bend_radius),
             (
              x0 + self.wgt.bend_radius,
              y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y1 - self.arm2 / 2.0 - self.wgt.bend_radius)]
            heater_bot = MetalRoute(heater_trace2, self.mt)
        totalxlen = self.dclength + self.mmi1x2length + 4 * self.wgt.bend_radius
        self.port_output_top = (
         totalxlen,
         self.DCgap / 2.0 + self.wgt.wg_width / 2.0 + self.angle_y_distDC)
        self.port_output_bot = (
         totalxlen,
         -self.DCgap / 2.0 - self.wgt.wg_width / 2.0 - self.angle_y_distDC)
        self.htr_top_in_dir = 'WEST'
        self.htr_top_out_dir = 'EAST'
        self.htr_bot_in_dir = 'WEST'
        self.htr_bot_out_dir = 'EAST'
        components = [
         mmi1, dc_out, wg_top, wg_bot]
        if self.heater:
            self.htr_top_in = (x0 + self.wgt.bend_radius,
             y0 + self.arm1 / 2.0 + self.wgt.bend_radius + self.mt.width / 2.0)
            self.htr_top_out = (
             x0 + 3 * self.wgt.bend_radius,
             y0 + self.arm1 / 2.0 + self.wgt.bend_radius + self.mt.width / 2.0)
            self.htr_bot_in = (
             x0 + self.wgt.bend_radius,
             y1 - self.arm2 / 2.0 - self.wgt.bend_radius - self.mt.width / 2.0)
            self.htr_bot_out = (
             x0 + 3 * self.wgt.bend_radius,
             y1 - self.arm2 / 2.0 - self.wgt.bend_radius - self.mt.width / 2.0)
            components.append(heater_top)
            components.append(heater_bot)
        for c in components:
            self.add(c)

    def __build_ports(self):
        self.portlist['input'] = {'port':(0, 0), 
         'direction':'WEST'}
        self.portlist['output_top'] = {'port':self.port_output_top, 
         'direction':'EAST'}
        self.portlist['output_bot'] = {'port':self.port_output_bot, 
         'direction':'EAST'}
        if self.heater:
            self.portlist['heater_top_in'] = {'port':self.htr_top_in,  'direction':self.htr_top_in_dir}
            self.portlist['heater_top_out'] = {'port':self.htr_top_out, 
             'direction':self.htr_top_out_dir}
            self.portlist['heater_bot_in'] = {'port':self.htr_bot_in, 
             'direction':self.htr_bot_in_dir}
            self.portlist['heater_bot_out'] = {'port':self.htr_bot_out, 
             'direction':self.htr_bot_out_dir}


class MachZehnderSwitchDC2x2(tk.Component):
    __doc__ = " Standard Mach-Zehnder Optical Switch Cell class with heaters on each arm and a directional coupler for both input and output.  It is possible to generate your own Mach-Zehnder from the other classes, but this class is simply a shorthand (with some extra type-checking).  Defaults to a *balanced* Mach Zehnder.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **DC1length** (float): Length of the directional coupler region at the input\n           * **DC1gap** (float): Size of the directional coupler gap at the input\n           * **DC2length** (float): Length of the directional coupler region at the output\n           * **DC2gap** (float): Size of the directional coupler gap at the output\n\n        Keyword Args:\n           * **angle** (float): Angle in radians (between 0 and pi/2) at which the waveguide bends towards the coupling region.  Default=pi/6.\n           * **arm1** (float): Additional length of the top arm (when going `'EAST'`).  Defaults to zero.\n           * **arm2** (float): Additional length of the bottom arm (when going `'EAST'`).  Defaults to zero.\n           * **heater** (boolean): If true, adds heater on-top of one MZI arm.  Defaults to False.\n           * **heater_length** (float): Specifies the length of the heater along the waveguide. Doesn't include the length of the 180 degree bend.  Defaults to 400.0.\n           * **mt** (MetalTemplate): If 'heater' is true, must specify a Metal Template that defines heater & heater cladding layers.\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the taper will point *towards*, must be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians).  Defaults to `'EAST'` (0 radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input_top'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['input_bot'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output_top'] = {'port': (x2, y2), 'direction': 'dir2'}\n           * portlist['output_bot'] = {'port': (x3, y3), 'direction': 'dir3'}\n           * portlist['heater_top_in'] = {'port', (x4, y4), 'direction': 'dir4'}\n           * portlist['heater_top_out'] = {'port', (x5, y5), 'direction': 'dir5'}\n           * portlist['heater_bot_in'] = {'port', (x6, y6), 'direction': 'dir6'}\n           * portlist['heater_bot_out'] = {'port', (x7, y7), 'direction': 'dir7'}\n\n        Where in the above (x1,y1) is the input port, (x2, y2) is the top output port, (x3, y3) is the bottom output port, and the directions are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n        Four additional ports are created for the heaters if the `heater` argument is True.  Metals are not generated, but should be connected to the specified 'heater' ports.\n\n    "

    def __init__(self, wgt, DC1length, DC1gap, DC2length, DC2gap, angle=np.pi / 6.0, arm1=0, arm2=0, heater=False, heater_length=400, mt=None, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'MachZehnderSwitchDC2x2', locals())
        self.portlist = {}
        self.wgt = wgt
        self.arm1 = arm1
        self.arm2 = arm2
        if angle > np.pi / 2.0 or angle < 0:
            raise ValueError('Warning! Improper angle specified (' + str(angle) + ').  Must be between 0 and pi/2.0.')
        else:
            self.angle = angle
            self.DC1length = DC1length
            self.DC1gap = DC1gap
            self.DC2length = DC2length
            self.DC2gap = DC2gap
            padding = 0.01
            dlx = abs(self.wgt.bend_radius * np.tan(self.angle / 2.0))
            self.angle_x_dist = 2 * dlx + 2.0 * (dlx + padding) * np.cos(self.angle)
            self.angle_y_dist = 2.0 * (dlx + padding) * np.sin(self.angle)
            self.dc1length = self.DC1length + 2 * self.angle_x_dist
            self.dc2length = self.DC2length + 2 * self.angle_x_dist
            self.heater = heater
            if heater:
                self.heater_length = heater_length
                self.mt = mt
            else:
                self.heater_length = 0
        self.port = port
        self.direction = direction
        self._MachZehnderSwitchDC2x2__build_cell()
        self._MachZehnderSwitchDC2x2__build_ports()
        self._auto_transform_()

    def __build_cell(self):
        dc_in = DirectionalCoupler((self.wgt),
          (self.DC1length),
          (self.DC1gap),
          angle=(self.angle),
          port=(0, 0),
          direction='EAST')
        dc_out = DirectionalCoupler((self.wgt),
          (self.DC2length),
          (self.DC2gap),
          angle=(self.angle),
          port=(
         self.dc1length + self.dc2length + 4 * self.wgt.bend_radius,
         -self.DC2gap - self.wgt.wg_width - 2 * self.angle_y_dist),
          direction='WEST')
        y_end_top, y_end_bot = dc_out.portlist['output_top']['port'][1], dc_out.portlist['output_bot']['port'][1]
        x0, y0 = dc_in.portlist['output_top']['port']
        trace1 = [
         (
          x0, y0),
         (
          x0 + self.wgt.bend_radius, y0),
         (
          x0 + self.wgt.bend_radius,
          y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
         (
          x0 + 3 * self.wgt.bend_radius,
          y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
         (
          x0 + 3 * self.wgt.bend_radius, y_end_bot),
         (
          x0 + 4 * self.wgt.bend_radius, y_end_bot)]
        wg_top = Waveguide(trace1, self.wgt)
        x1, y1 = dc_in.portlist['output_bot']['port']
        trace2 = [
         (
          x1, y1),
         (
          x1 + self.wgt.bend_radius, y1),
         (
          x1 + self.wgt.bend_radius,
          y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
         (
          x1 + 3 * self.wgt.bend_radius,
          y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
         (
          x1 + 3 * self.wgt.bend_radius, y_end_top),
         (
          x1 + 4 * self.wgt.bend_radius, y_end_top)]
        wg_bot = Waveguide(trace2, self.wgt)
        if self.heater:
            heater_trace1 = [
             (
              x0 + self.wgt.bend_radius,
              y0 + self.arm1 / 2.0 + self.wgt.bend_radius),
             (
              x0 + self.wgt.bend_radius,
              y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y0 + 2 * self.wgt.bend_radius + self.arm1 / 2.0 + self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y0 + self.arm1 / 2.0 + self.wgt.bend_radius)]
            heater_top = MetalRoute(heater_trace1, self.mt)
            heater_trace2 = [
             (
              x0 + self.wgt.bend_radius,
              y1 - self.arm2 / 2.0 - self.wgt.bend_radius),
             (
              x0 + self.wgt.bend_radius,
              y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y1 - 2 * self.wgt.bend_radius - self.arm2 / 2.0 - self.heater_length / 2.0),
             (
              x0 + 3 * self.wgt.bend_radius,
              y1 - self.arm2 / 2.0 - self.wgt.bend_radius)]
            heater_bot = MetalRoute(heater_trace2, self.mt)
        totalxlen = self.dc1length + self.dc2length + 4 * self.wgt.bend_radius
        dy_output = self.DC2gap / 2.0 + self.wgt.wg_width / 2.0 + self.angle_y_dist
        dy_input = self.DC1gap / 2.0 + self.wgt.wg_width / 2.0 + self.angle_y_dist
        self.port_output_top = (
         totalxlen, 0)
        self.port_output_bot = (totalxlen, -2 * dy_output)
        self.port_input_top = (0.0, 0.0)
        self.port_input_bot = (0.0, -2 * dy_input)
        self.htr_top_in_dir = 'WEST'
        self.htr_top_out_dir = 'EAST'
        self.htr_bot_in_dir = 'WEST'
        self.htr_bot_out_dir = 'EAST'
        components = [
         dc_in, dc_out, wg_top, wg_bot]
        if self.heater:
            components.append(heater_top)
            components.append(heater_bot)
            self.htr_top_in = (
             x0 + self.wgt.bend_radius,
             y0 + self.arm1 / 2.0 + self.wgt.bend_radius + self.mt.width / 2.0)
            self.htr_top_out = (
             x0 + 3 * self.wgt.bend_radius,
             y0 + self.arm1 / 2.0 + self.wgt.bend_radius + self.mt.width / 2.0)
            self.htr_bot_in = (
             x0 + self.wgt.bend_radius,
             y1 - self.arm2 / 2.0 - self.wgt.bend_radius - self.mt.width / 2.0)
            self.htr_bot_out = (
             x0 + 3 * self.wgt.bend_radius,
             y1 - self.arm2 / 2.0 - self.wgt.bend_radius - self.mt.width / 2.0)
        for c in components:
            self.add(c)

    def __build_ports(self):
        self.portlist['input_top'] = {'port':self.port_input_top, 
         'direction':'WEST'}
        self.portlist['input_bot'] = {'port':self.port_input_bot,  'direction':'WEST'}
        self.portlist['output_top'] = {'port':self.port_output_top, 
         'direction':'EAST'}
        self.portlist['output_bot'] = {'port':self.port_output_bot, 
         'direction':'EAST'}
        if self.heater:
            self.portlist['heater_top_in'] = {'port':self.htr_top_in,  'direction':self.htr_top_in_dir}
            self.portlist['heater_top_out'] = {'port':self.htr_top_out, 
             'direction':self.htr_top_out_dir}
            self.portlist['heater_bot_in'] = {'port':self.htr_bot_in, 
             'direction':self.htr_bot_in_dir}
            self.portlist['heater_bot_out'] = {'port':self.htr_bot_out, 
             'direction':self.htr_bot_out_dir}


if __name__ == '__main__':
    from . import *
    top = gdspy.Cell('top')
    wgt = WaveguideTemplate(bend_radius=50, wg_width=1.0, resist='+')
    htr_mt = MetalTemplate(width=25,
      clad_width=25,
      bend_radius=(wgt.bend_radius),
      resist='+',
      fab='ETCH',
      metal_layer=13,
      metal_datatype=0,
      clad_layer=14,
      clad_datatype=0)
    mt = MetalTemplate(width=25,
      clad_width=25,
      resist='+',
      fab='ETCH',
      metal_layer=11,
      metal_datatype=0,
      clad_layer=12,
      clad_datatype=0)
    wg_in = Waveguide([(0, 0), (300, 0)], wgt)
    tk.add(top, wg_in)
    mzi = MachZehnderSwitchDC2x2(
 wgt, DC1length=200, 
     DC1gap=0.5, 
     DC2length=100, 
     DC2gap=1.5, 
     arm1=500, 
     arm2=500, 
     heater=True, 
     heater_length=400, 
     mt=htr_mt, **wg_in.portlist['output'])
    tk.add(top, mzi)
    x_to, y_to = mzi.portlist['output_top']['port']
    wg_out_top = Waveguide([
     (
      x_to, y_to),
     (
      x_to + wgt.bend_radius * 0.75, y_to),
     (
      x_to + 1.5 * wgt.bend_radius, y_to + wgt.bend_radius),
     (
      x_to + wgt.bend_radius + 300, y_to + wgt.bend_radius)], wgt)
    tk.add(top, wg_out_top)
    x_bo, y_bo = mzi.portlist['output_bot']['port']
    wg_out_bot = Waveguide([
     (
      x_bo, y_bo),
     (
      x_bo + wgt.bend_radius * 0.75, y_bo),
     (
      x_bo + 1.5 * wgt.bend_radius, y_bo - wgt.bend_radius),
     (
      x_bo + wgt.bend_radius + 300, y_bo - wgt.bend_radius)], wgt)
    tk.add(top, wg_out_bot)
    gdspy.LayoutViewer(cells=top, depth=4)