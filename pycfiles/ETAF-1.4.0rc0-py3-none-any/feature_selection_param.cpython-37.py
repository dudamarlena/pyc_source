# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/feature_selection_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 9689 bytes
import copy
from federatedml.param.base_param import BaseParam
from federatedml.util import consts

class UniqueValueParam(BaseParam):
    __doc__ = '\n    Use the difference between max-value and min-value to judge.\n\n    Parameters\n    ----------\n    eps: float, default: 1e-5\n        The column(s) will be filtered if its difference is smaller than eps.\n    '

    def __init__(self, eps=1e-05):
        self.eps = eps

    def check(self):
        descr = "Unique value param's"
        self.check_positive_number(self.eps, descr)
        return True


class IVValueSelectionParam(BaseParam):
    __doc__ = '\n    Use information values to select features.\n\n    Parameters\n    ----------\n    value_threshold: float, default: 1.0\n        Used if iv_value_thres method is used in feature selection.\n\n    host_thresholds: List of float or None, default: None\n        Set threshold for different host. If None, use same threshold as guest. If provided, the order should map with\n        the host id setting.\n\n    '

    def __init__(self, value_threshold=0.0, host_thresholds=None, local_only=False):
        super().__init__()
        self.value_threshold = value_threshold
        self.host_thresholds = host_thresholds
        self.local_only = local_only

    def check(self):
        if not isinstance(self.value_threshold, (float, int)):
            raise ValueError("IV selection param's value_threshold should be float or int")
        else:
            if self.host_thresholds is not None:
                if not isinstance(self.host_thresholds, list):
                    raise ValueError("IV selection param's host_threshold should be list or None")
            assert isinstance(self.local_only, bool), "IV selection param's local_only should be bool"
        return True


class IVPercentileSelectionParam(BaseParam):
    __doc__ = '\n    Use information values to select features.\n\n    Parameters\n    ----------\n    percentile_threshold: float, 0 <= percentile_threshold <= 1.0, default: 1.0\n        Percentile threshold for iv_percentile method\n\n\n    '

    def __init__(self, percentile_threshold=1.0, local_only=False):
        super().__init__()
        self.percentile_threshold = percentile_threshold
        self.local_only = local_only

    def check(self):
        descr = "IV selection param's"
        self.check_decimal_float(self.percentile_threshold, descr)
        self.check_boolean(self.local_only, descr)
        return True


class VarianceOfCoeSelectionParam(BaseParam):
    __doc__ = '\n    Use coefficient of variation to select features. When judging, the absolute value will be used.\n\n    Parameters\n    ----------\n    value_threshold: float, default: 1.0\n        Used if coefficient_of_variation_value_thres method is used in feature selection. Filter those\n        columns who has smaller coefficient of variance than the threshold.\n\n    '

    def __init__(self, value_threshold=1.0):
        self.value_threshold = value_threshold

    def check(self):
        descr = "Coff of Variances param's"
        self.check_positive_number(self.value_threshold, descr)
        return True


class OutlierColsSelectionParam(BaseParam):
    __doc__ = '\n    Given percentile and threshold. Judge if this quantile point is larger than threshold. Filter those larger ones.\n\n    Parameters\n    ----------\n    percentile: float, [0., 1.] default: 1.0\n        The percentile points to compare.\n\n    upper_threshold: float, default: 1.0\n        Percentile threshold for coefficient_of_variation_percentile method\n\n    '

    def __init__(self, percentile=1.0, upper_threshold=1.0):
        self.percentile = percentile
        self.upper_threshold = upper_threshold

    def check(self):
        descr = "Outlier Filter param's"
        self.check_decimal_float(self.percentile, descr)
        self.check_defined_type(self.upper_threshold, descr, ['float', 'int'])
        return True


class ManuallyFilterParam(BaseParam):
    __doc__ = "\n    Specified columns that need to be filtered. If exist, it will be filtered directly, otherwise, ignore it.\n\n    Parameters\n    ----------\n    filter_out_indexes: list or int, default: []\n        Specify columns' indexes to be filtered out\n\n    filter_out_names : list of string, default: []\n        Specify columns' names to be filtered out\n\n    "

    def __init__(self, filter_out_indexes=None, filter_out_names=None):
        super().__init__()
        if filter_out_indexes is None:
            filter_out_indexes = []
        if filter_out_names is None:
            filter_out_names = []
        self.filter_out_indexes = filter_out_indexes
        self.filter_out_names = filter_out_names

    def check(self):
        descr = "Manually Filter param's"
        self.check_defined_type(self.filter_out_indexes, descr, ['list', 'NoneType'])
        self.check_defined_type(self.filter_out_names, descr, ['list', 'NoneType'])
        return True


class FeatureSelectionParam(BaseParam):
    __doc__ = '\n    Define the feature selection parameters.\n\n    Parameters\n    ----------\n    select_col_indexes: list or int, default: -1\n        Specify which columns need to calculated. -1 represent for all columns.\n\n    select_names : list of string, default: []\n        Specify which columns need to calculated. Each element in the list represent for a column name in header.\n\n    filter_methods: list, ["manually", "unique_value", "iv_value_thres", "iv_percentile",\n                "coefficient_of_variation_value_thres", "outlier_cols"],\n                 default: ["unique_value"]\n\n        Specify the filter methods used in feature selection. The orders of filter used is depended on this list.\n        Please be notified that, if a percentile method is used after some certain filter method,\n        the percentile represent for the ratio of rest features.\n\n        e.g. If you have 10 features at the beginning. After first filter method, you have 8 rest. Then, you want\n        top 80% highest iv feature. Here, we will choose floor(0.8 * 8) = 6 features instead of 8.\n\n    unique_param: filter the columns if all values in this feature is the same\n\n    iv_value_param: Use information value to filter columns. If this method is set, a float threshold need to be provided.\n        Filter those columns whose iv is smaller than threshold.\n\n    iv_percentile_param: Use information value to filter columns. If this method is set, a float ratio threshold\n        need to be provided. Pick floor(ratio * feature_num) features with higher iv. If multiple features around\n        the threshold are same, all those columns will be keep.\n\n    variance_coe_param: Use coefficient of variation to judge whether filtered or not.\n\n    outlier_param: Filter columns whose certain percentile value is larger than a threshold.\n\n    need_run: bool, default True\n        Indicate if this module needed to be run\n\n    '

    def __init__(self, select_col_indexes=-1, select_names=None, filter_methods=None, unique_param=UniqueValueParam(), iv_value_param=IVValueSelectionParam(), iv_percentile_param=IVPercentileSelectionParam(), variance_coe_param=VarianceOfCoeSelectionParam(), outlier_param=OutlierColsSelectionParam(), manually_param=ManuallyFilterParam(), need_run=True):
        super(FeatureSelectionParam, self).__init__()
        self.select_col_indexes = select_col_indexes
        if select_names is None:
            self.select_names = []
        else:
            self.select_names = select_names
        if filter_methods is None:
            self.filter_methods = [
             consts.UNIQUE_VALUE]
        else:
            self.filter_methods = filter_methods
        self.unique_param = copy.deepcopy(unique_param)
        self.iv_value_param = copy.deepcopy(iv_value_param)
        self.iv_percentile_param = copy.deepcopy(iv_percentile_param)
        self.variance_coe_param = copy.deepcopy(variance_coe_param)
        self.outlier_param = copy.deepcopy(outlier_param)
        self.manually_param = copy.deepcopy(manually_param)
        self.need_run = need_run

    def check(self):
        descr = "hetero feature selection param's"
        self.check_defined_type(self.filter_methods, descr, ['list'])
        for idx, method in enumerate(self.filter_methods):
            method = method.lower()
            self.check_valid_value(method, descr, ['unique_value', 'iv_value_thres', 'iv_percentile',
             'coefficient_of_variation_value_thres',
             'outlier_cols', 'manually'])
            self.filter_methods[idx] = method

        self.check_defined_type(self.select_col_indexes, descr, ['list', 'int'])
        self.unique_param.check()
        self.iv_value_param.check()
        self.iv_percentile_param.check()
        self.variance_coe_param.check()
        self.outlier_param.check()
        self.manually_param.check()