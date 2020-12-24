# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/boosting_tree_param.py
# Compiled at: 2020-05-05 22:26:58
# Size of source mod 2**32: 17422 bytes
from federatedml.param.base_param import BaseParam
from federatedml.param.encrypt_param import EncryptParam
from federatedml.param.encrypted_mode_calculation_param import EncryptedModeCalculatorParam
from federatedml.param.cross_validation_param import CrossValidationParam
from federatedml.param.predict_param import PredictParam
from federatedml.util import consts
import copy, collections

class ObjectiveParam(BaseParam):
    __doc__ = "\n    Define objective parameters that used in federated ml.\n\n    Parameters\n    ----------\n    objective : None or str, accepted None,'cross_entropy','lse','lae','log_cosh','tweedie','fair','huber' only,\n                None in host's config, should be str in guest'config.\n                when task_type is classification, only support cross_enctropy,\n                other 6 types support in regression task. default: None\n\n    params : None or list, should be non empty list when objective is 'tweedie','fair','huber',\n             first element of list shoulf be a float-number large than 0.0 when objective is 'fair','huber',\n             first element of list should be a float-number in [1.0, 2.0) when objective is 'tweedie'\n    "

    def __init__(self, objective=None, params=None):
        self.objective = objective
        self.params = params

    def check(self, task_type=None):
        if self.objective is None:
            return True
        descr = "objective param's"
        if task_type not in [consts.CLASSIFICATION, consts.REGRESSION]:
            self.objective = self.check_and_change_lower(self.objective, [
             'cross_entropy', 'lse', 'lae', 'huber', 'fair',
             'log_cosh', 'tweedie'], descr)
        if task_type == consts.CLASSIFICATION:
            if self.objective != 'cross_entropy':
                raise ValueError("objective param's objective {} not supported".format(self.objective))
        else:
            if task_type == consts.REGRESSION:
                self.objective = self.check_and_change_lower(self.objective, [
                 'lse', 'lae', 'huber', 'fair', 'log_cosh', 'tweedie'], descr)
                params = self.params
                if self.objective in ('huber', 'fair', 'tweedie') and not type(params).__name__ != 'list':
                    if len(params) < 1:
                        raise ValueError("objective param's params {} not supported, should be non-empty list".format(params))
                    if type(params[0]).__name__ not in ('float', 'int', 'long'):
                        raise ValueError("objective param's params[0] {} not supported".format(self.params[0]))
                    if self.objective == 'tweedie' and not params[0] < 1:
                        if params[0] >= 2:
                            raise ValueError('in tweedie regression, objective params[0] should betweend [1, 2)')
                    if not self.objective == 'fair':
                        pass
                    if params[0] <= 0.0:
                        raise ValueError('in {} regression, objective params[0] should greater than 0.0'.format(self.objective))
            return True


class DecisionTreeParam(BaseParam):
    __doc__ = '\n    Define decision tree parameters that used in federated ml.\n\n    Parameters\n    ----------\n    criterion_method : str, accepted "xgboost" only, the criterion function to use, default: \'xgboost\'\n\n    criterion_params: list, should be non empty and first element is float-number, default: 0.1.\n\n    max_depth: int, positive integer, the max depth of a decision tree, default: 5\n\n    min_sample_split: int, least quantity of nodes to split, default: 2\n\n    min_impurity_split: float, least gain of a single split need to reach, default: 1e-3\n\n    min_leaf_node: int, when samples no more than min_leaf_node, it becomes a leave, default: 1\n\n    max_split_nodes: int, positive integer, we will use no more than max_split_nodes to\n                      parallel finding their splits in a batch, for memory consideration. default is 65536\n\n    n_iter_no_change: bool, accepted True,False only, if set to True, tol will use to consider\n                      stop tree growth. default: True\n\n    feature_importance_type: str, support \'split\', \'gain\' only.\n                             if is \'split\', feature_importances calculate by feature split times,\n                             if is \'gain\', feature_importances calculate by feature split gain.\n                             default: \'split\'\n\n    tol: float, only use when n_iter_no_change is set to True, default: 0.001\n\n    use_missing: bool, accepted True, False only, use missing value in training process or not. default: False\n\n    zero_as_missing: bool, accepted True, False only, regard 0 as missing value or not,\n                     will be use only if use_missing=True, default: False\n    '

    def __init__(self, criterion_method='xgboost', criterion_params=[0.1], max_depth=5, min_sample_split=2, min_imputiry_split=0.001, min_leaf_node=1, max_split_nodes=consts.MAX_SPLIT_NODES, feature_importance_type='split', n_iter_no_change=True, tol=0.001, use_missing=False, zero_as_missing=False):
        self.criterion_method = criterion_method
        self.criterion_params = criterion_params
        self.max_depth = max_depth
        self.min_sample_split = min_sample_split
        self.min_impurity_split = min_imputiry_split
        self.min_leaf_node = min_leaf_node
        self.max_split_nodes = max_split_nodes
        self.feature_importance_type = feature_importance_type
        self.n_iter_no_change = n_iter_no_change
        self.tol = tol
        self.use_missing = use_missing
        self.zero_as_missing = zero_as_missing

    def check(self):
        descr = 'decision tree param'
        self.criterion_method = self.check_and_change_lower(self.criterion_method, [
         'xgboost'], descr)
        if type(self.criterion_params).__name__ != 'list':
            raise ValueError("decision tree param's criterion_params {} not supported, should be list".format(self.criterion_params))
        if len(self.criterion_params) == 0:
            raise ValueError("decisition tree param's criterio_params should be non empty")
        if type(self.criterion_params[0]).__name__ not in ('int', 'long', 'float'):
            raise ValueError("decision tree param's criterion_params element shoubld be numeric")
        if type(self.max_depth).__name__ not in ('int', 'long'):
            raise ValueError("decision tree param's max_depth {} not supported, should be integer".format(self.max_depth))
        if self.max_depth < 1:
            raise ValueError("decision tree param's max_depth should be positive integer, no less than 1")
        if type(self.min_sample_split).__name__ not in ('int', 'long'):
            raise ValueError("decision tree param's min_sample_split {} not supported, should be integer".format(self.min_sample_split))
        if type(self.min_impurity_split).__name__ not in ('int', 'long', 'float'):
            raise ValueError("decision tree param's min_impurity_split {} not supported, should be numeric".format(self.min_impurity_split))
        if type(self.min_leaf_node).__name__ not in ('int', 'long'):
            raise ValueError("decision tree param's min_leaf_node {} not supported, should be integer".format(self.min_leaf_node))
        if type(self.max_split_nodes).__name__ not in ('int', 'long') or self.max_split_nodes < 1:
            raise ValueError("decision tree param's max_split_nodes {} not supported, " + 'should be positive integer between 1 and {}'.format(self.max_split_nodes, consts.MAX_SPLIT_NODES))
        if type(self.n_iter_no_change).__name__ != 'bool':
            raise ValueError("decision tree param's n_iter_no_change {} not supported, should be bool type".format(self.n_iter_no_change))
        if type(self.tol).__name__ not in ('float', 'int', 'long'):
            raise ValueError("decision tree param's tol {} not supported, should be numeric".format(self.tol))
        self.feature_importance_type = self.check_and_change_lower(self.feature_importance_type, [
         'split', 'gain'], descr)
        return True


class BoostingTreeParam(BaseParam):
    __doc__ = '\n    Define boosting tree parameters that used in federated ml.\n\n    Parameters\n    ----------\n    task_type : str, accepted \'classification\', \'regression\' only, default: \'classification\'\n\n    tree_param : DecisionTreeParam Object, default: DecisionTreeParam()\n\n    objective_param : ObjectiveParam Object, default: ObjectiveParam()\n\n    learning_rate : float, accepted float, int or long only, the learning rate of secure boost. default: 0.3\n\n    num_trees : int, accepted int, float only, the max number of trees to build. default: 5\n\n    subsample_feature_rate : float, a float-number in [0, 1], default: 0.8\n\n    n_iter_no_change : bool,\n        when True and residual error less than tol, tree building process will stop. default: True\n\n    encrypt_param : EncodeParam Object, encrypt method use in secure boost, default: EncryptParam(), this parameter\n                    is only for hetero-secureboost\n\n    bin_num: int, positive integer greater than 1, bin number use in quantile. default: 32\n\n    encrypted_mode_calculator_param: EncryptedModeCalculatorParam object, the calculation mode use in secureboost,\n                                     default: EncryptedModeCalculatorParam(), only for hetero-secureboost\n\n    use_missing: bool, accepted True, False only, use missing value in training process or not. default: False\n\n    zero_as_missing: bool, accepted True, False only, regard 0 as missing value or not,\n                     will be use only if use_missing=True, default: False\n\n    validation_freqs: None or positive integer or container object in python. Do validation in training process or Not.\n                      if equals None, will not do validation in train process;\n                      if equals positive integer, will validate data every validation_freqs epochs passes;\n                      if container object in python, will validate data if epochs belong to this container.\n                        e.g. validation_freqs = [10, 15], will validate data when epoch equals to 10 and 15.\n                      Default: None\n                      The default value is None, 1 is suggested. You can set it to a number larger than 1 in order to\n                      speed up training by skipping validation rounds. When it is larger than 1, a number which is\n                      divisible by "num_trees" is recommended, otherwise, you will miss the validation scores\n                      of last training iteration.\n\n    early_stopping_rounds: should be a integer larger than 0，will stop training if one metric of one validation data\n                            doesn’t improve in last early_stopping_round rounds，\n                            need to set validation freqs and will check early_stopping every at every validation epoch,\n\n    metrics: list, default: []\n             Specify which metrics to be used when performing evaluation during training process.\n             If set as empty, default metrics will be used. For regression tasks, default metrics are\n             [\'root_mean_squared_error\', \'mean_absolute_error\']， For binary-classificatiin tasks, default metrics\n             are [\'auc\', \'ks\']. For multi-classification tasks, default metrics are [\'accuracy\', \'precision\', \'recall\']\n\n    use_first_metric_only: use only the first metric for early stopping\n    '

    def __init__(self, tree_param=DecisionTreeParam(), task_type=consts.CLASSIFICATION, objective_param=ObjectiveParam(), learning_rate=0.3, num_trees=5, subsample_feature_rate=0.8, n_iter_no_change=True, tol=0.0001, encrypt_param=EncryptParam(), bin_num=32, use_missing=False, zero_as_missing=False, encrypted_mode_calculator_param=EncryptedModeCalculatorParam(), predict_param=PredictParam(), cv_param=CrossValidationParam(), validation_freqs=None, early_stopping_rounds=None, metrics=None, use_first_metric_only=True):
        self.tree_param = copy.deepcopy(tree_param)
        self.task_type = task_type
        self.objective_param = copy.deepcopy(objective_param)
        self.learning_rate = learning_rate
        self.num_trees = num_trees
        self.subsample_feature_rate = subsample_feature_rate
        self.n_iter_no_change = n_iter_no_change
        self.tol = tol
        self.encrypt_param = copy.deepcopy(encrypt_param)
        self.bin_num = bin_num
        self.use_missing = use_missing
        self.zero_as_missing = zero_as_missing
        self.encrypted_mode_calculator_param = copy.deepcopy(encrypted_mode_calculator_param)
        self.predict_param = copy.deepcopy(predict_param)
        self.cv_param = copy.deepcopy(cv_param)
        self.validation_freqs = validation_freqs
        self.early_stopping_rounds = early_stopping_rounds
        self.metrics = metrics
        self.use_first_metric_only = use_first_metric_only

    def check(self):
        self.tree_param.check()
        descr = "boosting tree param's"
        if self.task_type not in [consts.CLASSIFICATION, consts.REGRESSION]:
            raise ValueError("boosting tree param's task_type {} not supported, should be {} or {}".format(self.task_type, consts.CLASSIFICATION, consts.REGRESSION))
        self.objective_param.check(self.task_type)
        if type(self.learning_rate).__name__ not in ('float', 'int', 'long'):
            raise ValueError("boosting tree param's learning_rate {} not supported, should be numeric".format(self.learning_rate))
        if type(self.num_trees).__name__ not in ('int', 'long') or self.num_trees < 1:
            raise ValueError("boosting tree param's num_trees {} not supported, should be postivie integer".format(self.num_trees))
        if type(self.subsample_feature_rate).__name__ not in ('float', 'int', 'long') or self.subsample_feature_rate < 0 or self.subsample_feature_rate > 1:
            raise ValueError("boosting tree param's subsample_feature_rate should be a numeric number between 0 and 1")
        if type(self.n_iter_no_change).__name__ != 'bool':
            raise ValueError("boosting tree param's n_iter_no_change {} not supported, should be bool type".format(self.n_iter_no_change))
        if type(self.tol).__name__ not in ('float', 'int', 'long'):
            raise ValueError("boosting tree param's tol {} not supported, should be numeric".format(self.tol))
        self.encrypt_param.check()
        if type(self.bin_num).__name__ not in ('int', 'long') or self.bin_num < 2:
            raise ValueError("boosting tree param's bin_num {} not supported, should be positive integer greater than 1".format(self.bin_num))
        self.encrypted_mode_calculator_param.check()
        if self.validation_freqs is None:
            pass
        else:
            if isinstance(self.validation_freqs, int):
                if self.validation_freqs < 1:
                    raise ValueError("validation_freqs should be larger than 0 when it's integer")
            elif not isinstance(self.validation_freqs, collections.Container):
                raise ValueError('validation_freqs should be None or positive integer or container')
            if self.early_stopping_rounds is None:
                pass
            else:
                if isinstance(self.early_stopping_rounds, int):
                    if self.early_stopping_rounds < 1:
                        raise ValueError("early stopping rounds should be larger than 0 when it's integer")
                    if self.validation_freqs is None:
                        raise ValueError('validation freqs must be set when early stopping is enabled')
                if self.metrics is not None and not isinstance(self.metrics, list):
                    raise ValueError('metrics should be a list')
                return True