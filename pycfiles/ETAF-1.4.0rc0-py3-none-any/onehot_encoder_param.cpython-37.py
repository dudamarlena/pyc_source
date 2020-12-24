# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/onehot_encoder_param.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 1889 bytes
from arch.api.utils import log_utils
from federatedml.param.base_param import BaseParam
LOGGER = log_utils.getLogger()

class OneHotEncoderParam(BaseParam):
    __doc__ = '\n\n    Parameters\n    ----------\n\n    transform_col_indexes: list or int, default: -1\n        Specify which columns need to calculated. -1 represent for all columns.\n\n    transform_col_names : list of string, default: []\n        Specify which columns need to calculated. Each element in the list represent for a column name in header.\n\n\n    need_run: bool, default True\n        Indicate if this module needed to be run\n    '

    def __init__(self, transform_col_indexes=-1, transform_col_names=None, need_run=True):
        super(OneHotEncoderParam, self).__init__()
        if transform_col_names is None:
            transform_col_names = []
        self.transform_col_indexes = transform_col_indexes
        self.transform_col_names = transform_col_names
        self.need_run = need_run

    def check(self):
        descr = "One-hot encoder param's"
        self.check_defined_type(self.transform_col_indexes, descr, ['list', 'int', 'NoneType'])
        self.check_defined_type(self.transform_col_names, descr, ['list', 'NoneType'])
        return True