# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/util/interceptor.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 6144 bytes
import tensorflow as tf
from tensorflow_probability import edward2 as ed
from contextlib import contextmanager
from inferpy import util
from inferpy.contextmanager import data_model
CURRENT_ENABLE_INTERCEPTOR = None
ALLOW_CONDITIONS = True

@contextmanager
def disallow_conditions():
    global ALLOW_CONDITIONS
    ALLOW_CONDITIONS = False
    try:
        yield
    finally:
        ALLOW_CONDITIONS = True


@contextmanager
def enable_interceptor(enable_globals, enable_locals):
    global CURRENT_ENABLE_INTERCEPTOR
    sess = util.session.get_session()
    try:
        if enable_globals:
            enable_globals.load(True, session=sess)
        if enable_locals:
            enable_locals.load(True, session=sess)
        CURRENT_ENABLE_INTERCEPTOR = (enable_globals, enable_locals)
        yield
    finally:
        if enable_globals:
            enable_globals.load(False, session=sess)
        if enable_locals:
            enable_locals.load(False, session=sess)
        CURRENT_ENABLE_INTERCEPTOR = None


def set_values(**model_kwargs):
    """Creates a value-setting interceptor. Usable as a parameter of the ed2.interceptor.

        :model_kwargs: The name of each argument must be the name of a random variable to intercept,
            and the value is the element which intercepts the value of the random variable.

        :returns: The random variable with the intercepted value
    """

    def interceptor(f, *args, **kwargs):
        name = kwargs.get('name')
        if name in model_kwargs:
            interception_value = model_kwargs[name]
            if ALLOW_CONDITIONS:
                if CURRENT_ENABLE_INTERCEPTOR is not None:
                    enable_globals, enable_locals = CURRENT_ENABLE_INTERCEPTOR
                    if enable_globals is None:
                        enable_globals = tf.constant(False)
                    if enable_locals is None:
                        enable_locals = tf.constant(False)
                    _value = (ed.interceptable(f))(*args, **kwargs).value
                    is_local_hidden = data_model.is_active()
                    conditional_value = tf.cond(tf.logical_or(tf.logical_and(enable_globals, tf.constant(not is_local_hidden)), tf.logical_and(enable_locals, tf.constant(is_local_hidden))), lambda : interception_value, lambda : _value)
                    kwargs['value'] = tf.broadcast_to(conditional_value, _value.shape)
            else:
                kwargs['value'] = interception_value
        return (ed.interceptable(f))(*args, **kwargs)

    return interceptor


def set_values_condition(var_condition, var_value):
    """Creates a value-setting interceptor. Usable as a parameter of the ed2.interceptor.

        :var_condition (`tf.Variable`): The boolean tf.Variable, used to intercept the value property with
            `value_var` or the variable value property itself
        :var_value (`tf.Variable`): The tf.Variable used to intercept the value property when `var_condition` is True

        :returns: The random variable with the intercepted value
    """

    def interceptor(f, *args, **kwargs):
        if ALLOW_CONDITIONS:
            _value = (ed.interceptable(f))(*args, **kwargs).value
            conditional_value = tf.cond(var_condition, lambda : var_value, lambda : _value)
            return (ed.interceptable(f))(args, value=tf.broadcast_to(conditional_value, _value.shape), **kwargs)
        else:
            return (ed.interceptable(f))(*args, **kwargs)

    return interceptor


def make_predictable_variables(initial_value, rv_name):
    if ALLOW_CONDITIONS:
        is_observed = tf.Variable(False, trainable=False, name='inferpy-predict-enabled-{name}'.format(name=(rv_name or 'default')))
        observed_value = tf.Variable(initial_value, trainable=False, name='inferpy-predict-{name}'.format(name=(rv_name or 'default')))
        util.session.get_session().run(tf.variables_initializer([is_observed, observed_value]))
        return (
         is_observed, observed_value)
    else:
        return (None, None)