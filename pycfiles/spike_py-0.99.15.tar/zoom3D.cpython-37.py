# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/zoom3D.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 2516 bytes
"""Code to display 2D data-sets in interactive 3D, using Mayavi

Original code from Alice Lynch - mai 2016

adapted my M-A Delsuc
"""
from __future__ import print_function
import numpy as np
try:
    from mayavi import mlab
    ok = True
except:
    raise Exception('This plugin requires the installation of Mayavi (http://docs.enthought.com/mayavi/mayavi/installation.html) )')
    print('*** The zoom3D plugin requires the installation of Mayavi (http://docs.enthought.com/mayavi/mayavi/installation.html)')
    ok = False

from spike import NPKError
from spike.NPKData import NPKData_plugin
import spike.NPKData as npk

def zoom3D(npkd, zoom, fontsize=0.7, font='times', colormap='blue-red', showaxes=True):
    """
    use the zoom region and display it in interactive 3D
    
    zoom : f1lo, f1up, f2lo, f2up - expressed in current unit

    remark, use a small zoom region !

    x = axis 2
    y = axis 1
    z = intensity
    """
    z1lo, z1up, z2lo, z2up = npk.parsezoom(npkd, zoom)
    d5 = np.zeros((z2up - z2lo + 1, z1up - z1lo + 1))
    for i in range(z2lo, z2up + 1):
        cc = npkd.col(i)
        d5[i - z2lo, :] = cc[z1lo:z1up + 1]

    zmax = np.amax(d5)
    zmin = np.amin(d5)
    xmin = zoom[2]
    xmax = zoom[3]
    ymin = zoom[0]
    ymax = zoom[1]
    mlab.figure(bgcolor=(1.0, 1.0, 1.0), fgcolor=(0.0, 0.0, 0.0))
    mlab.surf(d5, extent=[0, 1000, 0, 1000, 0, 1000], warp_scale='auto', colormap=colormap)
    ax = mlab.axes(x_axis_visibility=showaxes, y_axis_visibility=showaxes, z_axis_visibility=showaxes, xlabel=('F2 ' + npkd.axis2.currentunit), ylabel=('F1 ' + npkd.axis1.currentunit), zlabel='Intensity', ranges=[xmin, xmax, ymin, ymax, zmin, zmax], nb_labels=5)
    ax.label_text_property.font_family = font
    ax.title_text_property.font_family = font
    ax.axes.font_factor = fontsize


if ok:
    NPKData_plugin('zoomwindow', zoom3D)