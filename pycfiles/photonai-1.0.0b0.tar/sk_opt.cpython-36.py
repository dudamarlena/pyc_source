# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/optimization/scikit_optimize/sk_opt.py
# Compiled at: 2019-09-11 10:06:07
# Size of source mod 2**32: 6220 bytes
from skopt import Optimizer
from skopt.space import Real, Integer
from skopt.space import Categorical as skoptCategorical
from skopt.plots import plot_evaluations, plot_objective
import numpy as np, matplotlib.pylab as plt
from photonai.optimization import FloatRange, IntegerRange
from photonai.optimization.base_optimizer import PhotonBaseOptimizer
from photonai.optimization import Categorical as PhotonCategorical
from photonai.photonlogger import Logger

class SkOptOptimizer(PhotonBaseOptimizer):

    def __init__(self, num_iterations: int=20, acq_func: str='gp_hedge', acq_func_kwargs: dict=None):
        self.optimizer = None
        self.hyperparameter_list = []
        self.metric_to_optimize = ''
        self.ask = self.ask_generator()
        self.num_iterations = num_iterations
        self.acq_func = acq_func
        self.acq_func_kwargs = acq_func_kwargs
        self.maximize_metric = True
        self.constant_dictionary = {}

    def prepare(self, pipeline_elements: list, maximize_metric: bool):
        self.hyperparameter_list = []
        self.maximize_metric = maximize_metric
        space = []
        for pipe_element in pipeline_elements:
            if hasattr(pipe_element, 'hyperparameters'):
                for name, value in pipe_element.hyperparameters.items():
                    if isinstance(value, list):
                        if len(value) < 2:
                            self.constant_dictionary[name] = value[0]
                            continue
                        if isinstance(value, PhotonCategorical):
                            if len(value.values) < 2:
                                self.constant_dictionary[name] = value.values[0]
                                continue
                        skopt_param = self._convert_PHOTON_to_skopt_space(value, name)
                        if skopt_param is not None:
                            space.append(skopt_param)

        if len(space) == 0:
            Logger().warn('Did not find any hyperparameters to convert into skopt space')
            self.optimizer = None
        else:
            self.optimizer = Optimizer(space, 'ET', acq_func=(self.acq_func), acq_func_kwargs=(self.acq_func_kwargs))
        self.ask = self.ask_generator()

    def _convert_PHOTON_to_skopt_space(self, hyperparam: object, name: str):
        if not hyperparam:
            return
        else:
            self.hyperparameter_list.append(name)
            if isinstance(hyperparam, PhotonCategorical):
                return skoptCategorical((hyperparam.values), name=name)
            if isinstance(hyperparam, list):
                return skoptCategorical(hyperparam, name=name)
            if isinstance(hyperparam, FloatRange):
                if hyperparam.range_type == 'linspace':
                    return Real((hyperparam.start), (hyperparam.stop), name=name, prior='uniform')
                else:
                    if hyperparam.range_type == 'logspace':
                        return Real((hyperparam.start), (hyperparam.stop), name=name, prior='log-uniform')
                    return Real((hyperparam.start), (hyperparam.stop), name=name)
            elif isinstance(hyperparam, IntegerRange):
                return Integer((hyperparam.start), (hyperparam.stop), name=name)

    def ask_generator(self):
        if self.optimizer is None:
            yield {}
        else:
            for i in range(self.num_iterations):
                next_config_list = self.optimizer.ask()
                next_config_dict = {self.hyperparameter_list[number]:self._convert_to_native(value) for number, value in enumerate(next_config_list)}
                yield next_config_dict

    def _convert_to_native(self, obj):
        if type(obj).__module__ == np.__name__:
            return np.asscalar(obj)
        else:
            return obj

    def tell(self, config, performance):
        if self.optimizer is not None:
            config_values = [config[name] for name in self.hyperparameter_list]
            best_config_metric_performance = performance[1]
            if self.maximize_metric:
                if isinstance(best_config_metric_performance, list):
                    print('BEST CONFIG METRIC PERFORMANCE: ' + str(best_config_metric_performance))
                    best_config_metric_performance = best_config_metric_performance[0]
                best_config_metric_performance = -best_config_metric_performance
            self.optimizer.tell(config_values, best_config_metric_performance)

    def plot_evaluations(self):
        results = SkoptResults()
        results.space = self.optimizer.space
        results.x_iters = self.optimizer.Xi
        results = self._convert_categorical_hyperparameters(results)
        results.x = results.x_iters[np.argmin(self.optimizer.yi)]
        plt.figure(figsize=(10, 10))
        return plot_evaluations(results)

    def plot_objective(self):
        results = SkoptResults()
        results.space = self.optimizer.space
        results.x_iters = self.optimizer.Xi
        results = self._convert_categorical_hyperparameters(results)
        results.x = results.x_iters[np.argmin(self.optimizer.yi)]
        results.models = self.optimizer.models
        plt.figure(figsize=(10, 10))
        return plot_objective(results)

    def _convert_categorical_hyperparameters(self, results):
        parameter_types = list()
        for i, dim in enumerate(results.space.dimensions):
            if isinstance(dim, skoptCategorical):
                parameter_types.append(dim.transformer)
                setattr(results.space.dimensions[i], 'categories', dim.transformed_bounds)
            else:
                parameter_types.append(False)

        for i, xs in enumerate(results.x_iters):
            for k, xsk in enumerate(xs):
                if parameter_types[k]:
                    results.x_iters[i][k] = parameter_types[k].transform([xsk])

        return results


class SkoptResults:

    def __init__(self):
        self.space = None
        self.x_iters = None
        self.x = None
        self.models = None