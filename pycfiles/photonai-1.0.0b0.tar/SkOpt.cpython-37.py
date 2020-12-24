# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/optimization/SkOpt.py
# Compiled at: 2019-09-26 08:58:51
# Size of source mod 2**32: 3380 bytes
from .OptimizationStrategies import PhotonBaseOptimizer
from .Hyperparameters import FloatRange, IntegerRange
from .Hyperparameters import Categorical as PhotonCategorical
from skopt import Optimizer
from skopt.space import Real, Integer
import skopt.space as skoptCategorical
import numpy as np

class SkOptOptimizer(PhotonBaseOptimizer):

    def __init__(self, num_iterations: int=20, base_estimator='ET'):
        self.optimizer = None
        self.hyperparameter_list = []
        self.metric_to_optimize = ''
        self.ask = self.ask_generator()
        self.num_iterations = num_iterations
        self.base_estimator = base_estimator
        self.maximize_metric = True
        self.constant_dictionary = {}

    def prepare(self, pipeline_elements: list, maximize_metric: bool):
        self.hyperparameter_list = []
        self.maximize_metric = maximize_metric
        space = []
        for pipe_element in pipeline_elements:
            for name, value in pipe_element.hyperparameters.items():
                if isinstance(value, list):
                    if len(value) < 2:
                        self.constant_dictionary[name] = value[0]
                        continue
                    elif isinstance(value, PhotonCategorical) and len(value.values) < 2:
                        self.constant_dictionary[name] = value.values[0]
                        continue
                    skopt_param = self._convert_PHOTON_to_skopt_space(value, name)
                    if skopt_param is not None:
                        space.append(skopt_param)

        self.optimizer = Optimizer(space, self.base_estimator)
        self.ask = self.ask_generator()

    def _convert_PHOTON_to_skopt_space(self, hyperparam: object, name: str):
        if not hyperparam:
            return
        self.hyperparameter_list.append(name)
        if isinstance(hyperparam, PhotonCategorical):
            return skoptCategorical((hyperparam.values), name=name)
        if isinstance(hyperparam, list):
            return skoptCategorical(hyperparam, name=name)
        if isinstance(hyperparam, FloatRange):
            return Real((hyperparam.start), (hyperparam.stop), name=name)
        if isinstance(hyperparam, IntegerRange):
            return Integer((hyperparam.start), (hyperparam.stop), name=name)

    def ask_generator(self):
        for i in range(self.num_iterations):
            next_config_list = self.optimizer.ask()
            next_config_dict = {self.hyperparameter_list[number]:self._convert_to_native(value) for number, value in enumerate(next_config_list)}
            yield next_config_dict

    def _convert_to_native(self, obj):
        if type(obj).__module__ == np.__name__:
            return np.asscalar(obj)
        return obj

    def tell(self, config, performance):
        config_values = [config[name] for name in self.hyperparameter_list]
        best_config_metric_performance = performance[1]
        if self.maximize_metric:
            best_config_metric_performance = -best_config_metric_performance
        self.optimizer.tell(config_values, best_config_metric_performance)