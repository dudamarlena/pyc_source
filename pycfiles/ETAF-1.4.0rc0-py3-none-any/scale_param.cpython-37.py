# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/scale_param.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 4827 bytes
from arch.api.utils import log_utils
from federatedml.param.base_param import BaseParam
from federatedml.util import consts
LOGGER = log_utils.getLogger()

class ScaleParam(BaseParam):
    __doc__ = '\n    Define the feature scale parameters.\n\n    Parameters\n    ----------\n        method : str, like scale in sklearn, now it support "min_max_scale" and "standard_scale", and will support other scale method soon.\n                 Default None, which will do nothing for scale\n\n        mode: str, the mode support "normal" and "cap". for mode is "normal", the feat_upper and feat_lower is the normal value like "10" or "3.1" and for "cap", feat_upper and\n              feature_lower will between 0 and 1, which means the percentile of the column. Default "normal"\n\n        feat_upper: int or float, the upper limit in the column. If the scaled value is larger than feat_upper, it will be set to feat_upper. Default None.\n        feat_lower: int or float, the lower limit in the column. If the scaled value is less than feat_lower, it will be set to feat_lower. Default None.\n\n        scale_col_indexes: list,the idx of column in scale_column_idx will be scaled, while the idx of column is not in, it will not be scaled.\n        scale_names : list of string, default: [].Specify which columns need to scaled. Each element in the list represent for a column name in header.\n        with_mean: bool, used for "standard_scale". Default False.\n        with_std: bool, used for "standard_scale". Default False.\n            The standard scale of column x is calculated as : z = (x - u) / s, where u is the mean of the column and s is the standard deviation of the column.\n            if with_mean is False, u will be 0, and if with_std is False, s will be 1.\n\n        need_run: bool, default True\n            Indicate if this module needed to be run\n\n    '

    def __init__(self, method=None, mode='normal', scale_col_indexes=-1, scale_names=None, feat_upper=None, feat_lower=None, with_mean=True, with_std=True, need_run=True):
        super().__init__()
        if scale_names is None:
            scale_names = []
        self.method = method
        self.mode = mode
        self.feat_upper = feat_upper
        self.feat_lower = feat_lower
        self.scale_col_indexes = scale_col_indexes
        self.scale_names = scale_names
        self.with_mean = with_mean
        self.with_std = with_std
        self.need_run = need_run

    def check(self):
        if self.method is not None:
            descr = "scale param's method"
            self.method = self.check_and_change_lower(self.method, [
             consts.MINMAXSCALE, consts.STANDARDSCALE], descr)
        else:
            descr = "scale param's mode"
            self.mode = self.check_and_change_lower(self.mode, [
             consts.NORMAL, consts.CAP], descr)
            if self.scale_col_indexes != -1:
                if not isinstance(self.scale_col_indexes, list):
                    raise ValueError('scale_col_indexes is should be -1 or a list')
            if not isinstance(self.scale_names, list):
                raise ValueError('scale_names is should be a list of string')
            else:
                for e in self.scale_names:
                    if not isinstance(e, str):
                        raise ValueError('scale_names is should be a list of string')

        self.check_boolean(self.with_mean, 'scale_param with_mean')
        self.check_boolean(self.with_std, 'scale_param with_std')
        self.check_boolean(self.need_run, 'scale_param need_run')
        LOGGER.debug('Finish scale parameter check!')
        return True