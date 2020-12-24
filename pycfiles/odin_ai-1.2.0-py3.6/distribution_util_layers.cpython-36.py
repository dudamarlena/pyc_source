# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/networks/distribution_util_layers.py
# Compiled at: 2019-09-18 09:29:47
# Size of source mod 2**32: 4622 bytes
from __future__ import absolute_import, division, print_function
import collections, tensorflow as tf
from tensorflow.python.keras.layers import Layer
from tensorflow_probability.python.distributions import Distribution
from tensorflow_probability.python.layers.distribution_layer import DistributionLambda, _get_convert_to_tensor_fn, _serialize
from tensorflow_probability.python.layers.internal import distribution_tensor_coercible as dtc
from tensorflow_probability.python.layers.internal import tensor_tuple
__all__ = [
 'ConcatDistribution', 'Sampling', 'Moments', 'Stddev', 'DistributionAttr']

def _check_distribution(x):
    assert isinstance(x, Distribution), 'Input to this layer must be instance of tensorflow_probability Distribution'


class ConcatDistribution(DistributionLambda):
    __doc__ = ' This layer create a new `Distribution` by concatenate parameters of\n  multiple distributions of the same type along given `axis`\n  '

    def __init__(self, axis=None, convert_to_tensor_fn=Distribution.sample, **kwargs):
        from odin.bay.distributions.utils import concat_distribution
        (super(ConcatDistribution, self).__init__)(
         (lambda dists: concat_distribution(dists=dists, axis=axis)), 
         convert_to_tensor_fn, **kwargs)
        self.axis = axis

    def get_config(self):
        config = super(ConcatDistribution, self).get_config()
        config['axis'] = self.axis
        return config


class Sampling(Layer):
    __doc__ = ' Sample the output from tensorflow-probability\n  distribution layers '

    def __init__(self, n_samples=None, **kwargs):
        (super(Sampling, self).__init__)(**kwargs)
        self.n_samples = n_samples

    def get_config(self):
        config = super(Sampling, self).get_config()
        config['n_samples'] = self.n_samples
        return config

    def call(self, x, n_samples=None, **kwargs):
        if not isinstance(x, Distribution):
            return tf.expand_dims(x, axis=0)
        else:
            if n_samples is None:
                n_samples = self.n_samples
            if n_samples is None:
                return x.sample()
            return x.sample(n_samples)


class Moments(Layer):
    __doc__ = ' Moments '

    def __init__(self, mean=True, variance=True, **kwargs):
        (super(Moments, self).__init__)(**kwargs)
        self.mean = bool(mean)
        self.variance = bool(variance)
        if not self.mean:
            if not self.variance:
                raise AssertionError('This layer must return mean or variance')

    def call(self, x, **kwargs):
        if not isinstance(x, Distribution):
            return x
        else:
            outputs = []
            if self.mean:
                outputs.append(x.mean())
            if self.variance:
                outputs.append(x.variance())
            if len(outputs) == 1:
                return outputs[0]
            return tuple(outputs)

    def get_config(self):
        config = super(Moments, self).get_config()
        config['mean'] = self.mean
        config['variance'] = self.variance
        return config

    def compute_output_shape(self, input_shape):
        if self.mean:
            if self.variance:
                return [input_shape, input_shape]
        return input_shape


class Stddev(Layer):
    __doc__ = ' Get standard deviation of an input distribution, return identity\n  if the input is not an instance of `Distribution` '

    def __init__(self, **kwargs):
        (super(Stddev, self).__init__)(**kwargs)

    def call(self, x, **kwargs):
        if not isinstance(x, Distribution):
            return x
        else:
            return x.stddev()

    def compute_output_shape(self, input_shape):
        return input_shape


class DistributionAttr(Layer):
    __doc__ = ' This layer provide convenient way to extract statistics stored\n  as attributes of the `Distribution` '

    def __init__(self, attr_name, convert_to_tensor_fn=Distribution.sample, **kwargs):
        (super(DistributionAttr, self).__init__)(**kwargs)
        self.attr_name = str(attr_name)
        if isinstance(convert_to_tensor_fn, property):
            convert_to_tensor_fn = convert_to_tensor_fn.fget
        self.convert_to_tensor_fn = convert_to_tensor_fn

    def get_config(self):
        config = super(DistributionAttr, self).get_config()
        config['attr_name'] = self.attr_name
        config['convert_to_tensor_fn'] = self.convert_to_tensor_fn
        return config

    def call(self, x):
        attrs = self.attr_name.split('.')
        for a in attrs:
            x = getattr(x, a)

        if isinstance(x, Distribution):
            if not isinstance(x, dtc._TensorCoercible):
                dist = dtc._TensorCoercible(distribution=x,
                  convert_to_tensor_fn=(self.convert_to_tensor_fn))
                value = tf.convert_to_tensor(value=dist)
                value._tfp_distribution = dist
                dist.shape = value.shape
                dist.get_shape = value.get_shape
                x = dist
        return x