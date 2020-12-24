# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\sbend.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 4374 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk

class SBend(tk.Component):
    __doc__ = " Sinusoidal S-shaped Bend Cell class.  Creates a sinusoidal waveguide bend that can be used in waveguide routing.  The number of points is computed based on the waveguide template grid resolution to automatically minimize grid errors.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **length** (float): Length of the S-bend\n           * **height** (float): Height of the S-bend\n\n        Keyword Args:\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output'] = {'port': (x2, y2), 'direction': 'dir2'}\n\n        Where in the above (x1,y1) is the same as the 'port' input, (x2, y2) is the end of the taper, and 'dir1', 'dir2' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n    "

    def __init__(self, wgt, length, height, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'SBend', locals())
        self.port = port
        self.portlist = {}
        self.direction = direction
        self.input_port = (0, 0)
        self.output_port = (length, height)
        self.wgt = wgt
        self.wg_spec = {'layer':wgt.wg_layer,  'datatype':wgt.wg_datatype}
        self.clad_spec = {'layer':wgt.clad_layer,  'datatype':wgt.clad_datatype}
        self._SBend__build_cell()
        self._SBend__build_ports()
        self._auto_transform_()

    def __sine_function(self, t):
        return (
         self.output_port[0] * t,
         0.5 * self.output_port[1] * np.sin(np.pi * t - 0.5 * np.pi) + 0.5 * self.output_port[1])

    def __build_cell(self):
        wg = gdspy.Path(self.wgt.wg_width, (0, 0))
        (wg.parametric)(
 self._SBend__sine_function, tolerance=self.wgt.grid / 2.0, 
         max_points=199, **self.wg_spec)
        self.add(wg)
        for i in range(len(self.wgt.waveguide_stack) - 1):
            cur_width = self.wgt.waveguide_stack[(i + 1)][0]
            cur_spec = {'layer':self.wgt.waveguide_stack[(i + 1)][1][0], 
             'datatype':self.wgt.waveguide_stack[(i + 1)][1][1]}
            clad = gdspy.Path(cur_width, (0, 0))
            (clad.parametric)(
 self._SBend__sine_function, tolerance=self.wgt.grid / 2.0, 
             max_points=199, **cur_spec)
            self.add(clad)

    def __build_ports(self):
        self.portlist['input'] = {'port':self.input_port, 
         'direction':'WEST'}
        self.portlist['output'] = {'port':self.output_port,  'direction':'EAST'}


if __name__ == '__main__':
    from . import *
    top = gdspy.Cell('top')
    wgt = WaveguideTemplate(bend_radius=50, resist='+')
    wg1 = Waveguide([(0, 0), (100, 0)], wgt)
    tk.add(top, wg1)
    sb1 = SBend(wgt, 200.0, 100.0, **wg1.portlist['output'])
    tk.add(top, sb1)
    x, y = sb1.portlist['output']['port']
    wg2 = Waveguide([(x, y), (x + 100, y)], wgt)
    tk.add(top, wg2)
    gdspy.LayoutViewer(cells=top, depth=3)