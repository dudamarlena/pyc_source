# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/models/parameter.py
# Compiled at: 2019-04-01 11:32:16
# Size of source mod 2**32: 3553 bytes
import tensorflow as tf
import tensorflow.python.client as tf_session
from inferpy import contextmanager
from inferpy import exceptions

class Parameter:
    __doc__ = '\n    Random Variable parameter which can be optimized by an inference mechanism.\n    '

    def __init__(self, initial_value, name=None):
        self.name = name
        self.is_datamodel = False
        if contextmanager.randvar_registry.is_active():
            if self.name is None:
                raise exceptions.NotNamedParameter('Parameters defined inside a prob model must have a name.')
        elif contextmanager.randvar_registry.is_active():
            if contextmanager.data_model.is_active():
                self.is_datamodel = True
                if not isinstance(initial_value, (tf.Tensor, tf.SparseTensor, tf.Variable)):
                    initial_value = tf.convert_to_tensor(initial_value)
                input_varname = initial_value.op.name if contextmanager.randvar_registry.is_building_graph() else name
                contextmanager.randvar_registry.update_graph(input_varname)
                sample_shape = contextmanager.data_model.get_sample_shape(input_varname)
                if sample_shape is not ():
                    initial_value = tf.broadcast_to(initial_value, tf.TensorShape(sample_shape).concatenate(initial_value.shape))
        self.var = tf.Variable(initial_value, name=(self.name))
        if contextmanager.randvar_registry.is_active():
            contextmanager.randvar_registry.register_parameter(self)
            contextmanager.randvar_registry.update_graph(self.name)


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