# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/decimate_filter.py
# Compiled at: 2012-04-18 08:46:43
from __future__ import division
import sys, os, vtk, gtk
from gtkutils import ProgressBarDialog, str2posnum_or_err

class DecimateFilter(vtk.vtkDecimatePro):
    """
    CLASS: DecimateFilter
    DESCR:
        
    Public attrs:
      targetReduction
      #aspectRatio    
      #initialError   
      #errorIncrement 
      #maxIterations  
      #initialAngle   
    """
    fmts = {'targetReduction': '%1.2f'}
    labels = {'targetReduction': 'Target reduction'}
    converters = {'targetReduction': str2posnum_or_err}
    targetReduction = 0.8

    def __init__(self):
        prog = ProgressBarDialog(title='Rendering surface', parent=None, msg='Decimating data....', size=(300,
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
        self.SetTargetReduction(self.targetReduction)