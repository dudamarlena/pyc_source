# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/datamining/bandwidth.py
# Compiled at: 2010-11-12 22:12:07
"""
Bandwidth estimation.
"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__rcsid__ = '$Id: bandwidth.py 26773 2010-11-13 03:12:07Z dang $'
import math, rpy2.robjects as robj
from netlogger.analysis.datamining import rpython
from netlogger.analysis.datamining.base import PlotFunction, PlotParam, Plot, PlotError
rbase = rpython.base

class Prediction:

    def __init__(self, n):
        self.n = n


class Fivenum(Prediction):
    """Encapsulate Tukey's 5 values.
    """
    NAMES = ('min', 'q1', 'med', 'q3', 'max')

    def __init__(self, n, values):
        Prediction.__init__(self, n)
        self._v = values

    def __str__(self):
        buf = ''
        for (i, name) in enumerate(self.NAMES):
            buf += '%s = %s\n' % (name, self._v[i])

        return buf


class RPredict:
    """Predict future values, using R.
    """

    def get_value(self, confidence=0.95, size_mix={}, **param):
        """Get prediction value.

        Kwargs:
           param (dict): Parameters for prediction.
           size_mix (dict): Key is size in bytes, value is percent
              of files with that expected size. Both are integers.
        Return:
           (Predict) Prediction with confidence interval
        """
        if self._data is None or self._data.nrow == 0:
            raise ValueError('No data available for prediction')
        bytes = size_mix.keys()
        bytes.sort()
        mfs = robj.IntVector(bytes)
        mfp = robj.IntVector([ size_mix[b] for b in bytes ])
        result = rpython.nlr.bw_predict_path(self._data, confidence=confidence, group_col='path', min_file_sizes=mfs, min_file_pct=mfp, **param)
        return Fivenum(result.rx2('n')[0], tuple(result.rx2('value')))


class GroupedPlot(PlotFunction):
    """Plot that can be grouped.
    """
    PLOT_SCATTER = 'scatter'
    PLOT_DENSITY = 'density'

    class Param(PlotParam):
        """Parameters for this specific type of plot.
        """

        def __init__(self, interval=60, title='', groups=[], type='scatter', **kw):
            self._ptype = type
            if not title:
                title = 'Bandwidth, smoothed over %d second windows' % interval
            PlotParam.__init__(self, title=title, **kw)
            self.interval = interval
            self.groups = robj.StrVector(groups)
            self._attrs.extend(['interval', 'groups'])

    def create(self):
        """Create a scatterplot, using the current data frame
        and parameters.

        Return: Plot instance
        """
        self.log.debug('%splot.create.start' % self.param._ptype)
        self.create_common(rpy=rpython)
        name = 'bw_plot_%s' % self.param._ptype
        result = rpython.nlr.doplot(name, self.data, **self.param.as_dict())
        result = Plot(path=result, device=self.param.device)
        self.log.debug('%splot.create.end' % self.param._ptype)
        return result


class IperfPlot(PlotFunction):
    """Plot for iperf data.
    """

    class Param(PlotParam):

        def __init__(self, title='', **kw):
            PlotParam.__init__(self, title=title, **kw)

    def create(self):
        self.log.debug('iperf-plot.create.start')
        self.create_common(rpy=rpython)
        name = 'iperf_plot'
        result = rpython.nlr.doplot(name, self.data, **self.param.as_dict())
        result = Plot(path=result, device=self.param.device)
        self.log.debug('iperf-plot.create.end')
        return result