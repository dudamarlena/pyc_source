# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/bay/distributions/zero_inflated.py
# Compiled at: 2019-09-17 08:51:50
# Size of source mod 2**32: 11720 bytes
"""The ZeroInflated distribution class."""
from __future__ import absolute_import, division, print_function
import tensorflow as tf
from tensorflow_probability.python.distributions import Bernoulli, Independent, distribution
from tensorflow_probability.python.internal import reparameterization
from tensorflow_probability.python.util.seed_stream import SeedStream
__all__ = [
 'ZeroInflated']

def _broadcast_rate(probs, *others):
    others = list(others)
    others_ndims = [o.shape.ndims for o in others]
    assert len(set(others_ndims)) == 1
    others_ndims = others_ndims[0]
    probs_ndims = probs.shape.ndims
    if others_ndims < probs_ndims:
        for i in range(probs_ndims - others_ndims):
            others = [tf.expand_dims(o, -1) for o in others]

    else:
        if others_ndims > probs_ndims:
            for i in range(others_ndims - probs_ndims):
                probs = tf.expand_dims(probs, -1)

    return [
     probs] + others


class ZeroInflated(distribution.Distribution):
    __doc__ = 'zero-inflated distribution.\n\n  The `zero-inflated` object implements batched zero-inflated distributions.\n  The zero-inflated model is defined by a zero-inflation rate\n  and a python list of `Distribution` objects.\n\n  Methods supported include `log_prob`, `prob`, `mean`, `sample`, and\n  `entropy_lower_bound`.\n  '

    def __init__(self, count_distribution, inflated_distribution=None, logits=None, probs=None, validate_args=False, allow_nan_stats=True, name='ZeroInflated'):
        """Initialize a zero-inflated distribution.

    A `ZeroInflated` is defined by a zero-inflation rate (`inflated_distribution`,
    representing the probabilities of excess zeros) and a `Distribution` object
    having matching dtype, batch shape, event shape, and continuity
    properties (the dist).

    Parameters
    ----------
    count_distribution : A `tfp.distributions.Distribution` instance.
      The instance must have `batch_shape` matching the zero-inflation
      distribution.

    inflated_distribution: `tfp.distributions.Bernoulli`-like instance.
      Manages the probability of excess zeros, the zero-inflated rate.
      Must have either scalar `batch_shape` or `batch_shape` matching
      `count_distribution.batch_shape`.

    logits: An N-D `Tensor` representing the log-odds of a excess zeros
      A zero-inflation rate, where the probability of excess zeros is
      sigmoid(logits).
      Only one of `logits` or `probs` should be passed in.

    probs: An N-D `Tensor` representing the probability of a zero event.
      Each entry in the `Tensor` parameterizes an independent
      ZeroInflated distribution.
      Only one of `logits` or `probs` should be passed in.

    validate_args: Python `bool`, default `False`. If `True`, raise a runtime
      error if batch or event ranks are inconsistent between pi and any of
      the distributions. This is only checked if the ranks cannot be
      determined statically at graph construction time.

    allow_nan_stats: Boolean, default `True`. If `False`, raise an
     exception if a statistic (e.g. mean/mode/etc...) is undefined for any
      batch member. If `True`, batch members with valid parameters leading to
      undefined statistics will return NaN for this statistic.

    name: A name for this distribution (optional).

    References
    ----------
    Liu, L. & Blei, D.M.. (2017). Zero-Inflated Exponential Family Embeddings.
    Proceedings of the 34th International Conference on Machine Learning,
    in PMLR 70:2140-2148

    """
        parameters = dict(locals())
        self._runtime_assertions = []
        with tf.compat.v1.name_scope(name) as (name):
            if not isinstance(count_distribution, distribution.Distribution):
                raise TypeError('count_distribution must be a Distribution instance but saw: %s' % count_distribution)
            else:
                self._count_distribution = count_distribution
                if inflated_distribution is None:
                    inflated_distribution = Bernoulli(logits=logits, probs=probs,
                      dtype=(tf.int32),
                      validate_args=validate_args,
                      allow_nan_stats=allow_nan_stats,
                      name='ZeroInflatedRate')
                elif not isinstance(inflated_distribution, distribution.Distribution):
                    raise TypeError('inflated_distribution must be a Distribution instance but saw: %s' % inflated_distribution)
                else:
                    self._inflated_distribution = inflated_distribution
                    if self._count_distribution.batch_shape.ndims is None:
                        raise ValueError('Expected to know rank(batch_shape) from count_disttribution')
                    if self._inflated_distribution.batch_shape.ndims is None:
                        raise ValueError('Expected to know rank(batch_shape) from inflated_distribution')
                    inflated_batch_ndims = self._inflated_distribution.batch_shape.ndims
                    count_batch_ndims = self._count_distribution.batch_shape.ndims
                    if count_batch_ndims < inflated_batch_ndims:
                        self._inflated_distribution = Independent((self._inflated_distribution),
                          reinterpreted_batch_ndims=(inflated_batch_ndims - count_batch_ndims),
                          name='ZeroInflatedRate')
                    elif count_batch_ndims > inflated_batch_ndims:
                        raise ValueError('count_distribution has %d-D batch_shape, which smallerthan %d-D batch_shape of inflated_distribution' % (
                         count_batch_ndims, inflated_batch_ndims))
                if validate_args:
                    self._runtime_assertions.append(tf.assert_equal((self._count_distribution.batch_shape_tensor()),
                      (self._inflated_distribution.batch_shape_tensor()),
                      message='dist batch shape must match logits|probs batch shape'))
        reparameterization_type = [
         self._count_distribution.reparameterization_type,
         self._inflated_distribution.reparameterization_type]
        if any(i == reparameterization.NOT_REPARAMETERIZED for i in reparameterization_type):
            reparameterization_type = reparameterization.NOT_REPARAMETERIZED
        else:
            reparameterization_type = reparameterization.FULLY_REPARAMETERIZED
        super(ZeroInflated, self).__init__(dtype=(self._count_distribution.dtype), reparameterization_type=reparameterization_type,
          validate_args=validate_args,
          allow_nan_stats=allow_nan_stats,
          parameters=parameters,
          graph_parents=(self._count_distribution._graph_parents + self._inflated_distribution._graph_parents),
          name=name)

    @property
    def logits(self):
        """Log-odds of a `1` outcome (vs `0`)."""
        if isinstance(self._inflated_distribution, Independent):
            return self._inflated_distribution.distribution.logits_parameter()
        else:
            return self._inflated_distribution.logits_parameter()

    @property
    def probs(self):
        """Probability of a `1` outcome (vs `0`)."""
        if isinstance(self._inflated_distribution, Independent):
            return self._inflated_distribution.distribution.probs_parameter()
        else:
            return self._inflated_distribution.probs_parameter()

    @property
    def count_distribution(self):
        return self._count_distribution

    @property
    def inflated_distribution(self):
        return self._inflated_distribution

    def _batch_shape_tensor(self):
        return self._count_distribution._batch_shape_tensor()

    def _batch_shape(self):
        return self._count_distribution._batch_shape()

    def _event_shape_tensor(self):
        return self._count_distribution._event_shape_tensor()

    def _event_shape(self):
        return self._count_distribution._event_shape()

    def _mean(self):
        with tf.compat.v1.control_dependencies(self._runtime_assertions):
            probs, d_mean = _broadcast_rate(self.probs, self._count_distribution.mean())
            return (1 - probs) * d_mean

    def _variance(self):
        """
    (1 - pi) * (d.var + d.mean^2) - [(1 - pi) * d.mean]^2

    Note: mean(ZeroInflated) = (1 - pi) * d.mean
    where:
     - pi is zero-inflated rate
     - d is count distribution
    """
        with tf.compat.v1.control_dependencies(self._runtime_assertions):
            d = self._count_distribution
            probs, d_mean, d_variance = _broadcast_rate(self.probs, d.mean(), d.variance())
            return (1 - probs) * (d_variance + tf.square(d_mean)) - tf.math.square(self._mean())

    def _log_prob(self, x):
        with tf.compat.v1.control_dependencies(self._runtime_assertions):
            eps = tf.cast(1e-08, x.dtype)
            x = tf.convert_to_tensor(x, name='x')
            d = self._count_distribution
            pi = self.probs
            log_prob = d.log_prob(x)
            prob = tf.math.exp(log_prob)
            pi, prob, log_prob = _broadcast_rate(pi, prob, log_prob)
            y_0 = tf.math.log(pi + (1 - pi) * prob)
            y_1 = tf.math.log(1 - pi) + log_prob
            return tf.where(x <= eps, y_0, y_1)

    def _prob(self, x):
        return tf.math.exp(self._log_prob(x))

    def _sample_n(self, n, seed):
        with tf.compat.v1.control_dependencies(self._runtime_assertions):
            seed = SeedStream(seed, salt='ZeroInflated')
            mask = self.inflated_distribution.sample(n, seed())
            samples = self.count_distribution.sample(n, seed())
            mask, samples = _broadcast_rate(mask, samples)
            return samples * tf.cast(1 - mask, samples.dtype)

    def denoised_mean(self):
        return self.count_distribution.mean()

    def denoised_variance(self):
        return self.count_distribution.variance()