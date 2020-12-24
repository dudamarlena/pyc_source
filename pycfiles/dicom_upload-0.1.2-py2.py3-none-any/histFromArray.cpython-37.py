# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/histFromArray.py
# Compiled at: 2018-09-14 09:20:48
# Size of source mod 2**32: 677 bytes
import numpy as np
try:
    import ROOT
    ROOTfound = True
except ImportError:
    ROOTfound = False
    print('WARNING histFromArray.py: ROOT not found')

def histFromArray(array, nbin=100, name='h', verbose=False):
    if len(array[np.nonzero(array)]) == 0:
        return
    minval = np.min(array[np.nonzero(array)])
    maxval = np.max(array)
    if verbose:
        print('histFromArray creating histogram', name, 'with', nbin, 'bin')
    h = ROOT.TH1F(name, name, nbin, minval * 0.9, maxval * 1.1)
    for val in array.ravel():
        h.Fill(val)

    return h