# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/homo_nn_param.py
# Compiled at: 2020-04-30 07:16:32
# Size of source mod 2**32: 6524 bytes
import copy, typing
from types import SimpleNamespace
from federatedml.param.base_param import BaseParam
from federatedml.param.cross_validation_param import CrossValidationParam
from federatedml.param.predict_param import PredictParam
from federatedml.protobuf.generated import nn_model_meta_pb2
import json

class HomoNNParam(BaseParam):
    __doc__ = '\n    Parameters used for Homo Neural Network.\n\n    Parameters\n    ----------\n    '

    def __init__(self, secure_aggregate=True, aggregate_every_n_epoch=1, config_type='nn', nn_define=None, optimizer='SGD', loss=None, metrics=None, max_iter=100, batch_size=-1, early_stop='diff', predict_param=PredictParam(), cv_param=CrossValidationParam()):
        super(HomoNNParam, self).__init__()
        self.secure_aggregate = secure_aggregate
        self.aggregate_every_n_epoch = aggregate_every_n_epoch
        self.config_type = config_type
        self.nn_define = nn_define or []
        self.batch_size = batch_size
        self.max_iter = max_iter
        self.early_stop = early_stop
        self.metrics = metrics
        self.optimizer = optimizer
        self.loss = loss
        self.predict_param = copy.deepcopy(predict_param)
        self.cv_param = copy.deepcopy(cv_param)

    def check(self):
        supported_config_type = [
         'nn', 'keras', 'pytorch']
        if self.config_type not in supported_config_type:
            raise ValueError(f"config_type should be one of {supported_config_type}")
        self.early_stop = _parse_early_stop(self.early_stop)
        self.metrics = _parse_metrics(self.metrics)
        self.optimizer = _parse_optimizer(self.optimizer)

    def generate_pb(self):
        pb = nn_model_meta_pb2.HomoNNParam()
        pb.secure_aggregate = self.secure_aggregate
        pb.aggregate_every_n_epoch = self.aggregate_every_n_epoch
        pb.config_type = self.config_type
        if self.config_type == 'nn':
            for layer in self.nn_define:
                pb.nn_define.append(json.dumps(layer))

        else:
            if self.config_type == 'keras':
                pb.nn_define.append(json.dumps(self.nn_define))
            else:
                if self.config_type == 'pytorch':
                    for layer in self.nn_define:
                        pb.nn_define.append(json.dumps(layer))

        pb.batch_size = self.batch_size
        pb.max_iter = self.max_iter
        pb.early_stop.early_stop = self.early_stop.converge_func
        pb.early_stop.eps = self.early_stop.eps
        for metric in self.metrics:
            pb.metrics.append(metric)

        pb.optimizer.optimizer = self.optimizer.optimizer
        pb.optimizer.args = json.dumps(self.optimizer.kwargs)
        pb.loss = self.loss
        return pb

    def restore_from_pb(self, pb):
        self.secure_aggregate = pb.secure_aggregate
        self.aggregate_every_n_epoch = pb.aggregate_every_n_epoch
        self.config_type = pb.config_type
        if self.config_type == 'nn':
            for layer in pb.nn_define:
                self.nn_define.append(json.loads(layer))

        else:
            if self.config_type == 'keras':
                self.nn_define = pb.nn_define[0]
            else:
                if self.config_type == 'pytorch':
                    for layer in pb.nn_define:
                        self.nn_define.append(json.loads(layer))

                else:
                    raise ValueError(f"{self.config_type} is not supported")
        self.batch_size = pb.batch_size
        self.max_iter = pb.max_iter
        self.early_stop = _parse_early_stop(dict(early_stop=(pb.early_stop.early_stop), eps=(pb.early_stop.eps)))
        self.metrics = list(pb.metrics)
        self.optimizer = _parse_optimizer(dict(optimizer=pb.optimizer.optimizer, **json.loads(pb.optimizer.args)))
        self.loss = pb.loss
        return pb


def _parse_metrics(param):
    """
    Examples:

        1. "metrics": "Accuracy"
        2. "metrics": ["Accuracy"]
    """
    if not param:
        return []
    if isinstance(param, str):
        return [
         param]
    if isinstance(param, list):
        return param
    raise ValueError(f"invalid metrics type: {type(param)}")


def _parse_optimizer(param):
    """
    Examples:

        1. "optimize": "SGD"
        2. "optimize": {
                "optimizer": "SGD",
                "learning_rate": 0.05
            }
    """
    kwargs = {}
    if isinstance(param, str):
        return SimpleNamespace(optimizer=param, kwargs=kwargs)
    if isinstance(param, dict):
        optimizer = param.get('optimizer', kwargs)
        if not optimizer:
            raise ValueError(f"optimizer config: {param} invalid")
        kwargs = {k:v for k, v in param.items() if k != 'optimizer' if k != 'optimizer'}
        return SimpleNamespace(optimizer=optimizer, kwargs=kwargs)
    raise ValueError(f"invalid type for optimize: {type(param)}")


def _parse_early_stop(param):
    """
       Examples:

           1. "early_stop": "diff"
           2. "early_stop": {
                   "early_stop": "diff",
                   "eps": 0.0001
               }
    """
    default_eps = 0.0001
    if isinstance(param, str):
        return SimpleNamespace(converge_func=param, eps=default_eps)
    if isinstance(param, dict):
        early_stop = param.get('early_stop', None)
        eps = param.get('eps', default_eps)
        if not early_stop:
            raise ValueError(f"early_stop config: {param} invalid")
        return SimpleNamespace(converge_func=early_stop, eps=eps)
    raise ValueError(f"invalid type for early_stop: {type(param)}")