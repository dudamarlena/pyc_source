# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/roi2myroi.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 958 bytes
from __future__ import print_function
import numpy as np
from scipy.spatial import ConvexHull
import dicom_tools.pyqtgraph as pg

def roi2myroi(ROI, verbose=False):
    rois = [None] * len(ROI)
    firsttime = True
    for layer in xrange(0, len(ROI)):
        fetta = ROI[layer]
        apoints = []
        if fetta.max() > 0:
            for j, riga in enumerate(fetta):
                for i, elemento in enumerate(riga):
                    if elemento:
                        thispoint = [
                         i, j]
                        apoints.append(thispoint)

            points = np.array(apoints)
            if firsttime:
                firsttime = False
                for point in points:
                    print(point)

            hull = ConvexHull(points)
            rois[layer] = pg.PolyLineROI((hull.simplices.tolist()), pen=(6, 9), closed=True).saveState()

    return rois