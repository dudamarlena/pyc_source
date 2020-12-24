# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\taper.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 4400 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk

class Taper(tk.Component):
    __doc__ = " Taper Cell class.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **length** (float): Length of the taper\n           * **end_width** (float): Final width of the taper (initial width received from WaveguieTemplate)\n\n        Keyword Args:\n           * **start_width** (float): Beginning width of the taper.  Defaults to the waveguide width provided by the WaveguideTemplate object.\n           * **end_clad_width** (float): Clad width at the end of the taper.  Defaults to the regular clad width.\n           * **extra_clad_length** (float): Extra cladding beyond the end of the taper.  Defaults to 0.\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians).\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output'] = {'port': (x2, y2), 'direction': 'dir2'}\n\n        Where in the above (x1,y1) is the same as the 'port' input, (x2, y2) is the end of the taper, and 'dir1', 'dir2' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n    "

    def __init__(self, wgt, length, end_width, start_width=None, end_clad_width=None, extra_clad_length=0, port=(0, 0), direction='EAST'):
        tk.Component.__init__(self, 'Taper', locals())
        self.portlist = {}
        self.port = port
        self.direction = direction
        self.length = length
        self.end_width = end_width
        self.start_width = wgt.wg_width if start_width == None else start_width
        self.end_clad_width = wgt.clad_width if end_clad_width == None else end_clad_width
        self.extra_clad_length = extra_clad_length
        self.wgt = wgt
        self.wg_spec = {'layer':wgt.wg_layer,  'datatype':wgt.wg_datatype}
        self.clad_spec = {'layer':wgt.clad_layer,  'datatype':wgt.clad_datatype}
        self._Taper__build_cell()
        self._Taper__build_ports()
        self._auto_transform_()

    def __build_cell(self):
        path = gdspy.Path(self.start_width, (0, 0))
        (path.segment)(
 self.length, direction=0.0, final_width=self.end_width, **self.wg_spec)
        path2 = gdspy.Path(2 * self.wgt.clad_width + self.wgt.wg_width, (0, 0))
        (path2.segment)(
 self.length, direction=0.0, 
         final_width=2 * self.end_clad_width + self.end_width, **self.clad_spec)
        (path2.segment)((self.extra_clad_length), **self.clad_spec)
        self.add(path)
        self.add(path2)

    def __build_ports(self):
        self.portlist['input'] = {'port':(0, 0), 
         'direction':'WEST'}
        self.portlist['output'] = {'port':(self.length, 0),  'direction':'EAST'}


if __name__ == '__main__':
    from . import *
    top = gdspy.Cell('top')
    wgt = WaveguideTemplate(bend_radius=50, resist='+')
    wg1 = Waveguide([(0, 0), (100, 40)], wgt)
    tk.add(top, wg1)
    tp1 = Taper(wgt, 100.0, 0.3, end_clad_width=50, **wg1.portlist['input'])
    tp2 = Taper(wgt, 100.0, 0.5, end_clad_width=15, **wg1.portlist['output'])
    tk.add(top, tp1)
    tk.add(top, tp2)
    gdspy.LayoutViewer()