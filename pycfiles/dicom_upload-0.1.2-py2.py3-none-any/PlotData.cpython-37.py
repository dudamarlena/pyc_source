# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/PlotData.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1572 bytes


class PlotData(object):
    """PlotData"""

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