# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/models/parameter.py
# Compiled at: 2019-09-03 11:37:11
# Size of source mod 2**32: 3335 bytes
import tensorflow as tf
from tensorflow.python.client import session as tf_session
from . import sanitize_input_arg
from inferpy import contextmanager
from inferpy import util

class Parameter:
    __doc__ = '\n    Random Variable parameter which can be optimized by an inference mechanism.\n    '

    def __init__(self, initial_value, name=None):
        self.is_datamodel = False
        self.name = name if name else util.name.generate('parameter')
        sanitized_initial_value = tf.convert_to_tensor(sanitize_input_arg(initial_value))
        if contextmanager.data_model.is_active():
            self.is_datamodel = True
            input_varname = sanitized_initial_value.op.name if contextmanager.randvar_registry.is_building_graph() else name
            contextmanager.randvar_registry.update_graph(input_varname)
            sample_shape = contextmanager.data_model.get_sample_shape(input_varname)
            if sample_shape is not ():
                sanitized_initial_value = tf.broadcast_to(sanitized_initial_value, tf.TensorShape(sample_shape).concatenate(sanitized_initial_value.shape))
        self.var = tf.Variable(sanitized_initial_value, name=(self.name))
        util.session.get_session().run(tf.variables_initializer([self.var]))
        contextmanager.randvar_registry.register_parameter(self)
        contextmanager.randvar_registry.update_graph()


def _tensor_conversion_function(p, dtype=None, name=None, as_ref=False):
    """
        Function that converts the inferpy variable into a Tensor.
        This will enable the use of enable tf.convert_to_tensor(rv)

        If the variable needs to be broadcast_to, do it right now
    """
    return tf.convert_to_tensor(p.var)


tf.register_tensor_conversion_function(Parameter, _tensor_conversion_function)

def _session_run_conversion_fetch_function(p):
    """
        This will enable run and operations with other tensors
    """
    return (
     [
      tf.convert_to_tensor(p)], lambda val: val[0])


tf_session.register_session_run_conversion_functions(Parameter, _session_run_conversion_fetch_function)