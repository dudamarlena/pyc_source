# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\compare\pitch_dtw.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\ncompare signals using dynamic time warping (or CC) of pitch traces\n\nCopyright (C) 2011 Daniel Meliza <dan // meliza.org>\nCreated 2011-08-30\n'
from chirp.common import postfilter
from chirp.common.config import _configurable
from chirp.compare.base_comparison import base_comparison
from chirp.compare.feat_dtw import feat_dtw

class pitch_dtw(feat_dtw):
    """
    Compute pairwise distances between motifs using dynamic time
    warping of the pitch traces. Configurable options:

    estimator:    the estimator to use
    metric:       the metric for comparing pairs of time points in pitch traces
    cost_matrix:  the cost matrix controlling moves through the metric space
    dynamic_cost: use dynamic cost matrix to ensure finite distances

    Additional options specify the degree of postfiltering; see
    common.postfilter.pitchfilter
    """
    _descr = 'dynamic time warping of pitch traces (requires .plg files)'
    file_extension = '.plg'
    options = dict(estimator='p.map', **feat_dtw.options)
    config_sections = ('spectrogram', 'dtw', 'pitch_dtw')

    def __init__(self, configfile=None, **kwargs):
        feat_dtw.__init__(self, configfile=configfile, **kwargs)
        self.readconfig(configfile)
        self.options.update(kwargs)
        self.filter = postfilter.pitchfilter(configfile=configfile, **kwargs)

    def load_signal(self, locator, cout=None):
        return _load_plg(locator, self.filter, self.options['estimator'])

    def options_str(self):
        out = feat_dtw.options_str(self) + '\n** Estimator = %(estimator)s' % self.options
        return out


class pitch_cc(base_comparison, _configurable):
    """
    Compute pairwise distances between motifs using peak cross-correlation of
    the pitch traces. Configurable options:

    estimator:    the estimator to use
    """
    _descr = 'dynamic time warping of pitch traces (requires .plg files)'
    file_extension = '.plg'
    options = dict(estimator='p.map')
    config_sections = 'pitch_cc'

    def __init__(self, configfile=None, **kwargs):
        self.readconfig(configfile)
        self.options.update(kwargs)
        self.filter = postfilter.pitchfilter(configfile=configfile, **kwargs)

    def load_signal(self, locator, cout=None):
        return _load_plg(locator, self.filter, self.options['estimator'])

    def compare(self, ref, tgt):
        from chirp.compare.spcc import spectcc
        R = ref - ref.mean()
        T = tgt - tgt.mean()
        return (
         spectcc(R, T, biased_norm=True).sum(0).max(),)

    def options_str(self):
        out = '** Estimator = %(estimator)s' % self.options
        return out

    @property
    def compare_stat_fields(self):
        """ Return a tuple of the names for the statistics returned by compare() """
        return ('pcc', )


def _load_plg(locator, filt, estimator):
    """
    Load a pitch trace and filters it. If no points are
    reliable, returns None.
    """
    from chirp.common import plg
    pest = plg.read(locator)
    ind = filt(pest)
    if not any(ind):
        return
    else:
        ind = postfilter.ind_endpoints(ind)
        return pest[estimator][ind[0]:ind[1] + 1]
        return