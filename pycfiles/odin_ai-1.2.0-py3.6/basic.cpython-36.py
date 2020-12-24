# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/bay/distribution_layers/basic.py
# Compiled at: 2019-09-17 06:01:10
# Size of source mod 2**32: 26273 bytes
from __future__ import absolute_import, division, print_function
import numpy as np, tensorflow as tf, tensorflow_probability as tfp
from six import string_types
from tensorflow.python.keras.utils import tf_utils as keras_tf_utils
from tensorflow_probability.python import bijectors as tfb
from tensorflow_probability.python import distributions as tfd
from tensorflow_probability.python import layers as tfl
from tensorflow_probability.python.internal import distribution_util as dist_util
from tensorflow_probability.python.layers.distribution_layer import _event_size
from tensorflow_probability.python.layers.internal import distribution_tensor_coercible as dtc
from odin.bay.distributions import NegativeBinomialDisp, ZeroInflated
__all__ = [
 'DistributionLambda', 'MultivariateNormalLayer', 'BernoulliLayer',
 'DeterministicLayer', 'VectorDeterministicLayer', 'OneHotCategoricalLayer',
 'GammaLayer', 'DirichletLayer', 'GaussianLayer', 'NormalLayer',
 'LogNormalLayer', 'LogisticLayer', 'ZIBernoulliLayer',
 'update_convert_to_tensor_fn']
DistributionLambda = tfl.DistributionLambda
BernoulliLayer = tfl.IndependentBernoulli
LogisticLayer = tfl.IndependentLogistic

def update_convert_to_tensor_fn(dist, fn):
    if not isinstance(dist, dtc._TensorCoercible):
        raise AssertionError('dist must be output from tfd.DistributionLambda')
    else:
        assert callable(fn), 'fn must be callable'
        if isinstance(fn, property):
            fn = fn.fget
    dist._concrete_value = None
    dist._convert_to_tensor_fn = fn
    return dist


def _preprocess_eventshape(params, event_shape, n_dims=1):
    if isinstance(event_shape, string_types):
        if event_shape.lower().strip() == 'auto':
            event_shape = params.shape[-n_dims:]
        else:
            raise ValueError("Not support for event_shape='%s'" % event_shape)
    return event_shape


class DeterministicLayer(DistributionLambda):
    __doc__ = '\n  ```none\n  pmf(x; loc) = 1, if x == loc, else 0\n  cdf(x; loc) = 1, if x >= loc, else 0\n  ```\n  '

    def __init__(self, event_shape=(), convert_to_tensor_fn=tfd.Distribution.sample, activity_regularizer=None, validate_args=False, **kwargs):
        (super(DeterministicLayer, self).__init__)(
 lambda t: type(self).new(t, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'DeterministicLayer', [params]):
            params = tf.convert_to_tensor(value=params, name='params')
            return tfd.Deterministic(loc=params, validate_args=validate_args)

    @staticmethod
    def params_size(event_size, name=None):
        """ The number of `params` needed to create a single distribution. """
        return event_size


class VectorDeterministicLayer(DistributionLambda):
    __doc__ = '\n  ```none\n  pmf(x; loc)\n    = 1, if All[Abs(x - loc) <= atol + rtol * Abs(loc)],\n    = 0, otherwise.\n  ```\n  '

    def __init__(self, event_shape=(), convert_to_tensor_fn=tfd.Distribution.sample, activity_regularizer=None, validate_args=False, **kwargs):
        (super(VectorDeterministicLayer, self).__init__)(
 lambda t: type(self).new(t, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'VectorDeterministicLayer', [params]):
            params = tf.convert_to_tensor(value=params, name='params')
            return tfd.VectorDeterministic(loc=params, validate_args=validate_args)

    @staticmethod
    def params_size(event_size, name=None):
        """ The number of `params` needed to create a single distribution. """
        return event_size


class OneHotCategoricalLayer(DistributionLambda):
    __doc__ = " A `d`-variate OneHotCategorical Keras layer from `d` params.\n\n  Parameters\n  ----------\n  convert_to_tensor_fn: callable\n    that takes a `tfd.Distribution` instance and returns a\n    `tf.Tensor`-like object. For examples, see `class` docstring.\n    Default value: `tfd.Distribution.sample`.\n\n  sample_dtype: `dtype`\n    Type of samples produced by this distribution.\n    Default value: `None` (i.e., previous layer's `dtype`).\n\n  validate_args: `bool` (default `False`)\n    When `True` distribution parameters are checked for validity\n    despite possibly degrading runtime performance.\n    When `False` invalid inputs may silently render incorrect outputs.\n    Default value: `False`.\n\n  **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n\n  Note\n  ----\n  If input as probability values is given, it will be clipped by value\n  [1e-8, 1 - 1e-8]\n\n  "

    def __init__(self, event_shape=(), convert_to_tensor_fn=tfd.Distribution.sample, probs_input=False, sample_dtype=None, activity_regularizer=None, validate_args=False, **kwargs):
        (super(OneHotCategoricalLayer, self).__init__)(
 lambda t: type(self).new(t, probs_input, sample_dtype, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, probs_input=False, dtype=None, validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'OneHotCategoricalLayer', [params]):
            params = tf.convert_to_tensor(value=params, name='params')
            return tfd.OneHotCategorical(logits=(params if not probs_input else None),
              probs=(tf.clip_by_value(params, 1e-08, 0.99999999) if probs_input else None),
              dtype=(dtype or params.dtype.base_dtype),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_size, name=None):
        """The number of `params` needed to create a single distribution."""
        return event_size


class DirichletLayer(DistributionLambda):
    __doc__ = '\n  Parameters\n  ----------\n  pre_softplus : bool (default: False)\n    applying softplus activation on the parameters before parameterizing\n\n  clip_for_stable : bool (default: True)\n    clipping the concentration into range [1e-3, 1e3] for stability\n\n  '

    def __init__(self, event_shape='auto', pre_softplus=False, clip_for_stable=True, convert_to_tensor_fn=tfd.Distribution.sample, activity_regularizer=None, validate_args=False, **kwargs):
        (super(DirichletLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, pre_softplus, clip_for_stable, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape='auto', pre_softplus=False, clip_for_stable=True, validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        event_shape = _preprocess_eventshape(params, event_shape)
        with tf.compat.v1.name_scope(name, 'DirichletLayer', [params, event_shape]):
            params = tf.convert_to_tensor(value=params, name='params')
            event_shape = dist_util.expand_to_vector(tf.convert_to_tensor(value=event_shape,
              name='event_shape',
              dtype=(tf.int32)),
              tensor_name='event_shape')
            output_shape = tf.concat([
             tf.shape(input=params)[:-1],
             event_shape],
              axis=0)
            if pre_softplus:
                params = tf.nn.softplus(params)
            if clip_for_stable:
                params = tf.clip_by_value(params, 0.001, 1000.0)
            return tfd.Independent(tfd.Dirichlet(concentration=(tf.reshape(params, output_shape)), validate_args=validate_args),
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'Dirichlet_params_size', [event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return _event_size(event_shape, name=(name or 'Dirichlet_params_size'))


class GaussianLayer(DistributionLambda):
    __doc__ = 'An independent normal Keras layer.\n\n  Parameters\n  ----------\n  event_shape: integer vector `Tensor` representing the shape of single\n    draw from this distribution.\n\n  softplus_scale : bool\n    if True, `scale = softplus(params) + softplus_inverse(1.0)`\n\n  convert_to_tensor_fn: Python `callable` that takes a `tfd.Distribution`\n    instance and returns a `tf.Tensor`-like object.\n    Default value: `tfd.Distribution.sample`.\n\n  validate_args: Python `bool`, default `False`. When `True` distribution\n    parameters are checked for validity despite possibly degrading runtime\n    performance. When `False` invalid inputs may silently render incorrect\n    outputs.\n    Default value: `False`.\n\n  **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n\n  '

    def __init__(self, event_shape=(), softplus_scale=True, convert_to_tensor_fn=tfd.Distribution.sample, activity_regularizer=None, validate_args=False, **kwargs):
        (super(GaussianLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, softplus_scale, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape=(), softplus_scale=True, validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'NormalLayer', [params, event_shape]):
            params = tf.convert_to_tensor(value=params, name='params')
            event_shape = dist_util.expand_to_vector(tf.convert_to_tensor(value=event_shape,
              name='event_shape',
              dtype=(tf.int32)),
              tensor_name='event_shape')
            output_shape = tf.concat([
             tf.shape(input=params)[:-1],
             event_shape],
              axis=0)
            loc_params, scale_params = tf.split(params, 2, axis=(-1))
            if softplus_scale:
                scale_params = tf.math.softplus(scale_params) + tfp.math.softplus_inverse(1.0)
            return tfd.Independent(tfd.Normal(loc=(tf.reshape(loc_params, output_shape)), scale=(tf.reshape(scale_params, output_shape)),
              validate_args=validate_args),
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'Normal_params_size', [event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return 2 * _event_size(event_shape, name=(name or 'Normal_params_size'))


class LogNormalLayer(DistributionLambda):
    __doc__ = 'An independent LogNormal Keras layer.\n\n  Parameters\n  ----------\n  event_shape: integer vector `Tensor` representing the shape of single\n    draw from this distribution.\n\n  softplus_scale : bool\n    if True, `scale = softplus(params) + softplus_inverse(1.0)`\n\n  convert_to_tensor_fn: Python `callable` that takes a `tfd.Distribution`\n    instance and returns a `tf.Tensor`-like object.\n    Default value: `tfd.Distribution.sample`.\n\n  validate_args: Python `bool`, default `False`. When `True` distribution\n    parameters are checked for validity despite possibly degrading runtime\n    performance. When `False` invalid inputs may silently render incorrect\n    outputs.\n    Default value: `False`.\n\n  **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n\n  '

    def __init__(self, event_shape=(), softplus_scale=True, convert_to_tensor_fn=tfd.Distribution.sample, validate_args=False, activity_regularizer=None, **kwargs):
        (super(LogNormalLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, softplus_scale, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape=(), softplus_scale=True, validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'LogNormalLayer', [params, event_shape]):
            params = tf.convert_to_tensor(value=params, name='params')
            event_shape = dist_util.expand_to_vector(tf.convert_to_tensor(value=event_shape,
              name='event_shape',
              dtype=(tf.int32)),
              tensor_name='event_shape')
            output_shape = tf.concat([
             tf.shape(input=params)[:-1],
             event_shape],
              axis=0)
            loc_params, scale_params = tf.split(params, 2, axis=(-1))
            if softplus_scale:
                scale_params = tf.math.softplus(scale_params) + tfp.math.softplus_inverse(1.0)
            return tfd.Independent(tfd.LogNormal(loc=(tf.reshape(loc_params, output_shape)), scale=(tf.reshape(scale_params, output_shape)),
              validate_args=validate_args),
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'LogNormal_params_size', [event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return 2 * _event_size(event_shape, name=(name or 'LogNormal_params_size'))


class GammaLayer(DistributionLambda):
    __doc__ = 'An independent Gamma Keras layer.\n\n  Parameters\n  ----------\n  event_shape: integer vector `Tensor` representing the shape of single\n    draw from this distribution.\n\n  convert_to_tensor_fn: Python `callable` that takes a `tfd.Distribution`\n    instance and returns a `tf.Tensor`-like object.\n    Default value: `tfd.Distribution.sample`.\n\n  validate_args: Python `bool`, default `False`. When `True` distribution\n    parameters are checked for validity despite possibly degrading runtime\n    performance. When `False` invalid inputs may silently render incorrect\n    outputs.\n    Default value: `False`.\n\n  **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n\n  '

    def __init__(self, event_shape=(), convert_to_tensor_fn=tfd.Distribution.sample, validate_args=False, activity_regularizer=None, **kwargs):
        (super(GammaLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape=(), validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'GammaLayer', [params, event_shape]):
            params = tf.convert_to_tensor(value=params, name='params')
            event_shape = dist_util.expand_to_vector(tf.convert_to_tensor(value=event_shape,
              name='event_shape',
              dtype=(tf.int32)),
              tensor_name='event_shape')
            output_shape = tf.concat([
             tf.shape(input=params)[:-1],
             event_shape],
              axis=0)
            concentration_params, rate_params = tf.split(params, 2, axis=(-1))
            return tfd.Independent(tfd.Gamma(concentration=(tf.reshape(concentration_params, output_shape)),
              rate=(tf.reshape(rate_params, output_shape)),
              validate_args=validate_args),
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'Gamma_params_size', [event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return 2 * _event_size(event_shape, name=(name or 'Gamma_params_size'))


class MultivariateNormalLayer(DistributionLambda):
    __doc__ = "A `d`-variate Multivariate Normal distribution Keras layer:\n\n  Different covariance mode:\n   - tril (lower triangle): `d + d * (d + 1) // 2` params.\n   - diag (diagonal) : `d + d` params.\n   - full (full) : `d + d * d` params.\n\n  Typical choices for `convert_to_tensor_fn` include:\n\n  - `tfd.Distribution.sample`\n  - `tfd.Distribution.mean`\n  - `tfd.Distribution.mode`\n  - `lambda s: s.mean() + 0.1 * s.stddev()`\n\n    Parameters\n    ----------\n    event_size: Scalar `int` representing the size of single draw from this\n      distribution.\n\n    covariance_type : {'diag', 'tril', 'full'}\n\n    softplus_scale : bool\n      if True, `scale = softplus(params) + softplus_inverse(1.0)`\n\n    convert_to_tensor_fn: Python `callable` that takes a `tfd.Distribution`\n      instance and returns a `tf.Tensor`-like object. For examples, see\n      `class` docstring.\n      Default value: `tfd.Distribution.sample`.\n\n    validate_args: Python `bool`, default `False`. When `True` distribution\n      parameters are checked for validity despite possibly degrading runtime\n      performance. When `False` invalid inputs may silently render incorrect\n      outputs.\n      Default value: `False`.\n\n    **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n  "

    def __init__(self, event_size, covariance_type='diag', softplus_scale=True, convert_to_tensor_fn=tfd.Distribution.sample, validate_args=False, activity_regularizer=None, **kwargs):
        (super(MultivariateNormalLayer, self).__init__)(
 lambda t: type(self).new(t, event_size, covariance_type, softplus_scale, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_size, covariance_type, softplus_scale, validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        covariance_type = str(covariance_type).lower().strip()
        if not covariance_type in ('full', 'tril', 'diag'):
            raise AssertionError("No support for given covariance_type: '%s'" % covariance_type)
        else:
            if bool(softplus_scale):
                scale_fn = lambda x: tf.math.softplus(x) + tfp.math.softplus_inverse(1.0)
            else:
                scale_fn = lambda x: x
        with tf.compat.v1.name_scope(name, 'MultivariateNormalLayer', [
         params, event_size]):
            params = tf.convert_to_tensor(value=params, name='params')
            if covariance_type == 'tril':
                scale_tril = tfb.ScaleTriL(diag_shift=(np.array(1e-05, params.dtype.as_numpy_dtype())),
                  validate_args=validate_args)
                return tfd.MultivariateNormalTriL(loc=(params[..., :event_size]),
                  scale_tril=(scale_tril(scale_fn(params[..., event_size:]))),
                  validate_args=validate_args)
            if covariance_type == 'diag':
                return tfd.MultivariateNormalDiag(loc=(params[..., :event_size]), scale_diag=(scale_fn(params[..., event_size:])),
                  validate_args=validate_args)
            if covariance_type == 'full':
                return tfd.MultivariateNormalFullCovariance(loc=(params[..., :event_size]),
                  covariance_matrix=(tf.reshape(scale_fn(params[..., event_size:]), (
                 event_size, event_size))),
                  validate_args=validate_args)

    @staticmethod
    def params_size(event_size, covariance_type='diag', name=None):
        """The number of `params` needed to create a single distribution."""
        covariance_type = str(covariance_type).lower().strip()
        assert covariance_type in ('full', 'tril', 'diag'), "No support for given covariance_type: '%s'" % covariance_type
        with tf.compat.v1.name_scope(name, 'MultivariateNormal_params_size', [
         event_size]):
            if covariance_type == 'tril':
                return event_size + event_size * (event_size + 1) // 2
            else:
                if covariance_type == 'diag':
                    return event_size + event_size
                if covariance_type == 'full':
                    return event_size + event_size * event_size


class ZIBernoulliLayer(DistributionLambda):
    __doc__ = 'A Independent zero-inflated bernoulli keras layer\n\n  Parameters\n  ----------\n  event_shape: integer vector `Tensor` representing the shape of single\n    draw from this distribution.\n\n  given_log_count : boolean\n    is the input representing log count values or the count itself\n\n  convert_to_tensor_fn: Python `callable` that takes a `tfd.Distribution`\n    instance and returns a `tf.Tensor`-like object.\n    Default value: `tfd.Distribution.sample`.\n\n  validate_args: Python `bool`, default `False`. When `True` distribution\n    parameters are checked for validity despite possibly degrading runtime\n    performance. When `False` invalid inputs may silently render incorrect\n    outputs.\n    Default value: `False`.\n\n  **kwargs: Additional keyword arguments passed to `tf.keras.Layer`.\n\n  '

    def __init__(self, event_shape=(), given_logits=True, convert_to_tensor_fn=tfd.Distribution.sample, validate_args=False, activity_regularizer=None, **kwargs):
        (super(ZIBernoulliLayer, self).__init__)(
 lambda t: type(self).new(t, event_shape, given_logits, validate_args),
 convert_to_tensor_fn, activity_regularizer=activity_regularizer, **kwargs)

    @staticmethod
    def new(params, event_shape=(), given_logits=True, validate_args=False, name=None):
        """Create the distribution instance from a `params` vector."""
        with tf.compat.v1.name_scope(name, 'ZIBernoulliLayer', [
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
            bernoulli_params, rate_params = tf.split(params, 2, axis=(-1))
            bernoulli_params = tf.reshape(bernoulli_params, output_shape)
            bern = tfd.Bernoulli(logits=(bernoulli_params if given_logits else None), probs=(bernoulli_params if not given_logits else None),
              validate_args=validate_args)
            zibern = ZeroInflated(count_distribution=bern, logits=(tf.reshape(rate_params, output_shape)),
              validate_args=validate_args)
            return tfd.Independent(zibern,
              reinterpreted_batch_ndims=tf.size(input=event_shape),
              validate_args=validate_args)

    @staticmethod
    def params_size(event_shape=(), name=None):
        """The number of `params` needed to create a single distribution."""
        with tf.compat.v1.name_scope(name, 'ZeroInflatedBernoulli_params_size', [
         event_shape]):
            event_shape = tf.convert_to_tensor(value=event_shape, name='event_shape',
              dtype=(tf.int32))
            return 2 * _event_size(event_shape, name=(name or 'ZeroInflatedBernoulli_params_size'))


NormalLayer = GaussianLayer