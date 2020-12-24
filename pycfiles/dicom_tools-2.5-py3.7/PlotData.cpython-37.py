# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/PlotData.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1572 bytes


class PlotData(object):
    __doc__ = "\n    Class used for managing plot data\n      - allows data sharing between multiple graphics items (curve, scatter, graph..)\n      - each item may define the columns it needs\n      - column groupings ('pos' or x, y, z)\n      - efficiently appendable \n      - log, fft transformations\n      - color mode conversion (float/byte/qcolor)\n      - pen/brush conversion\n      - per-field cached masking\n        - allows multiple masking fields (different graphics need to mask on different criteria) \n        - removal of nan/inf values\n      - option for single value shared by entire column\n      - cached downsampling\n      - cached min / max / hasnan / isuniform\n    "

    def __init__(self):
        self.fields = {}
        self.maxVals = {}
        self.minVals = {}

    def addFields(self, **fields):
        for f in fields:
            if f not in self.fields:
                self.fields[f] = None

    def hasField(self, f):
        return f in self.fields

    def __getitem__(self, field):
        return self.fields[field]

    def __setitem__(self, field, val):
        self.fields[field] = val

    def max(self, field):
        mx = self.maxVals.get(field, None)
        if mx is None:
            mx = np.max(self[field])
            self.maxVals[field] = mx
        return mx

    def min(self, field):
        mn = self.minVals.get(field, None)
        if mn is None:
            mn = np.min(self[field])
            self.minVals[field] = mn
        return mn