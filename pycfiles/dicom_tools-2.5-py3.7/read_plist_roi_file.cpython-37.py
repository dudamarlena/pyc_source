# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/read_plist_roi_file.py
# Compiled at: 2018-09-14 09:39:29
# Size of source mod 2**32: 900 bytes
import plistlib
import dicom_tools.pyqtgraph as pg

def read_plist_roi_file(fname, debug=False):
    with open(fname, 'rb') as (fp):
        pl = plistlib.load(fp)
        outrois = [None] * pl['Images'][0]['ImageTotalNum']
        nRois = 0
        for image in pl['Images']:
            points = image['ROIs'][0]['Point_px']
            outpoints = []
            for point in points:
                if debug:
                    print(point, type(point))
                px = float(point.split(',')[0][1:])
                py = image['ImageHeight'] - float(point.split(',')[1][:-1])
                if debug:
                    print(px, py)
                outpoints.append([px, py])

            if debug:
                print(image['ImageIndex'], outpoints)
            outrois[image['ImageIndex']] = pg.PolyLineROI(outpoints, closed=True).saveState()
            nRois += 1

    return (
     outrois, nRois)