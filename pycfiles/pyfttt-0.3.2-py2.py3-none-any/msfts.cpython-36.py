# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/seasonal/msfts.py
# Compiled at: 2018-04-10 23:59:35
# Size of source mod 2**32: 1921 bytes
import numpy as np
from pyFTS.common import FLR
from pyFTS.models.seasonal import sfts

class MultiSeasonalFTS(sfts.SeasonalFTS):
    """MultiSeasonalFTS"""

    def __init__(self, name, indexer, **kwargs):
        super(MultiSeasonalFTS, self).__init__('MSFTS')
        self.name = 'Multi Seasonal FTS'
        self.shortname = 'MSFTS ' + name
        self.detail = ''
        self.seasonality = 1
        self.has_seasonality = True
        self.has_point_forecasting = True
        self.is_high_order = False
        self.is_multivariate = True
        self.indexer = indexer
        self.flrgs = {}

    def generate_flrg(self, flrs):
        for flr in flrs:
            if str(flr.index) not in self.flrgs:
                self.flrgs[str(flr.index)] = sfts.SeasonalFLRG(flr.index)
            self.flrgs[str(flr.index)].append_rhs(flr.RHS)

    def train(self, data, **kwargs):
        if kwargs.get('sets', None) is not None:
            self.sets = kwargs.get('sets', None)
        if kwargs.get('parameters', None) is not None:
            self.seasonality = kwargs.get('parameters', None)
        flrs = FLR.generate_indexed_flrs(self.sets, self.indexer, data)
        self.generate_flrg(flrs)

    def forecast(self, data, **kwargs):
        ret = []
        index = self.indexer.get_season_of_data(data)
        ndata = self.indexer.get_data(data)
        for k in np.arange(0, len(index)):
            flrg = self.flrgs[str(index[k])]
            mp = self.getMidpoints(flrg)
            ret.append(sum(mp) / len(mp))

        return ret

    def forecast_ahead(self, data, steps, **kwargs):
        ret = []
        for i in steps:
            flrg = self.flrgs[str(i)]
            mp = self.getMidpoints(flrg)
            ret.append(sum(mp) / len(mp))

        return ret