# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/models/latents.py
# Compiled at: 2019-08-28 02:06:54
# Size of source mod 2**32: 2788 bytes
from __future__ import absolute_import, division, print_function
from typing import Type
import tensorflow as tf
from tensorflow_probability.python.distributions import LogNormal, MultivariateNormalDiag, Normal
from odin.bay.distribution_layers import LogNormalLayer, MultivariateNormalLayer, NormalLayer
from odin.networks import DenseDistribution

class NormalDiagLatent(DenseDistribution):

    def __init__(self, units, use_bias=True, name='LatentSpace'):
        super(NormalDiagLatent, self).__init__(units=units,
          posterior=MultivariateNormalLayer(event_size=units, covariance_type='diag',
          softplus_scale=True),
          prior=MultivariateNormalDiag(loc=tf.zeros(shape=units), scale_identity_multiplier=1),
          use_bias=use_bias,
          name=name)


class NormalLatent(DenseDistribution):

    def __init__(self, units, use_bias=True, name='LatentSpace'):
        super(NormalLatent, self).__init__(units=units, posterior=NormalLayer(event_shape=units, softplus_scale=True),
          prior=Normal(loc=tf.zeros(shape=units), scale=tf.ones(shape=units)),
          use_bias=use_bias,
          name=name)


class LogNormalLatent(DenseDistribution):

    def __init__(self, units, use_bias=True, name='LatentSpace'):
        super(LogNormalLatent, self).__init__(units=units, posterior=LogNormalLayer(event_shape=units, softplus_scale=True),
          prior=LogNormal(loc=tf.zeros(shape=units), scale=tf.ones(shape=units)),
          use_bias=use_bias,
          name=name)


class MixedNormalLatent(DenseDistribution):
    pass


class DirichletLatent(DenseDistribution):
    pass


_latent_map = {'normal':NormalLatent, 
 'diag':NormalDiagLatent, 
 'mixed':MixedNormalLatent, 
 'diri':DirichletLatent, 
 'lognormal':LogNormalLatent}

def get_latent(name):
    name = str(name).lower()
    if name not in _latent_map:
        raise ValueError("Only support following latent: %s; but given: '%s'" % (
         ', '.join(_latent_map.keys()), name))
    return _latent_map[name]