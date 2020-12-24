# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prabhu/src/git/VTKPythonPackage/VTK-osx_2.7/Wrapping/Python/vtk/tk/vtkTkPhotoImage.py
# Compiled at: 2018-11-28 17:07:58
"""
A subclass of tkinter.PhotoImage that connects a
vtkImageData to a photo widget.

Created by Daniel Blezek, August 2002
"""
from __future__ import absolute_import
import sys
if sys.hexversion < 50331648:
    import Tkinter as tkinter
else:
    import tkinter
from .vtkLoadPythonTkWidgets import vtkLoadPythonTkWidgets

class vtkTkPhotoImage(tkinter.PhotoImage):
    """
    A subclass of PhotoImage with helper functions
    for displaying vtkImageData
    """

    def __init__(self, **kw):
        tkinter.PhotoImage.__init__(self, kw)
        vtkLoadPythonTkWidgets(self.tk)

    def PutImageSlice(self, image, z, orientation='transverse', window=256, level=128):
        t = str(image.__this__)
        s = 'vtkImageDataToTkPhoto %s %s %d %s %d %d' % (t, self.name, z, orientation, window, level)
        self.tk.eval(s)