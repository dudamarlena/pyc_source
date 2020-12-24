# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/DataSources/Holstege.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = '\nInterface to Yeast Transcription Data from Holstege et al. Cell 1998\n\nCopyright (2005) Whitehead Institute for Biomedical Research (except as noted below)\nAll Rights Reserved\n\nAuthor: David Benjamin Gordon\n\n'
import sys, re, os, math, time, string, tempfile, TAMO.paths
_transcriptome_file = TAMO.paths.Holstegedir + 'orf_transcriptome.txt'
TAMO.paths.CHECK(_transcriptome_file, 'Holstege')
_orf2expression = {}
_orf2halflife = {}
_orf2transfreq = {}

def _load_transcriptome():
    FID = open(_transcriptome_file, 'r')
    lines = [ x.strip() for x in FID.readlines() ]
    FID.close()
    del lines[0]
    for line in lines:
        toks = line.split()
        orf = toks[0]
        el = toks[1]
        hl = toks[2]
        tf = toks[3]
        if el.find('#') == -1:
            _orf2expression[orf] = float(el)
        if hl.find('#') == -1:
            _orf2halflife[orf] = float(hl)
        if tf.find('#') == -1:
            _orf2transfreq[orf] = float(tf)


def orf2expression(orf):
    return _result(_orf2expression, orf)


def orf2halflife(orf):
    return _result(_orf2halflife, orf)


def orf2transfreq(orf):
    return _result(_orf2transfreq, orf)


def _result(D, key):
    if not D:
        _load_transcriptome()
    if D.has_key(key):
        return D[key]
    else:
        return
        return