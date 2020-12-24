# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/models/prob_model.py
# Compiled at: 2019-04-01 11:32:16
# Size of source mod 2**32: 6625 bytes
import functools
from collections import OrderedDict
from tensorflow_probability import edward2 as ed
import tensorflow as tf, networkx as nx
from matplotlib import pyplot as plt
from inferpy import util
from inferpy import exceptions
from inferpy import contextmanager
from .random_variable import RandomVariable

def probmodel(builder):
    """
    Decorator to create probabilistic models. The function decorated
    must be a function which declares the Random Variables in the model.
    It is not needed that the function returns such variables (we capture
    them using ed.tape).
    """

    @functools.wraps(builder)
    def wrapper(*args, **kwargs):
        return ProbModel(builder=(lambda : builder(*args, **kwargs)))

    return wrapper


class ProbModel:
    __doc__ = '\n    Class that implements the probabilistic model functionality.\n    It is composed of a graph, capturing the variable relationships, an OrderedDict containing\n    the Random Variables in order of creation, and the function which\n    '

    def __init__(self, builder):
        self.builder = builder
        g_for_nxgraph = tf.Graph()
        with g_for_nxgraph.as_default():
            self.graph = self._build_graph()
        self.vars, self.params = self._build_model()
        self._last_expanded_vars = None
        self._last_expanded_params = None
        self._last_fitted_vars = None
        self._last_fitted_params = None

    @property
    def posterior(self):
        if self._last_fitted_vars is None:
            raise RuntimeError('posterior cannot be accessed before using the fit function.')
        return self._last_fitted_vars

    def _build_graph(self):
        with contextmanager.randvar_registry.init():
            self.builder()
            nx_graph = contextmanager.randvar_registry.get_graph()
        return nx_graph

    def _build_model(self):
        with contextmanager.randvar_registry.init(self.graph):
            with ed.tape() as (model_tape):
                self.builder()
            var_parameters = contextmanager.randvar_registry.get_var_parameters()
            model_vars = OrderedDict()
            for k, v in model_tape.items():
                registered_rv = contextmanager.randvar_registry.get_builder_variable(k)
                if registered_rv is None:
                    model_vars[k] = RandomVariable(v, name=k, is_datamodel=False, ed_cls=None, var_args=None,
                      var_kwargs=None,
                      sample_shape=())
                else:
                    model_vars[k] = registered_rv

        return (
         model_vars, var_parameters)

    def plot_graph(self):
        nx.draw((self.graph), cmap=(plt.get_cmap('jet')), with_labels=True)
        plt.show()

    @util.tf_run_ignored
    def fit(self, sample_dict, inference_method):
        if not isinstance(sample_dict, dict):
            raise TypeError('The `sample_dict` type must be dict.')
        if len(sample_dict) == 0:
            raise ValueError('The number of mapped variables must be at least 1.')
        fitted_vars, fitted_params = inference_method.run(self, sample_dict)
        self._last_fitted_vars = fitted_vars
        self._last_fitted_params = fitted_params
        return self.posterior

    @util.tf_run_allowed
    def log_prob(self, sample_dict):
        """ Computes the log probabilities of a (set of) sample(s)"""
        return {k:self.vars[k].log_prob(v) for k, v in sample_dict.items()}

    @util.tf_run_allowed
    def sum_log_prob(self, sample_dict):
        """ Computes the sum of the log probabilities of a (set of) sample(s)"""
        return tf.reduce_sum([tf.reduce_mean(lp) for lp in self.log_prob(sample_dict).values()])

    @util.tf_run_allowed
    def sample(self, size=1):
        """ Generates a sample for eache variable in the model """
        expanded_vars, expanded_params = self.expand_model(size)
        return {name:tf.convert_to_tensor(var) for name, var in expanded_vars.items()}

    def expand_model(self, size=None):
        """ Create the expanded model vars using size as plate size and return the OrderedDict """
        with contextmanager.data_model.fit(size=size):
            expanded_vars, expanded_params = self._build_model()
        self._last_expanded_vars = expanded_vars
        self._last_expanded_params = expanded_params
        return (
         expanded_vars, expanded_params)

    def _get_plate_size(self, sample_dict):
        plate_shapes = [util.iterables.get_shape(v) for k, v in sample_dict.items() if k in self.vars if self.vars[k].is_datamodel]
        plate_sizes = [s[0] if len(s) > 0 else 1 for s in plate_shapes]
        if len(plate_sizes) == 0:
            return 1
        plate_size = plate_sizes[0]
        if any((plate_size != x for x in plate_sizes[1:])):
            raise exceptions.InvalidParameterDimension('The number of elements for each mapped variable must be the same.')
        return plate_size