# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/make_histo_ofallpixels.py
# Compiled at: 2018-09-14 09:20:48
# Size of source mod 2**32: 828 bytes
try:
    import ROOT
    ROOTfound = True
except ImportError:
    ROOTfound = False
    print('WARNING make_histo_ofallpixels.py: ROOT not found')

import numpy as np, numpy as np
from dicom_tools.hist_match import match_all

def make_histo_ofallpixels(data, suffix='', verbose=False, normalize=False):
    nbin = 1000
    if normalize:
        datan = match_all(data)
    else:
        datan = data
    binmin = data.min() * 0.8
    binmax = data.max() * 1.2
    nFette = len(data)
    allhistos = []
    for layer in xrange(0, nFette):
        fetta = data[layer]
        thishisto = ROOT.TH1F('h' + str(layer) + suffix, 'h' + str(layer), nbin, binmin, binmax)
        for val in fetta.ravel():
            thishisto.Fill(val)

        allhistos.append(thishisto)

    return allhistos