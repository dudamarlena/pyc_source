# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/bay/distributions/utils.py
# Compiled at: 2019-09-18 09:29:42
# Size of source mod 2**32: 6375 bytes
from __future__ import absolute_import, division, print_function
import inspect
from typing import List, Optional, Text
import numpy as np, tensorflow as tf
from six import string_types
from tensorflow_probability.python import distributions as tfd
from tensorflow_probability.python.distributions import kullback_leibler
from tensorflow_probability.python.internal import assert_util, prefer_static, tensorshape_util
from tensorflow_probability.python.layers.internal import distribution_tensor_coercible
from odin.bay import distributions as obd
from odin.bay.distributions.negative_binomial_disp import NegativeBinomialDisp
from odin.bay.distributions.zero_inflated import ZeroInflated
__all__ = [
 'concat_distribution']
dist_params = {obd.Independent: ['distribution', 'reinterpreted_batch_ndims'], 
 ZeroInflated: ['count_distribution', 'inflated_distribution'], 
 obd.MixtureSameFamily: ['mixture_distribution', 'components_distribution'], 
 obd.Gamma: ['concentration', 'rate'], 
 obd.Normal: ['loc', 'scale'], 
 obd.LogNormal: ['loc', 'scale'], 
 obd.MultivariateNormalDiag: ['loc', 'scale'], 
 obd.MultivariateNormalTriL: ['loc', 'scale'], 
 obd.MultivariateNormalFullCovariance: ['loc', 'scale'], 
 NegativeBinomialDisp: ['loc', 'disp'], 
 obd.NegativeBinomial: ['total_count', 'logits_parameter'], 
 obd.Poisson: ['log_rate_parameter'], 
 obd.Gumbel: ['loc', 'scale'], 
 obd.Bernoulli: ['logits_parameter'], 
 obd.Dirichlet: ['concentration'], 
 obd.Beta: ['concentration1', 'concentration0'], 
 obd.OneHotCategorical: ['logits_parameter'], 
 obd.Categorical: ['logits_parameter'], 
 obd.Laplace: ['loc', 'scale'], 
 obd.Wishart: ['df', 'scale'], 
 obd.Uniform: ['low', 'high'], 
 obd.Multinomial: ['total_count', 'logits_parameter'], 
 obd.Deterministic: ['loc', 'atol', 'rtol'], 
 obd.VectorDeterministic: ['loc', 'atol', 'rtol']}
for dist_type, attr_names in dist_params.items():
    if not (isinstance(attr_names, (tuple, list)) and all(isinstance(name, string_types) for name in attr_names)):
        raise AssertionError('Error defining parameters of distributions')
    elif not (isinstance(dist_type, type) and issubclass(dist_type, obd.Distribution)):
        raise AssertionError('Error defining parameters of distributions')
    assert all(hasattr(dist_type, name) for name in attr_names), 'Error defining parameters of distributions'

def _find_axis_for_stack(dists, given_axis):
    if given_axis is not None:
        return int(given_axis)
    event_shape = dists[0].event_shape
    batch_shape = dists[0].batch_shape
    assertions = []
    for d in dists[1:]:
        assertions.append(tf.assert_equal(event_shape, d.event_shape))
        assertions.append(tf.assert_equal(batch_shape.ndims, d.batch_shape.ndims))

    with tf.control_dependencies(assertions):
        axis = []
        for d in dists:
            shape = d.batch_shape
            for ax, (i, j) in enumerate(zip(batch_shape, shape)):
                if i != j:
                    axis.append(ax)

        if len(axis) == 0:
            return 0
        else:
            assert len(set(axis)) == 1, 'Multiple dimensions are found to be different among the distributions, expect only 1 different dimension.'
            return axis[0]


def concat_distribution(dists: List[tfd.Distribution], axis: Optional[int]=None, validate_args: bool=False, allow_nan_stats: bool=True, name: Optional[Text]=None) -> tfd.Distribution:
    """ This layer create a new `Distribution` by concatenate parameters of
  multiple distributions of the same type along given `axis`

  Note
  ----
  If your distribution is the output from
  `tensorflow_probability.DistributionLambda`, this function will remove all
  the keras tracking ultilities, for better solution checkout
  `odin.networks.distribution_util_layer.ConcatDistribution`
  """
    if not isinstance(dists, (tuple, list)):
        dists = [
         dists]
    else:
        if len(dists) == 1:
            return dists[0]
        else:
            if len(dists) == 0:
                raise ValueError('No distributions were given')
            axis = _find_axis_for_stack(dists, given_axis=axis)
            t = type(dists[0])
            is_keras_output = False
            if issubclass(t, distribution_tensor_coercible._TensorCoercible):
                is_keras_output = True
                t = type.mro(t)[2]
                assert issubclass(t, tfd.Distribution) and not issubclass(t, distribution_tensor_coercible._TensorCoercible)
        if issubclass(t, tf.Tensor):
            if dists[0].shape.ndims == 0:
                return dists[0]
            else:
                return tf.concat(dists, axis=axis)
    if issubclass(t, obd.Distribution):
        pass
    else:
        return dists[0]
        if t not in dist_params:
            raise RuntimeError("Unknown distribution of type '%s' for concatenation" % str(t))
        params_name = dist_params[t]
        params = {}
        for p in params_name:
            attrs = [getattr(d, p) for d in dists]
            is_method = False
            if inspect.ismethod(attrs[0]):
                attrs = [a() for a in attrs]
                is_method = True
            if is_method:
                if '_parameter' == p[-10:]:
                    p = p[:-10]
            params[p] = concat_distribution(attrs, axis=axis)

        if name is not None:
            params['name'] = name
        args = inspect.getfullargspec(t.__init__).args
        if 'allow_nan_stats' in args:
            params['allow_nan_stats'] = allow_nan_stats
        if 'validate_args' in args:
            params['validate_args'] = validate_args
        dist = t(**params)
        return dist