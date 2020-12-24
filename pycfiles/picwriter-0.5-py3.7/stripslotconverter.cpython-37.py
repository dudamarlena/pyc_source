# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\stripslotconverter.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 9650 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk

class StripSlotConverter(tk.Component):
    __doc__ = " Strip-to-Slot Side Converter Cell class.  Adiabatically transforms a strip to a slot waveguide mode, with two sections.  Section 1 introduces a narrow waveguide alongside the input strip waveguide and gradually lowers the gap between the strip waveguide and narrow side waveguide.  Section 2 gradually converts the widths of the two waveguides until they are equal to the slot rail widths.  \n\n        Args:\n           * **wgt_input** (WaveguideTemplate):  WaveguideTemplate object for the input waveguide (should be either of type `strip` or `slot`).\n           * **wgt_output** (WaveguideTemplate):  WaveguideTemplate object for the output waveguide (should be either of type `strip` or `slot`, opposite of the input type).\n           * **length1** (float): Length of section 1 that gradually changes the distance between the two waveguides.\n           * **length2** (float): Length of section 2 that gradually changes the widths of the two waveguides until equal to the slot waveguide rail widths.\n           * **start_rail_width** (float): Width of the narrow waveguide appearing next to the strip waveguide.\n           * **end_strip_width** (float): Width of the strip waveguide at the end of `length1` and before `length2`\n           * **d** (float): Distance between the outer edge of the strip waveguide and the start of the slot waveguide rail.\n\n        Keyword Args:\n           * **input_strip** (Boolean): If `True`, sets the input port to be the strip waveguide side.  If `False`, slot waveguide is on the input.  Defaults to `None`, in which case the input port waveguide template is used to choose.\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output'] = {'port': (x2, y2), 'direction': 'dir2'}\n\n        Where in the above (x1,y1) is the same as the 'port' input, (x2, y2) is the end of the taper, and 'dir1', 'dir2' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n        Note: The waveguide and cladding layer/datatype are taken from the `wgt_slot` by default.\n\n    "

    def __init__(self, wgt_input, wgt_output, length1, length2, start_rail_width, end_strip_width, d, input_strip=None, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'StripSlotConverter', locals())
        self.portlist = {}
        if not isinstance(input_strip, bool):
            if input_strip != None:
                raise ValueError('Invalid input provided for `input_strip`.  Please specify a boolean.')
        elif input_strip == None:
            self.input_strip = wgt_input.wg_type == 'strip' or wgt_input.wg_type == 'swg'
        else:
            self.input_strip = input_strip
        if self.input_strip:
            self.wgt_strip = wgt_input
            self.wgt_slot = wgt_output
        else:
            self.wgt_strip = wgt_output
            self.wgt_slot = wgt_input
        self.wg_spec = {'layer':wgt_output.wg_layer, 
         'datatype':wgt_output.wg_datatype}
        self.clad_spec = {'layer':wgt_output.clad_layer, 
         'datatype':wgt_output.clad_datatype}
        self.length1 = length1
        self.length2 = length2
        self.d = d
        self.start_rail_width = start_rail_width
        self.end_strip_width = end_strip_width
        self.port = port
        self.direction = direction
        self._StripSlotConverter__build_cell()
        self._StripSlotConverter__build_ports()
        self._auto_transform_()

    def __build_cell(self):
        x0, y0 = (0, 0)
        pts = [
         (
          x0, y0 - self.wgt_strip.wg_width / 2.0),
         (
          x0, y0 + self.wgt_strip.wg_width / 2.0),
         (
          x0 + self.length1,
          y0 - self.wgt_strip.wg_width / 2.0 + self.end_strip_width),
         (
          x0 + self.length1, y0 - self.wgt_strip.wg_width / 2.0)]
        strip1 = gdspy.Polygon(pts,
          layer=(self.wgt_strip.wg_layer), datatype=(self.wgt_strip.wg_datatype))
        pts = [
         (
          x0, y0 + self.wgt_strip.wg_width / 2.0 + self.d),
         (
          x0, y0 + self.wgt_strip.wg_width / 2.0 + self.d + self.start_rail_width),
         (
          x0 + self.length1,
          y0 - self.wgt_strip.wg_width / 2.0 + self.end_strip_width + self.wgt_slot.slot + self.start_rail_width),
         (
          x0 + self.length1,
          y0 - self.wgt_strip.wg_width / 2.0 + self.end_strip_width + self.wgt_slot.slot)]
        thin_strip = gdspy.Polygon(pts,
          layer=(self.wgt_strip.wg_layer), datatype=(self.wgt_strip.wg_datatype))
        pts = [
         (
          x0 + self.length1,
          y0 - self.wgt_strip.wg_width / 2.0 + self.end_strip_width),
         (
          x0 + self.length1, y0 - self.wgt_strip.wg_width / 2.0),
         (
          x0 + self.length1 + self.length2, y0 - self.wgt_slot.wg_width / 2.0),
         (
          x0 + self.length1 + self.length2,
          y0 - self.wgt_slot.wg_width / 2.0 + self.wgt_slot.rail)]
        rail1 = gdspy.Polygon(pts,
          layer=(self.wgt_strip.wg_layer), datatype=(self.wgt_strip.wg_datatype))
        pts = [
         (
          x0 + self.length1,
          y0 - self.wgt_strip.wg_width / 2.0 + self.end_strip_width + self.wgt_slot.slot + self.start_rail_width),
         (
          x0 + self.length1,
          y0 - self.wgt_strip.wg_width / 2.0 + self.end_strip_width + self.wgt_slot.slot),
         (
          x0 + self.length1 + self.length2,
          y0 + self.wgt_slot.wg_width / 2.0 - self.wgt_slot.rail),
         (
          x0 + self.length1 + self.length2, y0 + self.wgt_slot.wg_width / 2.0)]
        rail2 = gdspy.Polygon(pts,
          layer=(self.wgt_strip.wg_layer), datatype=(self.wgt_strip.wg_datatype))
        pts = [
         (
          x0, y0 + self.wgt_strip.clad_width + self.wgt_strip.wg_width / 2.0),
         (
          x0 + self.length1 + self.length2,
          y0 + self.wgt_slot.clad_width + self.wgt_slot.wg_width / 2.0),
         (
          x0 + self.length1 + self.length2,
          y0 - self.wgt_slot.clad_width - self.wgt_slot.wg_width / 2.0),
         (
          x0, y0 - self.wgt_strip.clad_width - self.wgt_strip.wg_width / 2.0)]
        clad = gdspy.Polygon(pts,
          layer=(self.wgt_strip.clad_layer), datatype=(self.wgt_strip.clad_datatype))
        self.add(strip1)
        self.add(thin_strip)
        self.add(rail1)
        self.add(rail2)
        self.add(clad)

    def __build_ports(self):
        self.portlist['input'] = {'port':(0, 0), 
         'direction':'WEST'}
        self.portlist['output'] = {'port':(
          self.length1 + self.length2, 0), 
         'direction':'EAST'}


if __name__ == '__main__':
    from . import *
    top = gdspy.Cell('top')
    wgt_strip = WaveguideTemplate(bend_radius=50, wg_type='strip', wg_width=0.7)
    wgt_slot = WaveguideTemplate(bend_radius=50, wg_type='slot', wg_width=0.7, slot=0.2)
    wg1 = Waveguide([(0, 0), (100, 0)], wgt_strip)
    tk.add(top, wg1)
    ssc = StripSlotConverter(
 wgt_strip,
 wgt_slot, length1=15.0, 
     length2=15.0, 
     start_rail_width=0.1, 
     end_strip_width=0.4, 
     d=1.0, **wg1.portlist['output'])
    tk.add(top, ssc)
    x1, y1 = ssc.portlist['output']['port']
    wg2 = Waveguide([(x1, y1), (x1 + 100, y1)], wgt_slot)
    tk.add(top, wg2)
    gdspy.LayoutViewer(cells=top)