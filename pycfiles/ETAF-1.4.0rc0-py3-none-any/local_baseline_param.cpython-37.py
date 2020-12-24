# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/local_baseline_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1909 bytes
from federatedml.param.base_param import BaseParam

class LocalBaselineParam(BaseParam):
    __doc__ = '\n    Define the local baseline model param\n\n    Parameters\n    ----------\n    model_name: str, sklearn model used to train on baseline model\n\n    model_opts: dict or none, default None\n        Param to be used as input into baseline model\n\n    need_run: bool, default True\n        Indicate if this module needed to be run\n    '

    def __init__(self, model_name='LogisticRegression', model_opts=None, need_run=True):
        super(LocalBaselineParam, self).__init__()
        self.model_name = model_name
        self.model_opts = model_opts
        self.need_run = need_run

    def check(self):
        descr = 'local baseline param'
        self.mode = self.check_and_change_lower(self.model_name, [
         'logisticregression'], descr)
        self.check_boolean(self.need_run, descr)
        if self.model_opts is not None:
            if not isinstance(self.model_opts, dict):
                raise ValueError(descr + ' model_opts must be None or dict.')
        if self.model_opts is None:
            self.model_opts = {}
        return True