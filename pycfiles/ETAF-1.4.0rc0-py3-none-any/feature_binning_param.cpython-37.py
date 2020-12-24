# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/feature_binning_param.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 9670 bytes
import copy, math
from arch.api.utils import log_utils
from federatedml.param.base_param import BaseParam
from federatedml.util import consts
LOGGER = log_utils.getLogger()

class TransformParam(BaseParam):
    __doc__ = "\n    Define how to transfer the cols\n\n    Parameters\n    ----------\n    transform_cols : list of column index, default: -1\n        Specify which columns need to be transform. If column index is None, None of columns will be transformed.\n        If it is -1, it will use same columns as cols in binning module.\n\n    transform_names: list of string, default: []\n        Specify which columns need to calculated. Each element in the list represent for a column name in header.\n\n\n    transform_type: str, 'bin_num'or 'woe' or None default: 'bin_num'\n        Specify which value these columns going to replace.\n         1. bin_num: Transfer original feature value to bin index in which this value belongs to.\n         2. woe: This is valid for guest party only. It will replace original value to its woe value\n         3. None: nothing will be replaced.\n    "

    def __init__(self, transform_cols=-1, transform_names=None, transform_type='bin_num'):
        super(TransformParam, self).__init__()
        self.transform_cols = transform_cols
        self.transform_names = transform_names
        self.transform_type = transform_type

    def check(self):
        descr = "Transform Param's "
        if self.transform_cols is not None:
            if self.transform_cols != -1:
                self.check_defined_type(self.transform_cols, descr, ['list'])
        self.check_defined_type(self.transform_names, descr, ['list', 'NoneType'])
        if self.transform_names is not None:
            for name in self.transform_names:
                if not isinstance(name, str):
                    raise ValueError('Elements in transform_names should be string type')

        self.check_valid_value(self.transform_type, descr, ['bin_num', 'woe', None])


class OptimalBinningParam(BaseParam):
    __doc__ = '\n    Indicate optimal binning params\n\n    Parameters\n    ----------\n    metric_method: str, default: "iv"\n        The algorithm metric method. Support iv, gini, ks, chi-square\n\n\n    min_bin_pct: float, default: 0.05\n        The minimum percentage of each bucket\n\n    max_bin_pct: float, default: 1.0\n        The maximum percentage of each bucket\n\n    init_bin_nums: int, default 100\n        Number of bins when initialize\n\n    mixture: bool, default: True\n        Whether each bucket need event and non-event records\n\n    init_bucket_method: str default: quantile\n        Init bucket methods. Accept quantile and bucket.\n\n    '

    def __init__(self, metric_method='iv', min_bin_pct=0.05, max_bin_pct=1.0, init_bin_nums=1000, mixture=True, init_bucket_method='quantile'):
        super().__init__()
        self.init_bucket_method = init_bucket_method
        self.metric_method = metric_method
        self.max_bin = None
        self.mixture = mixture
        self.max_bin_pct = max_bin_pct
        self.min_bin_pct = min_bin_pct
        self.init_bin_nums = init_bin_nums
        self.adjustment_factor = None

    def check(self):
        descr = "hetero binning's optimal binning param's"
        self.check_string(self.metric_method, descr)
        self.metric_method = self.metric_method.lower()
        if self.metric_method in ('chi_square', 'chi-square'):
            self.metric_method = 'chi_square'
        self.check_valid_value(self.metric_method, descr, ['iv', 'gini', 'chi_square', 'ks'])
        self.check_positive_integer(self.init_bin_nums, descr)
        self.init_bucket_method = self.init_bucket_method.lower()
        self.check_valid_value(self.init_bucket_method, descr, ['quantile', 'bucket'])
        if self.max_bin_pct not in (1, 0):
            self.check_decimal_float(self.max_bin_pct, descr)
        if self.min_bin_pct not in (1, 0):
            self.check_decimal_float(self.min_bin_pct, descr)
        if self.min_bin_pct > self.max_bin_pct:
            raise ValueError("Optimal binning's min_bin_pct should less or equal than max_bin_pct")
        self.check_boolean(self.mixture, descr)
        self.check_positive_integer(self.init_bin_nums, descr)


class FeatureBinningParam(BaseParam):
    __doc__ = "\n    Define the feature binning method\n\n    Parameters\n    ----------\n    method : str, 'quantile' or 'bucket', default: 'quantile'\n        Binning method.\n\n    compress_thres: int, default: 10000\n        When the number of saved summaries exceed this threshold, it will call its compress function\n\n    head_size: int, default: 10000\n        The buffer size to store inserted observations. When head list reach this buffer size, the\n        QuantileSummaries object start to generate summary(or stats) and insert into its sampled list.\n\n    error: float, 0 <= error < 1 default: 0.001\n        The error of tolerance of binning. The final split point comes from original data, and the rank\n        of this value is close to the exact rank. More precisely,\n        floor((p - 2 * error) * N) <= rank(x) <= ceil((p + 2 * error) * N)\n        where p is the quantile in float, and N is total number of data.\n\n    bin_num: int, bin_num > 0, default: 10\n        The max bin number for binning\n\n    bin_indexes : list of int or int, default: -1\n        Specify which columns need to be binned. -1 represent for all columns. If you need to indicate specific\n        cols, provide a list of header index instead of -1.\n\n    bin_names : list of string, default: []\n        Specify which columns need to calculated. Each element in the list represent for a column name in header.\n\n    adjustment_factor : float, default: 0.5\n        the adjustment factor when calculating WOE. This is useful when there is no event or non-event in\n        a bin. Please note that this parameter will NOT take effect for setting in host.\n\n    category_indexes : list of int or int, default: []\n        Specify which columns are category features. -1 represent for all columns. List of int indicate a set of\n        such features. For category features, bin_obj will take its original values as split_points and treat them\n        as have been binned. If this is not what you expect, please do NOT put it into this parameters.\n\n        The number of categories should not exceed bin_num set above.\n\n    category_names : list of string, default: []\n        Use column names to specify category features. Each element in the list represent for a column name in header.\n\n    local_only : bool, default: False\n        Whether just provide binning method to guest party. If true, host party will do nothing.\n\n    transform_param: TransformParam\n        Define how to transfer the binned data.\n\n    need_run: bool, default True\n        Indicate if this module needed to be run\n\n    "

    def __init__(self, method=consts.QUANTILE, compress_thres=consts.DEFAULT_COMPRESS_THRESHOLD, head_size=consts.DEFAULT_HEAD_SIZE, error=consts.DEFAULT_RELATIVE_ERROR, bin_num=consts.G_BIN_NUM, bin_indexes=-1, bin_names=None, adjustment_factor=0.5, transform_param=TransformParam(), optimal_binning_param=OptimalBinningParam(), local_only=False, category_indexes=None, category_names=None, need_run=True):
        super(FeatureBinningParam, self).__init__()
        self.method = method
        self.compress_thres = compress_thres
        self.head_size = head_size
        self.error = error
        self.adjustment_factor = adjustment_factor
        self.bin_num = bin_num
        self.bin_indexes = bin_indexes
        self.bin_names = bin_names
        self.category_indexes = category_indexes
        self.category_names = category_names
        self.local_only = local_only
        self.transform_param = copy.deepcopy(transform_param)
        self.optimal_binning_param = copy.deepcopy(optimal_binning_param)
        self.need_run = need_run

    def check(self):
        descr = "hetero binning param's"
        self.check_string(self.method, descr)
        self.method = self.method.lower()
        self.check_valid_value(self.method, descr, [consts.QUANTILE, consts.BUCKET, consts.OPTIMAL])
        self.check_positive_integer(self.compress_thres, descr)
        self.check_positive_integer(self.head_size, descr)
        self.check_decimal_float(self.error, descr)
        self.check_positive_integer(self.bin_num, descr)
        if self.bin_indexes != -1:
            self.check_defined_type(self.bin_indexes, descr, ['list', 'RepeatedScalarContainer', 'NoneType'])
        self.check_defined_type(self.bin_names, descr, ['list', 'NoneType'])
        self.check_defined_type(self.category_indexes, descr, ['list', 'NoneType'])
        self.check_defined_type(self.category_names, descr, ['list', 'NoneType'])
        self.check_open_unit_interval(self.adjustment_factor, descr)
        self.transform_param.check()
        self.optimal_binning_param.check()