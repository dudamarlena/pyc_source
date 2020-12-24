# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/bay/distribution_layers/count_layers.py
# Compiled at: 2019-08-29 09:03:52
# Size of source mod 2**32: 21219 bytes
from __future__ import absolute_import, division, print_function
import tensorflow as tf
from tensorflow_probability.python import distributions as tfd
from tensorflow_probability.python import layers as tfl
from tensorflow_probability.python.internal import distribution_util as dist_util
from tensorflow_probability.python.layers import DistributionLambda
from tensorflow_probability.python.layers.distribution_layer import _event_size
from odin.bay.distributions import NegativeBinomialDisp, ZeroInflated
__all__ = [
 'PoissonLayer', 'NegativeBinomialDispLayer', 'NegativeBinomialLayer',
 'ZINegativeBinomialDispLayer', 'ZINegativeBinomialLayer', 'ZIPoissonLayer']
PoissonLayer = tfl.IndependentPoisson

class NegativeBinomialLayer(DistributionLambda):
    __doc__ = "An independent NegativeBinomial Keras layer.\n\n  Parameters\n  ----------\n  event_shape: integer vector `Tensor` representing the shape of single\n    draw from this distribution.\n  given_log_count : boolean\n    is the input representing log count values or the count itself\n  dispersion : {'full', 'share', 'single'}\n    'full' creates a dispersion value for each individual data point,\n    'share' creates a single vector of dispersion for all examples, and\n    'single' uses a single value as dispersion for all data points.\n    Note: the dispersion in this case is the probability of success.\n  convert_to_tensor_fn: Python `callable` that takes a `tfd.Distribution`\n    instance and returns a `tf.Tensor`-like object.\n    Default value: `tfd.Distribution.sample`.\n  validate_args: Python `bool`, default `False`. When `True` distribution\n    parameters are checked for validity despite possibly degrading runtime\n    performance. When `False` invalid inputs may silently render incorrect\n    outputs.\n    Default value: `False`.\n\n  **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n\n  "

    def __init__(self, event_shape=(), given_log_count=True, dispersion='full', convert_to_tensor_fn=tfd.Distribution.sample, validate_args=False, activity_regularizer=None, **kwargs):
        dispersion = str(dispersion).lower()
        assert dispersion in ('full', 'single', 'share'), "Only support three different dispersion value: 'full', 'single' and " + "'share', but given: %s" % dispersion
        (super(NegativeBinomialLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, given_log_count, dispersion, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape=(), given_log_count=True, dispersion='full', validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'NegativeBinomialLayer', [
         params, event_shape]):
            params = tf.convert_to_tensor(value=params, name='params')
            event_shape = dist_util.expand_to_vector(tf.convert_to_tensor(value=event_shape,
              name='event_shape',
              dtype=(tf.int32)),
              tensor_name='event_shape')
            output_shape = tf.concat([
             tf.shape(input=params)[:-1],
             event_shape],
              axis=0)
            ndims = output_shape.shape[0]
            total_count_params, logits_params = tf.split(params, 2, axis=(-1))
            if dispersion == 'single':
                logits_params = tf.reduce_mean(logits_params)
            else:
                if dispersion == 'share':
                    logits_params = tf.reduce_mean(logits_params, axis=tf.range(0, (ndims - 1),
                      dtype='int32'),
                      keepdims=True)
            if given_log_count:
                total_count_params = tf.exp(total_count_params, name='total_count')
            return tfd.Independent(tfd.NegativeBinomial(total_count=(tf.reshape(total_count_params, output_shape)),
              logits=(tf.reshape(logits_params, output_shape) if dispersion == 'full' else logits_params),
              validate_args=validate_args),
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'NegativeBinomial_params_size', [
         event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return 2 * _event_size(event_shape, name=(name or 'NegativeBinomial_params_size'))


class NegativeBinomialDispLayer(DistributionLambda):
    __doc__ = "An alternative parameterization of the NegativeBinomial Keras layer.\n\n  Parameters\n  ----------\n  event_shape: integer vector `Tensor` representing the shape of single\n    draw from this distribution.\n  given_log_mean : `bool`\n    is the input representing log mean values or the count mean itself\n  given_log_mean : `bool`\n    is the input representing log mean values or the count mean itself\n  dispersion : {'full', 'share', 'single'}\n    'full' creates a dispersion value for each individual data point,\n    'share' creates a single vector of dispersion for all examples, and\n    'single' uses a single value as dispersion for all data points.\n  convert_to_tensor_fn: Python `callable` that takes a `tfd.Distribution`\n    instance and returns a `tf.Tensor`-like object.\n    Default value: `tfd.Distribution.sample`.\n  validate_args: Python `bool`, default `False`. When `True` distribution\n    parameters are checked for validity despite possibly degrading runtime\n    performance. When `False` invalid inputs may silently render incorrect\n    outputs.\n    Default value: `False`.\n\n  **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n\n  "

    def __init__(self, event_shape=(), given_log_mean=True, given_log_disp=True, dispersion='full', convert_to_tensor_fn=tfd.Distribution.sample, validate_args=False, activity_regularizer=None, **kwargs):
        dispersion = str(dispersion).lower()
        assert dispersion in ('full', 'single', 'share'), "Only support three different dispersion value: 'full', 'single' and " + "'share', but given: %s" % dispersion
        (super(NegativeBinomialDispLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, given_log_mean, given_log_disp, dispersion, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape=(), given_log_mean=True, given_log_disp=True, dispersion='full', validate_args=False, name=None):
        """ Create the distribution instance from a `params` vector. """
        with tf.compat.v1.name_scope(name, 'NegativeBinomialDispLayer', [
         params, event_shape]):
            params = tf.convert_to_tensor(value=params, name='params')
            event_shape = dist_util.expand_to_vector(tf.convert_to_tensor(value=event_shape,
              name='event_shape',
              dtype=(tf.int32)),
              tensor_name='event_shape')
            output_shape = tf.concat([
             tf.shape(input=params)[:-1],
             event_shape],
              axis=0)
            loc_params, disp_params = tf.split(params, 2, axis=(-1))
            if dispersion == 'single':
                disp_params = tf.reduce_mean(disp_params)
            else:
                if dispersion == 'share':
                    disp_params = tf.reduce_mean(disp_params, axis=tf.range(0, (output_shape.shape[0] - 1),
                      dtype='int32'),
                      keepdims=True)
            if given_log_mean:
                loc_params = tf.exp(loc_params, name='loc')
            if given_log_disp:
                disp_params = tf.exp(disp_params, name='disp')
            return tfd.Independent(NegativeBinomialDisp(loc=(tf.reshape(loc_params, output_shape)), disp=(tf.reshape(disp_params, output_shape) if dispersion == 'full' else disp_params),
              validate_args=validate_args),
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'NegativeBinomialDisp_params_size', [
         event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return 2 * _event_size(event_shape, name=(name or 'NegativeBinomialDisp_params_size'))


class ZIPoissonLayer(DistributionLambda):
    __doc__ = 'A Independent zero-inflated Poisson keras layer\n  '

    def __init__(self, event_shape=(), convert_to_tensor_fn=tfd.Distribution.sample, validate_args=False, activity_regularizer=None, **kwargs):
        (super(ZIPoissonLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape=(), validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'ZIPoissonLayer', [params, event_shape]):
            params = tf.convert_to_tensor(value=params, name='params')
            event_shape = dist_util.expand_to_vector(tf.convert_to_tensor(value=event_shape,
              name='event_shape',
              dtype=(tf.int32)),
              tensor_name='event_shape')
            output_shape = tf.concat([
             tf.shape(input=params)[:-1],
             event_shape],
              axis=0)
            log_rate_params, logits_params = tf.split(params, 2, axis=(-1))
            zip = ZeroInflated(count_distribution=tfd.Poisson(log_rate=(tf.reshape(log_rate_params, output_shape)),
              validate_args=validate_args),
              logits=(tf.reshape(logits_params, output_shape)),
              validate_args=validate_args)
            return tfd.Independent(zip,
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'ZeroInflatedNegativeBinomial_params_size', [
         event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return 2 * _event_size(event_shape,
              name=(name or 'ZeroInflatedNegativeBinomial_params_size'))


class ZINegativeBinomialLayer(DistributionLambda):
    __doc__ = "A Independent zero-inflated negative binomial keras layer\n\n  Parameters\n  ----------\n  event_shape: integer vector `Tensor` representing the shape of single\n    draw from this distribution.\n  given_log_count : boolean\n    is the input representing log count values or the count itself\n  dispersion : {'full', 'share', 'single'}\n    'full' creates a dispersion value for each individual data point,\n    'share' creates a single vector of dispersion for all examples, and\n    'single' uses a single value as dispersion for all data points.\n  convert_to_tensor_fn: Python `callable` that takes a `tfd.Distribution`\n    instance and returns a `tf.Tensor`-like object.\n    Default value: `tfd.Distribution.sample`.\n  validate_args: Python `bool`, default `False`. When `True` distribution\n    parameters are checked for validity despite possibly degrading runtime\n    performance. When `False` invalid inputs may silently render incorrect\n    outputs.\n    Default value: `False`.\n\n  **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n\n  "

    def __init__(self, event_shape=(), given_log_count=True, dispersion='full', convert_to_tensor_fn=tfd.Distribution.sample, validate_args=False, activity_regularizer=None, **kwargs):
        (super(ZINegativeBinomialLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, given_log_count, dispersion, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape=(), given_log_count=True, dispersion='full', validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'ZINegativeBinomialLayer', [
         params, event_shape]):
            params = tf.convert_to_tensor(value=params, name='params')
            event_shape = dist_util.expand_to_vector(tf.convert_to_tensor(value=event_shape,
              name='event_shape',
              dtype=(tf.int32)),
              tensor_name='event_shape')
            output_shape = tf.concat([
             tf.shape(input=params)[:-1],
             event_shape],
              axis=0)
            ndims = output_shape.shape[0]
            total_count_params, logits_params, rate_params = tf.split(params, 3,
              axis=(-1))
            if dispersion == 'single':
                logits_params = tf.reduce_mean(logits_params)
            else:
                if dispersion == 'share':
                    logits_params = tf.reduce_mean(logits_params, axis=tf.range(0, (ndims - 1),
                      dtype='int32'),
                      keepdims=True)
            if given_log_count:
                total_count_params = tf.exp(total_count_params, name='total_count')
            nb = tfd.NegativeBinomial(total_count=(tf.reshape(total_count_params, output_shape)),
              logits=(tf.reshape(logits_params, output_shape) if dispersion == 'full' else logits_params),
              validate_args=validate_args)
            zinb = ZeroInflated(count_distribution=nb, logits=(tf.reshape(rate_params, output_shape)),
              validate_args=validate_args)
            return tfd.Independent(zinb,
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'ZeroInflatedNegativeBinomial_params_size', [
         event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return 3 * _event_size(event_shape,
              name=(name or 'ZeroInflatedNegativeBinomial_params_size'))


class ZINegativeBinomialDispLayer(DistributionLambda):
    __doc__ = "A Independent zero-inflated negative binomial (alternative\n  parameterization) keras layer\n\n  Parameters\n  ----------\n  event_shape: integer vector `Tensor` representing the shape of single\n    draw from this distribution.\n  given_log_mean : boolean\n    is the input representing log count values or the count itself\n  given_log_disp : boolean\n    is the input representing log dispersion values\n  dispersion : {'full', 'share', 'single'}\n    'full' creates a dispersion value for each individual data point,\n    'share' creates a single vector of dispersion for all examples, and\n    'single' uses a single value as dispersion for all data points.\n  convert_to_tensor_fn: Python `callable` that takes a `tfd.Distribution`\n    instance and returns a `tf.Tensor`-like object.\n    Default value: `tfd.Distribution.sample`.\n  validate_args: Python `bool`, default `False`. When `True` distribution\n    parameters are checked for validity despite possibly degrading runtime\n    performance. When `False` invalid inputs may silently render incorrect\n    outputs.\n    Default value: `False`.\n\n  **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n\n  "

    def __init__(self, event_shape=(), given_log_mean=True, given_log_disp=True, dispersion='full', convert_to_tensor_fn=tfd.Distribution.sample, validate_args=False, activity_regularizer=None, **kwargs):
        (super(ZINegativeBinomialDispLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, given_log_mean, given_log_disp, dispersion, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape=(), given_log_mean=True, given_log_disp=True, dispersion='full', validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'ZINegativeBinomialDispLayer', [
         params, event_shape]):
            params = tf.convert_to_tensor(value=params, name='params')
            event_shape = dist_util.expand_to_vector(tf.convert_to_tensor(value=event_shape,
              name='event_shape',
              dtype=(tf.int32)),
              tensor_name='event_shape')
            output_shape = tf.concat([
             tf.shape(input=params)[:-1],
             event_shape],
              axis=0)
            loc_params, disp_params, rate_params = tf.split(params, 3, axis=(-1))
            if dispersion == 'single':
                disp_params = tf.reduce_mean(disp_params)
            else:
                if dispersion == 'share':
                    disp_params = tf.reduce_mean(disp_params, axis=tf.range(0, (output_shape.shape[0] - 1),
                      dtype='int32'),
                      keepdims=True)
            if given_log_mean:
                loc_params = tf.exp(loc_params, name='loc')
            if given_log_disp:
                disp_params = tf.exp(disp_params, name='disp')
            nb = NegativeBinomialDisp(loc=(tf.reshape(loc_params, output_shape)), disp=(tf.reshape(disp_params, output_shape) if dispersion == 'full' else disp_params),
              validate_args=validate_args)
            zinb = ZeroInflated(count_distribution=nb, logits=(tf.reshape(rate_params, output_shape)),
              validate_args=validate_args)
            return tfd.Independent(zinb,
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'ZINegativeBinomialDisp_params_size', [
         event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return 3 * _event_size(event_shape, name=(name or 'ZINegativeBinomialDisp_params_size'))