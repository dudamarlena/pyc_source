# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/evaluation_param.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 4933 bytes
from arch.api.utils import log_utils
from federatedml.util import consts
from federatedml.param.base_param import BaseParam
LOGGER = log_utils.getLogger()

class EvaluateParam(BaseParam):
    __doc__ = "\n    Define the evaluation method of binary/multiple classification and regression\n\n    Parameters\n    ----------\n    eval_type: string, support 'binary' for HomoLR, HeteroLR and Secureboosting. support 'regression' for Secureboosting. 'multi' is not support these version\n\n    pos_label: specify positive label type, can be int, float and str, this depend on the data's label, this parameter effective only for 'binary'\n\n    need_run: bool, default True\n        Indicate if this module needed to be run\n    "

    def __init__(self, eval_type='binary', pos_label=1, need_run=True, metrics=None):
        super().__init__()
        self.eval_type = eval_type
        self.pos_label = pos_label
        self.need_run = need_run
        self.metrics = metrics
        self.default_metrics = {consts.BINARY: consts.ALL_BINARY_METRICS, 
         consts.MULTY: consts.ALL_MULTI_METRICS, 
         consts.REGRESSION: consts.ALL_REGRESSION_METRICS}
        self.allowed_metrics = {consts.BINARY: consts.ALL_BINARY_METRICS, 
         consts.MULTY: consts.ALL_MULTI_METRICS, 
         consts.REGRESSION: consts.ALL_REGRESSION_METRICS}

    def _use_single_value_default_metrics(self):
        self.default_metrics = {consts.BINARY: consts.DEFAULT_BINARY_METRIC, 
         consts.MULTY: consts.DEFAULT_MULTI_METRIC, 
         consts.REGRESSION: consts.DEFAULT_REGRESSION_METRIC}

    def _check_valid_metric(self, metrics_list):
        metric_list = consts.ALL_METRIC_NAME
        alias_name = consts.ALIAS
        full_name_list = []
        metrics_list = [str.lower(i) for i in metrics_list]
        for metric in metrics_list:
            if metric in metric_list:
                if metric not in full_name_list:
                    full_name_list.append(metric)
                    continue
                valid_flag = False
                for alias, full_name in alias_name.items():
                    if metric in alias:
                        if full_name not in full_name_list:
                            full_name_list.append(full_name)
                        valid_flag = True
                        break

                assert valid_flag, 'metric {} is not supported'.format(metric)

        allowed_metrics = self.allowed_metrics[self.eval_type]
        for m in full_name_list:
            if m not in allowed_metrics:
                raise ValueError('metric {} is not used for {} task'.format(m, self.eval_type))

        if consts.RECALL in full_name_list:
            if consts.PRECISION not in full_name_list:
                full_name_list.append(consts.PRECISION)
        if consts.RECALL not in full_name_list:
            if consts.PRECISION in full_name_list:
                full_name_list.append(consts.RECALL)
        return full_name_list

    def check(self):
        descr = "evaluate param's "
        self.eval_type = self.check_and_change_lower(self.eval_type, [
         consts.BINARY, consts.MULTY, consts.REGRESSION], descr)
        if type(self.pos_label).__name__ not in ('str', 'float', 'int'):
            raise ValueError("evaluate param's pos_label {} not supported, should be str or float or int type".format(self.pos_label))
        if type(self.need_run).__name__ != 'bool':
            raise ValueError("evaluate param's need_run {} not supported, should be bool".format(self.need_run))
        if self.metrics is None or len(self.metrics) == 0:
            self.metrics = self.default_metrics[self.eval_type]
            LOGGER.warning('use default metric {} for eval type {}'.format(self.metrics, self.eval_type))
        self.metrics = self._check_valid_metric(self.metrics)
        LOGGER.info('Finish evaluation parameter check!')
        return True

    def check_single_value_default_metric(self):
        self._use_single_value_default_metrics()
        self.check()