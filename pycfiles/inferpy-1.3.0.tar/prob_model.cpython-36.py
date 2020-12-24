# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/models/prob_model.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 8835 bytes
import functools
from collections import OrderedDict
from tensorflow_probability import edward2 as ed
import tensorflow as tf, networkx as nx, warnings
from inferpy import util
from inferpy import contextmanager
from inferpy.queries import Query
from .random_variable import RandomVariable
from inferpy.data.loaders import build_data_loader

def probmodel(builder):
    """
    Decorator to create probabilistic models. The function decorated
    must be a function which declares the Random Variables in the model.
    It is not required that the function returns such variables (they are
    captured using ed.tape).
    """

    @functools.wraps(builder)
    def wrapper(*args, **kwargs):

        @util.tf_run_ignored
        def fn():
            return builder(*args, **kwargs)

        return ProbModel(builder=fn)

    return wrapper


class ProbModel:
    __doc__ = '\n    Class that implements the probabilistic model functionality.\n    It is composed of a graph, capturing the variable relationships, an OrderedDict containing\n    the Random Variables/Parameters in order of creation, and the function which declare the\n    Random Variables/Parameters.\n    '

    def __init__(self, builder):
        self.builder = builder
        g_for_nxgraph = tf.Graph()
        with g_for_nxgraph.as_default():
            with tf.Session() as (sess):
                try:
                    default_sess = util.session.swap_session(sess)
                    self.graph = self._build_graph()
                finally:
                    util.session.swap_session(default_sess)

        self.vars, self.params = self._build_model()
        self.inference_method = None
        self.observed_vars = []
        self.layer_losses = None

    def prior(self, target_names=None, data={}, size_datamodel=1):
        if size_datamodel > 1:
            variables, _ = self.expand_model(size_datamodel)
        else:
            if size_datamodel == 1:
                variables = self.vars
            else:
                raise ValueError('size_datamodel must be greater than 0 but it is {}'.format(size_datamodel))
        util.init_uninit_vars()
        return Query(variables, target_names, data)

    def posterior(self, target_names=None, data={}):
        if self.inference_method is None:
            raise RuntimeError('posterior cannot be used before using the fit function.')
        if target_names is None:
            target_names = [name for name in self.vars.keys() if name not in self.observed_vars]
        else:
            if any(var in self.observed_vars for var in target_names):
                raise ValueError('target_names must correspond to not observed variables during the inference:                     {}'.format([v for v in self.vars.keys() if v not in self.observed_vars]))
        return self.inference_method.posterior(target_names, data)

    def posterior_predictive(self, target_names=None, data={}):
        if self.inference_method is None:
            raise RuntimeError('posterior_preductive cannot be used before using the fit function.')
        if target_names is None:
            target_names = [name for name in self.vars.keys() if name in self.observed_vars]
        else:
            if any(var not in self.observed_vars for var in target_names):
                raise ValueError('target_names must correspond to observed variables during the inference:                     {}'.format(self.observed_vars))
        return self.inference_method.posterior_predictive(target_names, data)

    def _build_graph(self):
        with contextmanager.randvar_registry.init():
            self.builder()
            nx_graph = contextmanager.randvar_registry.get_graph()
        return nx_graph

    def _build_model(self):
        with contextmanager.randvar_registry.init(self.graph):
            with contextmanager.layer_registry.init():
                with ed.tape() as (model_tape):
                    self.builder()
                self.layer_losses = contextmanager.layer_registry.get_losses()
            var_parameters = contextmanager.randvar_registry.get_var_parameters()
            model_vars = OrderedDict()
            for k, v in model_tape.items():
                registered_rv = contextmanager.randvar_registry.get_variable(k)
                if registered_rv is None:
                    model_vars[k] = RandomVariable(v, name=k, is_datamodel=False, ed_cls=None, var_args=None,
                      var_kwargs=None,
                      sample_shape=())
                else:
                    model_vars[k] = registered_rv

        return (
         model_vars, var_parameters)

    def plot_graph(self):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print('The function plot_graph requires to install inferpy[visualization]')
            raise

        nx.draw((self.graph), cmap=(plt.get_cmap('jet')), with_labels=True)
        plt.show()

    @util.tf_run_ignored
    def fit(self, data, inference_method):
        data_loader = build_data_loader(data)
        plate_size = data_loader.size
        if len(data_loader.variables) == 0:
            raise ValueError('The number of mapped variables must be at least 1.')
        if self.inference_method:
            warnings.warn('Fit was called before. This will restart the inference method and                 re-build the expanded model.')
        self.inference_method = inference_method
        with (util.interceptor.enable_interceptor)(*self.inference_method.get_interceptable_condition_variables()):
            inference_method.compile(self, plate_size, self.layer_losses)
            inference_method.update(data_loader)
        self.observed_vars = data_loader.variables

    def expand_model(self, size=1):
        """ Create the expanded model vars using size as plate size and return the OrderedDict """
        with contextmanager.data_model.fit(size=size):
            expanded_vars, expanded_params = self._build_model()
        return (expanded_vars, expanded_params)