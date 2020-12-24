# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\compare\spec_dtw.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\ncompare signals using time-warped spectrograms\n\nCopyright (C) 2011 Daniel Meliza <dan // meliza.org>\nCreated 2011-08-30\n'
from chirp.compare.feat_dtw import feat_dtw
from chirp.compare.spcc import spcc

class spec_dtw(feat_dtw, spcc):
    """
    Compute pairwise distances between signals using a dynamic
    time-warping variant of spcc. Like SPCC, the signal representation
    is a set of spectrographic frames; a matrix of similarities is
    calculated between each pair of frames in the two signals using
    the cross-correlation between frames, and then the DTW algorithm
    tries to find the optimal path.
    """
    _descr = 'DTW of spectrograms (requires wav; ebl optional)'
    file_extension = '.wav'
    options = dict(feat_dtw.options, metric='cosine', **spcc.options)
    config_sections = ('spectrogram', 'dtw', 'spcc', 'spec_dtw')

    def __init__(self, configfile=None, **kwargs):
        self.readconfig(configfile)
        self.options.update(kwargs)

    def load_signal(self, locator, *args, **kwargs):
        return spcc.load_signal(self, locator, *args, **kwargs).T

    def options_str(self):
        return spcc.options_str(self) + '\n' + feat_dtw.options_str(self)