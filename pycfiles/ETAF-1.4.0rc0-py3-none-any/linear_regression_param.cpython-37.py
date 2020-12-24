# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/linear_regression_param.py
# Compiled at: 2020-05-05 22:26:58
# Size of source mod 2**32: 11124 bytes
import copy
from federatedml.param.base_param import BaseParam
from federatedml.param.encrypt_param import EncryptParam
from federatedml.param.encrypted_mode_calculation_param import EncryptedModeCalculatorParam
from federatedml.param.cross_validation_param import CrossValidationParam
from federatedml.param.init_model_param import InitParam
from federatedml.param.predict_param import PredictParam
from federatedml.param.sqn_param import StochasticQuasiNewtonParam
from federatedml.param.stepwise_param import StepwiseParam
from federatedml.util import consts

class LinearParam(BaseParam):
    __doc__ = '\n    Parameters used for Linear Regression.\n\n    Parameters\n    ----------\n    penalty : str, \'L1\' or \'L2\'. default: \'L2\'\n        Penalty method used in LinR. Please note that, when using encrypted version in HeteroLinR,\n        \'L1\' is not supported.\n\n    tol : float, default: 1e-5\n        The tolerance of convergence\n\n    alpha : float, default: 1.0\n        Regularization strength coefficient.\n\n    optimizer : str, \'sgd\', \'rmsprop\', \'adam\', \'sqn\', or \'adagrad\', default: \'sgd\'\n        Optimize method\n\n    batch_size : int, default: -1\n        Batch size when updating model. -1 means use all data in a batch. i.e. Not to use mini-batch strategy.\n\n    learning_rate : float, default: 0.01\n        Learning rate\n\n    max_iter : int, default: 100\n        The maximum iteration for training.\n\n    init_param: InitParam object, default: default InitParam object\n        Init param method object.\n\n    early_stop : str, \'diff\' or \'abs\' or \'weight_dff\', default: \'diff\'\n        Method used to judge convergence.\n            a)\tdiff： Use difference of loss between two iterations to judge whether converge.\n            b)\tabs: Use the absolute value of loss to judge whether converge. i.e. if loss < tol, it is converged.\n            c)  weight_diff: Use difference between weights of two consecutive iterations\n\n    predict_param: PredictParam object, default: default PredictParam object\n\n    encrypt_param: EncryptParam object, default: default EncryptParam object\n\n    encrypted_mode_calculator_param: EncryptedModeCalculatorParam object, default: default EncryptedModeCalculatorParam object\n\n    cv_param: CrossValidationParam object, default: default CrossValidationParam object\n\n    decay: int or float, default: 1\n        Decay rate for learning rate. learning rate will follow the following decay schedule.\n        lr = lr0/(1+decay*t) if decay_sqrt is False. If decay_sqrt is True, lr = lr0 / sqrt(1+decay*t)\n        where t is the iter number.\n\n    decay_sqrt: Bool, default: True\n        lr = lr0/(1+decay*t) if decay_sqrt is False, otherwise, lr = lr0 / sqrt(1+decay*t)\n\n    validation_freqs: int, list, tuple, set, or None\n        validation frequency during training, required when using early stopping.\n        The default value is None, 1 is suggested. You can set it to a number larger than 1 in order to speed up training by skipping validation rounds.\n        When it is larger than 1, a number which is divisible by "max_iter" is recommended, otherwise, you will miss the validation scores of the last training iteration.\n\n    early_stopping_rounds: int, default: None\n        If positive number specified, at every specified training rounds, program checks for early stopping criteria.\n        Validation_freqs must also be set when using early stopping.\n\n    metrics: list, default: []\n        Specify which metrics to be used when performing evaluation during training process. If metrics have not improved at early_stopping rounds, trianing stops before convergence.\n        If set as empty, default metrics will be used. For regression tasks, default metrics are [\'root_mean_squared_error\', \'mean_absolute_error\']\n\n    use_first_metric_only: bool, default: False\n        Indicate whether to use the first metric in `metrics` as the only criterion for early stopping judgement.\n\n    '

    def __init__(self, penalty='L2', tol=1e-05, alpha=1.0, optimizer='sgd', batch_size=-1, learning_rate=0.01, init_param=InitParam(), max_iter=100, early_stop='diff', predict_param=PredictParam(), encrypt_param=EncryptParam(), sqn_param=StochasticQuasiNewtonParam(), encrypted_mode_calculator_param=EncryptedModeCalculatorParam(), cv_param=CrossValidationParam(), decay=1, decay_sqrt=True, validation_freqs=None, early_stopping_rounds=None, stepwise_param=StepwiseParam(), metrics=[], use_first_metric_only=False):
        super(LinearParam, self).__init__()
        self.penalty = penalty
        self.tol = tol
        self.alpha = alpha
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.init_param = copy.deepcopy(init_param)
        self.max_iter = max_iter
        self.early_stop = early_stop
        self.encrypt_param = encrypt_param
        self.encrypted_mode_calculator_param = copy.deepcopy(encrypted_mode_calculator_param)
        self.cv_param = copy.deepcopy(cv_param)
        self.predict_param = copy.deepcopy(predict_param)
        self.decay = decay
        self.decay_sqrt = decay_sqrt
        self.validation_freqs = validation_freqs
        self.sqn_param = copy.deepcopy(sqn_param)
        self.early_stopping_rounds = early_stopping_rounds
        self.stepwise_param = copy.deepcopy(stepwise_param)
        self.metrics = metrics
        self.use_first_metric_only = use_first_metric_only

    def check(self):
        descr = "linear_regression_param's "
        if self.penalty is None:
            self.penalty = 'NONE'
        else:
            if type(self.penalty).__name__ != 'str':
                raise ValueError(descr + 'penalty {} not supported, should be str type'.format(self.penalty))
        self.penalty = self.penalty.upper()
        if self.penalty not in ('L1', 'L2', 'NONE'):
            raise ValueError("penalty {} not supported, penalty should be 'L1', 'L2' or 'none'".format(self.penalty))
        if type(self.tol).__name__ not in ('int', 'float'):
            raise ValueError(descr + 'tol {} not supported, should be float type'.format(self.tol))
        if type(self.alpha).__name__ not in ('int', 'float'):
            raise ValueError(descr + 'alpha {} not supported, should be float type'.format(self.alpha))
        if type(self.optimizer).__name__ != 'str':
            raise ValueError(descr + 'optimizer {} not supported, should be str type'.format(self.optimizer))
        else:
            self.optimizer = self.optimizer.lower()
            if self.optimizer not in ('sgd', 'rmsprop', 'adam', 'adagrad', 'sqn'):
                raise ValueError(descr + "optimizer not supported, optimizer should be 'sgd', 'rmsprop', 'adam', 'sqn' or 'adagrad'")
            else:
                if type(self.batch_size).__name__ not in ('int', 'long'):
                    raise ValueError(descr + 'batch_size {} not supported, should be int type'.format(self.batch_size))
                if self.batch_size != -1:
                    if type(self.batch_size).__name__ not in ('int', 'long') or self.batch_size < consts.MIN_BATCH_SIZE:
                        raise ValueError(descr + ' {} not supported, should be larger than {} or -1 represent for all data'.format(self.batch_size, consts.MIN_BATCH_SIZE))
                    if type(self.learning_rate).__name__ not in ('int', 'float'):
                        raise ValueError(descr + 'learning_rate {} not supported, should be float type'.format(self.learning_rate))
                    self.init_param.check()
                    if type(self.max_iter).__name__ != 'int':
                        raise ValueError(descr + 'max_iter {} not supported, should be int type'.format(self.max_iter))
                elif self.max_iter <= 0:
                    raise ValueError(descr + 'max_iter must be greater or equal to 1')
        if type(self.early_stop).__name__ != 'str':
            raise ValueError(descr + 'early_stop {} not supported, should be str type'.format(self.early_stop))
        else:
            self.early_stop = self.early_stop.lower()
            if self.early_stop not in ('diff', 'abs', 'weight_diff'):
                raise ValueError(descr + "early_stop not supported, early_stop should be 'weight_diff', 'diff' or 'abs'")
            self.encrypt_param.check()
            if self.encrypt_param.method != consts.PAILLIER:
                raise ValueError(descr + "encrypt method supports 'Paillier' only")
            self.encrypted_mode_calculator_param.check()
            if type(self.decay).__name__ not in ('int', 'float'):
                raise ValueError(descr + "decay {} not supported, should be 'int' or 'float'".format(self.decay))
            if type(self.decay_sqrt).__name__ not in ('bool', ):
                raise ValueError(descr + "decay_sqrt {} not supported, should be 'bool'".format(self.decay))
            if self.validation_freqs is not None:
                if type(self.validation_freqs).__name__ not in ('int', 'list', 'tuple',
                                                                'set'):
                    raise ValueError("validation strategy param's validate_freqs's type not supported , should be int or list or tuple or set")
                if type(self.validation_freqs).__name__ == 'int':
                    if self.validation_freqs <= 0:
                        raise ValueError("validation strategy param's validate_freqs should greater than 0")
            self.sqn_param.check()
            self.stepwise_param.check()
            if self.early_stopping_rounds is None:
                pass
            else:
                if isinstance(self.early_stopping_rounds, int):
                    if self.early_stopping_rounds < 1:
                        raise ValueError("early stopping rounds should be larger than 0 when it's integer")
                    if self.validation_freqs is None:
                        raise ValueError('validation freqs must be set when early stopping is enabled')
                if not isinstance(self.metrics, list):
                    raise ValueError('metrics should be a list')
                if not isinstance(self.use_first_metric_only, bool):
                    raise ValueError('use_first_metric_only should be a boolean')
                return True