# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\bbend.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 5623 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk
import math

class BBend(tk.Component):
    __doc__ = " Bezier Cell class.  Creates a Bezier waveguide bend that can be used in waveguide routing.  The number of points is computed based on the waveguide template grid resolution to automatically minimize grid errors.\n        \n        See https://en.wikipedia.org/wiki/Bezier_curve for more information.\n    \n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **poles** (list): List of (x,y) pole coordinates used for routing the Bezier curve\n\n        Keyword Args:\n           * **start_width** (float): If a value is provided, overrides the initial waveguide width (otherwise the width is taken from the WaveguideTemplate object).  Currently only works for strip waveguides.\n           * **end_width** (float): If a value is provided, overrides the final waveguide width (otherwise the width is taken from the WaveguideTemplate object).  Currently only works for strip waveguides.\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output'] = {'port': (x2, y2), 'direction': 'dir2'}\n\n        Where in the above (x1,y1) is the same as the 'port' input, (x2, y2) is the end of the taper, and 'dir1', 'dir2' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n    "

    def __init__(self, wgt, poles, start_width=None, end_width=None):
        tk.Component.__init__(self, 'BBend', locals())
        self.portlist = {}
        self.port = (0, 0)
        if start_width != None:
            self.start_width = start_width
        else:
            self.start_width = wgt.wg_width
        if end_width != None:
            self.end_width = end_width
        else:
            self.end_width = wgt.wg_width
        self.input_port = (poles[0][0], poles[0][1])
        self.output_port = (poles[(-1)][0], poles[(-1)][1])
        self.poles = poles
        self.input_direction = tk.get_exact_angle(poles[1], poles[0])
        self.output_direction = tk.get_exact_angle(poles[(-2)], poles[(-1)])
        self.wgt = wgt
        self.wg_spec = {'layer':wgt.wg_layer,  'datatype':wgt.wg_datatype}
        self.clad_spec = {'layer':wgt.clad_layer,  'datatype':wgt.clad_datatype}
        self._BBend__build_cell()
        self._BBend__build_ports()

    def _bezier_function(self, t):
        n = len(self.poles) - 1
        x, y = (0, 0)
        for i in range(n + 1):
            coeff = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
            x += coeff * (1 - t) ** (n - i) * t ** i * self.poles[i][0]
            y += coeff * (1 - t) ** (n - i) * t ** i * self.poles[i][1]

        return (
         x, y)

    def __build_cell(self):
        wg = gdspy.Path(self.start_width, (0, 0))
        (wg.parametric)(
 self._bezier_function, final_width=self.end_width, 
         tolerance=self.wgt.grid / 2.0, 
         max_points=199, **self.wg_spec)
        self.add(wg)
        for i in range(len(self.wgt.waveguide_stack) - 1):
            cur_width = self.wgt.waveguide_stack[(i + 1)][0]
            cur_spec = {'layer':self.wgt.waveguide_stack[(i + 1)][1][0], 
             'datatype':self.wgt.waveguide_stack[(i + 1)][1][1]}
            clad = gdspy.Path(cur_width, (0, 0))
            (clad.parametric)(
 self._bezier_function, tolerance=self.wgt.grid / 2.0, 
             max_points=199, **cur_spec)
            self.add(clad)

    def __build_ports(self):
        self.portlist['input'] = {'port':self.input_port, 
         'direction':self.input_direction}
        self.portlist['output'] = {'port':self.output_port, 
         'direction':self.output_direction}


if __name__ == '__main__':
    from . import *
    top = gdspy.Cell('top')
    wgt = WaveguideTemplate(bend_radius=50, resist='+')
    wg1 = Waveguide([(0, 0), (25, 0)], wgt)
    tk.add(top, wg1)
    bb1 = BBend(wgt, [(25, 0), (125, 0), (125, 100), (225, 100)])
    tk.add(top, bb1)
    x, y = bb1.portlist['output']['port']
    wg2 = Waveguide([(x, y), (x + 25, y)], wgt)
    tk.add(top, wg2)
    gdspy.LayoutViewer(cells=top, depth=3)