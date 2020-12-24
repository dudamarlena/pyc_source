# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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