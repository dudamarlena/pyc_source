# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/queries/query.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 5077 bytes
import numpy as np, functools
from inferpy import contextmanager
from inferpy import util

def flatten_result(f):

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        simplify_result = kwargs.pop('simplify_result', True)
        result = f(*args, **kwargs)
        if simplify_result:
            if len(result) == 1:
                return result[list(result.keys())[0]]
        return result

    return wrapper


class Query:

    def __init__(self, variables, target_names=None, data={}, enable_interceptor_variables=(None, None)):
        if isinstance(target_names, str):
            target_names = [
             target_names]
        if target_names:
            if any(name not in variables for name in target_names):
                raise ValueError('Target names must correspond to variable names')
        self.target_variables = variables if not target_names else {k:v for k, v in variables.items() if k in target_names}
        self.observed_variables = variables
        self.data = data
        self.enable_interceptor_variables = enable_interceptor_variables

    @flatten_result
    @util.tf_run_ignored
    def log_prob(self):
        """ Computes the log probabilities of a (set of) sample(s)"""
        with (util.interceptor.enable_interceptor)(*self.enable_interceptor_variables):
            with contextmanager.observe(self.observed_variables, self.data):
                result = util.runtime.try_run({k:v.log_prob(v.value) for k, v in self.target_variables.items()})
        return result

    def sum_log_prob(self):
        """ Computes the sum of the log probabilities (evaluated) of a (set of) sample(s)"""
        return np.sum([np.mean(lp) for lp in self.log_prob(simplify_result=False).values()])

    @flatten_result
    @util.tf_run_ignored
    def sample(self, size=1):
        """ Generates a sample for eache variable in the model """
        with (util.interceptor.enable_interceptor)(*self.enable_interceptor_variables):
            with contextmanager.observe(self.observed_variables, self.data):
                samples = [util.runtime.try_run(self.target_variables) for _ in range(size)]
        if size == 1:
            result = samples[0]
        else:
            result = {k:np.array([sample[k] for sample in samples]) for k in self.target_variables.keys()}
        return result

    @flatten_result
    @util.tf_run_ignored
    def parameters(self, names=None):
        """ Return the parameters of the Random Variables of the model.
        If `names` is None, then return all the parameters of all the Random Variables.
        If `names` is a list, then return the parameters specified in the list (if exists) for all the Random Variables.
        If `names` is a dict, then return all the parameters specified (value) for each Random Variable (key).

        Note:
            If `tf_run=True`, but any of the returned parameters is not a Tensor and therefore cannot be evaluated)
            this returns a not evaluated dict (because the evaluation will raise an Exception)

        Args:
            names: A list, a dict or None. Specify the parameters for the Random Variables to be obtained.

        Returns:
            A dict, where the keys are the names of the Random Variables and the values a dict of parameters (name-value)

        """
        if not (names is None or isinstance(names, (list, dict))):
            raise TypeError("The argument 'names' must be None, a list or a dict, not {}.".format(type(names)))

        def filter_parameters(varname, parameters):
            parameter_names = list(parameters.keys())
            if names is None:
                selected_parameters = parameter_names
            else:
                selected_parameters = set(names if isinstance(names, list) else names.get(varname, parameters))
            return {k:util.runtime.try_run(v) for k, v in parameters.items() if k in selected_parameters}

        with contextmanager.observe(self.observed_variables, self.data):
            result = {k:filter_parameters(k, v.parameters) for k, v in self.target_variables.items()}
        return result