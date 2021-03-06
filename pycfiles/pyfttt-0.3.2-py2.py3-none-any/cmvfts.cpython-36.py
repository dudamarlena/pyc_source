# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/multivariate/cmvfts.py
# Compiled at: 2019-04-16 10:31:48
# Size of source mod 2**32: 4495 bytes
import numpy as np, pandas as pd
from pyFTS.common import FuzzySet, FLR, fts, flrg
from pyFTS.models import hofts
from pyFTS.models.multivariate import mvfts, grid, common
from types import LambdaType

class ClusteredMVFTS(mvfts.MVFTS):
    """ClusteredMVFTS"""

    def __init__(self, **kwargs):
        (super(ClusteredMVFTS, self).__init__)(**kwargs)
        self.fts_method = kwargs.get('fts_method', hofts.WeightedHighOrderFTS)
        self.fts_params = kwargs.get('fts_params', {})
        self.model = None
        self.knn = kwargs.get('knn', 2)
        self.is_high_order = True
        self.is_clustered = True
        self.order = kwargs.get('order', 2)
        self.lags = kwargs.get('lags', None)
        self.alpha_cut = kwargs.get('alpha_cut', 0.0)
        self.shortname = 'ClusteredMVFTS'
        self.name = 'Clustered Multivariate FTS'
        self.pre_fuzzyfy = kwargs.get('pre_fuzzyfy', True)

    def fuzzyfy(self, data):
        ndata = []
        for index, row in data.iterrows():
            data_point = self.format_data(row)
            ndata.append(self.partitioner.fuzzyfy(data_point, mode='sets'))

        return ndata

    def train(self, data, **kwargs):
        self.fts_params['order'] = self.order
        self.model = (self.fts_method)(partitioner=self.partitioner, **self.fts_params)
        ndata = self.check_data(data)
        self.model.train(ndata, fuzzyfied=(self.pre_fuzzyfy))
        self.partitioner.prune()

    def check_data(self, data):
        if self.pre_fuzzyfy:
            ndata = self.fuzzyfy(data)
        else:
            ndata = [self.format_data(k) for k in data.to_dict('records')]
        return ndata

    def forecast(self, ndata, **kwargs):
        ndata = self.check_data(ndata)
        return (self.model.forecast)(ndata, fuzzyfied=self.pre_fuzzyfy, **kwargs)

    def forecast_multivariate(self, data, **kwargs):
        ndata = self.check_data(data)
        generators = kwargs.get('generators', {})
        already_processed_cols = []
        ret = {}
        ret[self.target_variable.data_label] = (self.model.forecast)(ndata, fuzzyfied=self.pre_fuzzyfy, **kwargs)
        for var in self.explanatory_variables:
            if var.data_label not in already_processed_cols:
                if var.data_label in generators:
                    if isinstance(generators[var.data_label], LambdaType):
                        fx = generators[var.data_label]
                        if len(data[var.data_label].values) > self.order:
                            ret[var.data_label] = [fx(k) for k in data[var.data_label].values[self.order:]]
                        else:
                            ret[var.data_label] = [
                             fx(data[var.data_label].values[(-1)])]
                    else:
                        if isinstance(generators[var.data_label], fts.FTS):
                            model = generators[var.data_label]
                            ret[var.data_label] = model.is_multivariate or model.forecast(data[var.data_label].values)
                        else:
                            ret[var.data_label] = model.forecast(data)
                else:
                    if self.target_variable.name != var.name:
                        self.target_variable = var
                        self.partitioner.change_target_variable(var)
                        self.model.partitioner = self.partitioner
                        self.model.reset_calculated_values()
                        ret[var.data_label] = (self.model.forecast)(ndata, fuzzyfied=self.pre_fuzzyfy, **kwargs)
                    already_processed_cols.append(var.data_label)

        return pd.DataFrame(ret, columns=(ret.keys()))

    def forecast_ahead_multivariate(self, data, steps, **kwargs):
        ndata = self.apply_transformations(data)
        ret = ndata.iloc[:self.order]
        for k in np.arange(0, steps):
            sample = ret.iloc[k:self.order + k]
            tmp = (self.forecast_multivariate)(sample, **kwargs)
            ret = ret.append(tmp, ignore_index=True)

        return ret

    def __str__(self):
        """String representation of the model"""
        return str(self.model)

    def __len__(self):
        """
        The length (number of rules) of the model

        :return: number of rules
        """
        return len(self.model)