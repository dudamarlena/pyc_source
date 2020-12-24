# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/connect_filter.py
# Compiled at: 2012-04-18 08:45:31
from __future__ import division
import vtk, gtk
from gtkutils import ProgressBarDialog

class ConnectFilter(vtk.vtkPolyDataConnectivityFilter):
    """
    CLASS: ConnectFilter
    DESCR: Public attrs

      mode : the extraction mode as int
    """
    mode2num = {'Point Seeded Regions': 1, 
       'Cell Seeded Regions': 2, 
       'Specified Regions': 3, 
       'Largest Region': 4, 
       'All Regions': 5, 
       'Closest Point Region': 6}
    num2mode = dict([ (v, k) for k, v in mode2num.items() ])
    mode = 5

    def __init__(self):
        prog = ProgressBarDialog(title='Rendering surface', parent=None, msg='Computing connectivity ....', size=(300,
                                                                                                                  40))
        prog.set_modal(True)

        def start(o, event):
            prog.show()
            while gtk.events_pending():
                gtk.main_iteration()

        def progress(o, event):
            val = o.GetProgress()
            prog.bar.set_fraction(val)
            while gtk.events_pending():
                gtk.main_iteration()

        def end(o, event):
            prog.hide()
            while gtk.events_pending():
                gtk.main_iteration()

        self.AddObserver('StartEvent', start)
        self.AddObserver('ProgressEvent', progress)
        self.AddObserver('EndEvent', end)
        return

    def update(self):
        self.SetExtractionMode(self.mode)