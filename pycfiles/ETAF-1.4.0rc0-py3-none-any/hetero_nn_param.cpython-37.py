# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/hetero_nn_param.py
# Compiled at: 2020-05-05 22:26:58
# Size of source mod 2**32: 9750 bytes
import copy, collections
from types import SimpleNamespace
from federatedml.param.base_param import BaseParam
from federatedml.param.cross_validation_param import CrossValidationParam
from federatedml.param.encrypt_param import EncryptParam
from federatedml.param.encrypted_mode_calculation_param import EncryptedModeCalculatorParam
from federatedml.param.predict_param import PredictParam
from federatedml.util import consts

class HeteroNNParam(BaseParam):
    __doc__ = '\n    Parameters used for Homo Neural Network.\n\n    Args:\n        task_type: str, task type of hetero nn model, one of \'classification\', \'regression\'.\n        config_type: str, accept "keras" only.\n        bottom_nn_define: a dict represents the structure of bottom neural network.\n        interactive_layer_define: a dict represents the structure of interactive layer.\n        interactive_layer_lr: float, the learning rate of interactive layer.\n        top_nn_define: a dict represents the structure of top neural network.\n        optimizer: optimizer method, accept following types:\n            1. a string, one of "Adadelta", "Adagrad", "Adam", "Adamax", "Nadam", "RMSprop", "SGD"\n            2. a dict, with a required key-value pair keyed by "optimizer",\n                with optional key-value pairs such as learning rate.\n            defaults to "SGD"\n        loss:  str, a string to define loss function used\n        early_stopping_rounds: int, default: None\n        Will stop training if one metric doesn’t improve in last early_stopping_round rounds\n        metrics: list, default: None\n            Indicate when executing evaluation during train process, which metrics will be used. If not set,\n            default metrics for specific task type will be used. As for binary classification, default metrics are\n            [\'auc\', \'ks\'], for regression tasks, default metrics are [\'root_mean_squared_error\', \'mean_absolute_error\'],\n            [ACCURACY, PRECISION, RECALL] for multi-classification task\n        use_first_metric_only: bool, default: False\n            Indicate whether to use the first metric in `metrics` as the only criterion for early stopping judgement.\n        epochs: int, the maximum iteration for aggregation in training.\n        batch_size : int, batch size when updating model.\n            -1 means use all data in a batch. i.e. Not to use mini-batch strategy.\n            defaults to -1.\n        early_stop : str, accept \'diff\' only in this version, default: \'diff\'\n            Method used to judge converge or not.\n                a)\tdiff： Use difference of loss between two iterations to judge whether converge.\n        validation_freqs: None or positive integer or container object in python. Do validation in training process or Not.\n                  if equals None, will not do validation in train process;\n                  if equals positive integer, will validate data every validation_freqs epochs passes;\n                  if container object in python, will validate data if epochs belong to this container.\n                    e.g. validation_freqs = [10, 15], will validate data when epoch equals to 10 and 15.\n                  Default: None\n                  The default value is None, 1 is suggested. You can set it to a number larger than 1 in order to\n                  speed up training by skipping validation rounds. When it is larger than 1, a number which is\n                  divisible by "epochs" is recommended, otherwise, you will miss the validation scores\n                  of last training epoch.\n    '

    def __init__(self, task_type='classification', config_type='keras', bottom_nn_define=None, top_nn_define=None, interactive_layer_define=None, interactive_layer_lr=0.9, optimizer='SGD', loss=None, epochs=100, batch_size=-1, early_stop='diff', tol=1e-05, encrypt_param=EncryptParam(), encrypted_mode_calculator_param=EncryptedModeCalculatorParam(mode='confusion_opt'), predict_param=PredictParam(), cv_param=CrossValidationParam(), validation_freqs=None, early_stopping_rounds=None, metrics=None, use_first_metric_only=True):
        super(HeteroNNParam, self).__init__()
        self.task_type = task_type
        self.config_type = config_type
        self.bottom_nn_define = bottom_nn_define
        self.interactive_layer_define = interactive_layer_define
        self.interactive_layer_lr = interactive_layer_lr
        self.top_nn_define = top_nn_define
        self.batch_size = batch_size
        self.epochs = epochs
        self.early_stop = early_stop
        self.tol = tol
        self.optimizer = optimizer
        self.loss = loss
        self.validation_freqs = validation_freqs
        self.early_stopping_rounds = early_stopping_rounds
        self.metrics = metrics or []
        self.use_first_metric_only = use_first_metric_only
        self.encrypt_param = copy.deepcopy(encrypt_param)
        self.encrypted_model_calculator_param = encrypted_mode_calculator_param
        self.predict_param = copy.deepcopy(predict_param)
        self.cv_param = copy.deepcopy(cv_param)

    def check(self):
        self.optimizer = self._parse_optimizer(self.optimizer)
        supported_config_type = ['keras']
        if self.task_type not in ('classification', 'regression'):
            raise ValueError('config_type should be classification or regression')
        if self.config_type not in supported_config_type:
            raise ValueError(f"config_type should be one of {supported_config_type}")
        if not isinstance(self.tol, (int, float)):
            raise ValueError('tol should be numeric')
        if not isinstance(self.epochs, int) or self.epochs <= 0:
            raise ValueError('epochs should be a positive integer')
        if self.bottom_nn_define:
            if not isinstance(self.bottom_nn_define, dict):
                raise ValueError('bottom_nn_define should be a dict defining the structure of neural network')
        if self.top_nn_define:
            if not isinstance(self.top_nn_define, dict):
                raise ValueError('top_nn_define should be a dict defining the structure of neural network')
        if self.interactive_layer_define is not None:
            if not isinstance(self.interactive_layer_define, dict):
                raise ValueError('the interactive_layer_define should be a dict defining the structure of interactive layer')
        if self.batch_size != -1:
            if not isinstance(self.batch_size, int) or self.batch_size < consts.MIN_BATCH_SIZE:
                raise ValueError(' {} not supported, should be larger than 10 or -1 represent for all data'.format(self.batch_size))
        if self.early_stop != 'diff':
            raise ValueError('early stop should be diff in this version')
        if self.validation_freqs is None:
            pass
        else:
            if isinstance(self.validation_freqs, int):
                if self.validation_freqs < 1:
                    raise ValueError("validation_freqs should be larger than 0 when it's integer")
                else:
                    if not isinstance(self.validation_freqs, collections.Container):
                        raise ValueError('validation_freqs should be None or positive integer or container')
                if self.early_stopping_rounds:
                    if not isinstance(self.early_stopping_rounds, int):
                        raise ValueError('early stopping rounds should be None or int larger than 0')
            else:
                if self.early_stopping_rounds:
                    if isinstance(self.early_stopping_rounds, int):
                        if self.early_stopping_rounds < 1:
                            raise ValueError("early stopping should be larger than 0 when it's integer")
                        if not self.validation_freqs:
                            raise ValueError('If early stopping rounds is setting, validation_freqs should not be null')
                assert isinstance(self.metrics, list), 'metrics should be a list'
            self.encrypt_param.check()
            self.encrypted_model_calculator_param.check()
            self.predict_param.check()

    @staticmethod
    def _parse_optimizer(opt):
        """
        Examples:

            1. "optimize": "SGD"
            2. "optimize": {
                "optimizer": "SGD",
                "learning_rate": 0.05
            }
        """
        kwargs = {}
        if isinstance(opt, str):
            return SimpleNamespace(optimizer=opt, kwargs=kwargs)
        if isinstance(opt, dict):
            optimizer = opt.get('optimizer', kwargs)
            if not optimizer:
                raise ValueError(f"optimizer config: {opt} invalid")
            kwargs = {k:v for k, v in opt.items() if k != 'optimizer' if k != 'optimizer'}
            return SimpleNamespace(optimizer=optimizer, kwargs=kwargs)
        raise ValueError(f"invalid type for optimize: {type(opt)}")