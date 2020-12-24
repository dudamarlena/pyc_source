# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/logistic_regression_param.py
# Compiled at: 2020-05-05 22:26:58
# Size of source mod 2**32: 15061 bytes
import copy
from federatedml.param.base_param import BaseParam
from federatedml.param.cross_validation_param import CrossValidationParam
from federatedml.param.encrypt_param import EncryptParam
from federatedml.param.encrypted_mode_calculation_param import EncryptedModeCalculatorParam
from federatedml.param.init_model_param import InitParam
from federatedml.param.predict_param import PredictParam
from federatedml.param.stepwise_param import StepwiseParam
from federatedml.param.sqn_param import StochasticQuasiNewtonParam
from federatedml.util import consts

class LogisticParam(BaseParam):
    __doc__ = "\n    Parameters used for Logistic Regression both for Homo mode or Hetero mode.\n\n    Parameters\n    ----------\n    penalty : str, 'L1', 'L2' or None. default: 'L2'\n        Penalty method used in LR. Please note that, when using encrypted version in HomoLR,\n        'L1' is not supported.\n\n    tol : float, default: 1e-5\n        The tolerance of convergence\n\n    alpha : float, default: 1.0\n        Regularization strength coefficient.\n\n    optimizer : str, 'sgd', 'rmsprop', 'adam', 'nesterov_momentum_sgd', 'sqn' or 'adagrad', default: 'sgd'\n        Optimize method, if 'sqn' has been set, sqn_param will take effect. Currently, 'sqn' support hetero mode only.\n\n    batch_size : int, default: -1\n        Batch size when updating model. -1 means use all data in a batch. i.e. Not to use mini-batch strategy.\n\n    learning_rate : float, default: 0.01\n        Learning rate\n\n    max_iter : int, default: 100\n        The maximum iteration for training.\n\n    early_stop : str, 'diff', 'weight_diff' or 'abs', default: 'diff'\n        Method used to judge converge or not.\n            a)\tdiff： Use difference of loss between two iterations to judge whether converge.\n            b)  weight_diff: Use difference between weights of two consecutive iterations\n            c)\tabs: Use the absolute value of loss to judge whether converge. i.e. if loss < eps, it is converged.\n\n    decay: int or float, default: 1\n        Decay rate for learning rate. learning rate will follow the following decay schedule.\n        lr = lr0/(1+decay*t) if decay_sqrt is False. If decay_sqrt is True, lr = lr0 / sqrt(1+decay*t)\n        where t is the iter number.\n\n    decay_sqrt: Bool, default: True\n        lr = lr0/(1+decay*t) if decay_sqrt is False, otherwise, lr = lr0 / sqrt(1+decay*t)\n\n    encrypt_param: EncryptParam object, default: default EncryptParam object\n\n    predict_param: PredictParam object, default: default PredictParam object\n\n    cv_param: CrossValidationParam object, default: default CrossValidationParam object\n\n    multi_class: str, 'ovr', default: 'ovr'\n        If it is a multi_class task, indicate what strategy to use. Currently, support 'ovr' short for one_vs_rest only.\n\n    validation_freqs: int, list, tuple, set, or None\n        validation frequency during training.\n\n    early_stopping_rounds: int, default: None\n        Will stop training if one metric doesn’t improve in last early_stopping_round rounds\n\n    metrics: list, default: []\n        Indicate when executing evaluation during train process, which metrics will be used. If set as empty,\n        default metrics for specific task type will be used. As for binary classification, default metrics are\n        ['auc', 'ks']\n\n    use_first_metric_only: bool, default: False\n        Indicate whether use the first metric only for early stopping judgement.\n\n    "

    def __init__(self, penalty='L2', tol=1e-05, alpha=1.0, optimizer='sgd', batch_size=-1, learning_rate=0.01, init_param=InitParam(), max_iter=100, early_stop='diff', encrypt_param=EncryptParam(), predict_param=PredictParam(), cv_param=CrossValidationParam(), decay=1, decay_sqrt=True, multi_class='ovr', validation_freqs=None, early_stopping_rounds=None, stepwise_param=StepwiseParam(), metrics=[], use_first_metric_only=False):
        super(LogisticParam, self).__init__()
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
        self.predict_param = copy.deepcopy(predict_param)
        self.cv_param = copy.deepcopy(cv_param)
        self.decay = decay
        self.decay_sqrt = decay_sqrt
        self.multi_class = multi_class
        self.validation_freqs = validation_freqs
        self.stepwise_param = copy.deepcopy(stepwise_param)
        self.early_stopping_rounds = early_stopping_rounds
        self.metrics = metrics
        self.use_first_metric_only = use_first_metric_only

    def check(self):
        descr = "logistic_param's"
        if self.penalty is None:
            pass
        elif type(self.penalty).__name__ != 'str':
            raise ValueError("logistic_param's penalty {} not supported, should be str type".format(self.penalty))
        else:
            self.penalty = self.penalty.upper()
            if self.penalty not in [consts.L1_PENALTY, consts.L2_PENALTY, 'NONE']:
                raise ValueError("logistic_param's penalty not supported, penalty should be 'L1', 'L2' or 'none'")
            else:
                assert isinstance(self.tol, (int, float)), "logistic_param's tol {} not supported, should be float type".format(self.tol)
            if type(self.alpha).__name__ not in ('float', 'int'):
                raise ValueError("logistic_param's alpha {} not supported, should be float or int type".format(self.alpha))
        if type(self.optimizer).__name__ != 'str':
            raise ValueError("logistic_param's optimizer {} not supported, should be str type".format(self.optimizer))
        else:
            self.optimizer = self.optimizer.lower()
            if self.optimizer not in ('sgd', 'rmsprop', 'adam', 'adagrad', 'nesterov_momentum_sgd',
                                      'sqn'):
                raise ValueError("logistic_param's optimizer not supported, optimizer should be 'sgd', 'rmsprop', 'adam', 'nesterov_momentum_sgd', 'sqn' or 'adagrad'")
            elif not self.batch_size != -1 or type(self.batch_size).__name__ not in ('int', ) or self.batch_size < consts.MIN_BATCH_SIZE:
                raise ValueError(descr + ' {} not supported, should be larger than {} or -1 represent for all data'.format(self.batch_size, consts.MIN_BATCH_SIZE))
            if not isinstance(self.learning_rate, (float, int)):
                raise ValueError("logistic_param's learning_rate {} not supported, should be float or int type".format(self.learning_rate))
            else:
                self.init_param.check()
                if type(self.max_iter).__name__ != 'int':
                    raise ValueError("logistic_param's max_iter {} not supported, should be int type".format(self.max_iter))
                else:
                    if self.max_iter <= 0:
                        raise ValueError("logistic_param's max_iter must be greater or equal to 1")
        if type(self.early_stop).__name__ != 'str':
            raise ValueError("logistic_param's early_stop {} not supported, should be str type".format(self.early_stop))
        else:
            self.early_stop = self.early_stop.lower()
            if self.early_stop not in ('diff', 'abs', 'weight_diff'):
                raise ValueError("logistic_param's early_stop not supported, converge_func should be 'diff', 'weight_diff' or 'abs'")
            self.encrypt_param.check()
            self.predict_param.check()
            if self.encrypt_param.method not in [consts.PAILLIER, None]:
                raise ValueError("logistic_param's encrypted method support 'Paillier' or None only")
            if type(self.decay).__name__ not in ('int', 'float'):
                raise ValueError("logistic_param's decay {} not supported, should be 'int' or 'float'".format(self.decay))
            if type(self.decay_sqrt).__name__ not in ('bool', ):
                raise ValueError("logistic_param's decay_sqrt {} not supported, should be 'bool'".format(self.decay_sqrt))
            self.stepwise_param.check()
            if self.early_stopping_rounds is None:
                pass
            else:
                if isinstance(self.early_stopping_rounds, int):
                    if self.early_stopping_rounds < 1:
                        raise ValueError("early stopping rounds should be larger than 0 when it's integer")
                    if self.validation_freqs is None:
                        raise ValueError('validation freqs must be set when early stopping is enabled')
                return True


class HomoLogisticParam(LogisticParam):
    __doc__ = '\n    Parameters\n    ----------\n    re_encrypt_batches : int, default: 2\n        Required when using encrypted version HomoLR. Since multiple batch updating coefficient may cause\n        overflow error. The model need to be re-encrypt for every several batches. Please be careful when setting\n        this parameter. Too large batches may cause training failure.\n\n    aggregate_iters : int, default: 1\n        Indicate how many iterations are aggregated once.\n\n    '

    def __init__(self, penalty='L2', tol=1e-05, alpha=1.0, optimizer='sgd', batch_size=-1, learning_rate=0.01, init_param=InitParam(), max_iter=100, early_stop='diff', encrypt_param=EncryptParam(), re_encrypt_batches=2, predict_param=PredictParam(), cv_param=CrossValidationParam(), decay=1, decay_sqrt=True, aggregate_iters=1, multi_class='ovr', validation_freqs=None, early_stopping_rounds=None, metrics=[
 'auc', 'ks'], use_first_metric_only=False):
        super(HomoLogisticParam, self).__init__(penalty=penalty, tol=tol, alpha=alpha, optimizer=optimizer, batch_size=batch_size,
          learning_rate=learning_rate,
          init_param=init_param,
          max_iter=max_iter,
          early_stop=early_stop,
          encrypt_param=encrypt_param,
          predict_param=predict_param,
          cv_param=cv_param,
          multi_class=multi_class,
          validation_freqs=validation_freqs,
          decay=decay,
          decay_sqrt=decay_sqrt,
          early_stopping_rounds=early_stopping_rounds,
          metrics=metrics,
          use_first_metric_only=use_first_metric_only)
        self.re_encrypt_batches = re_encrypt_batches
        self.aggregate_iters = aggregate_iters

    def check(self):
        super().check()
        if type(self.re_encrypt_batches).__name__ != 'int':
            raise ValueError("logistic_param's re_encrypt_batches {} not supported, should be int type".format(self.re_encrypt_batches))
        else:
            if self.re_encrypt_batches < 0:
                raise ValueError("logistic_param's re_encrypt_batches must be greater or equal to 0")
            else:
                assert isinstance(self.aggregate_iters, int), "logistic_param's aggregate_iters {} not supported, should be int type".format(self.aggregate_iters)
            if self.encrypt_param.method == consts.PAILLIER:
                if self.optimizer != 'sgd':
                    raise ValueError("Paillier encryption mode supports 'sgd' optimizer method only.")
                if self.penalty == consts.L1_PENALTY:
                    raise ValueError("Paillier encryption mode supports 'L2' penalty or None only.")
            if self.optimizer == 'sqn':
                raise ValueError("'sqn' optimizer is supported for hetero mode only.")
            return True


class HeteroLogisticParam(LogisticParam):

    def __init__(self, penalty='L2', tol=1e-05, alpha=1.0, optimizer='sgd', batch_size=-1, learning_rate=0.01, init_param=InitParam(), max_iter=100, early_stop='diff', encrypted_mode_calculator_param=EncryptedModeCalculatorParam(), predict_param=PredictParam(), cv_param=CrossValidationParam(), decay=1, decay_sqrt=True, sqn_param=StochasticQuasiNewtonParam(), multi_class='ovr', validation_freqs=None, early_stopping_rounds=None, metrics=[
 'auc', 'ks'], use_first_metric_only=False):
        super(HeteroLogisticParam, self).__init__(penalty=penalty, tol=tol, alpha=alpha, optimizer=optimizer, batch_size=batch_size,
          learning_rate=learning_rate,
          init_param=init_param,
          max_iter=max_iter,
          early_stop=early_stop,
          predict_param=predict_param,
          cv_param=cv_param,
          decay=decay,
          decay_sqrt=decay_sqrt,
          multi_class=multi_class,
          validation_freqs=validation_freqs,
          early_stopping_rounds=early_stopping_rounds,
          metrics=metrics,
          use_first_metric_only=use_first_metric_only)
        self.encrypted_mode_calculator_param = copy.deepcopy(encrypted_mode_calculator_param)
        self.sqn_param = copy.deepcopy(sqn_param)

    def check(self):
        super().check()
        self.encrypted_mode_calculator_param.check()
        self.sqn_param.check()
        return True