# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/models/autoencoder.py
# Compiled at: 2019-09-04 06:01:19
# Size of source mod 2**32: 4083 bytes
from __future__ import absolute_import, division, print_function
from typing import Iterable
import tensorflow as tf
from tensorflow.python.keras.layers import Dense, Layer
from odin.bay.helpers import Statistic
from odin.networks import DenseDeterministic, DenseDistribution, Identity, Parallel
from sisua.models.base import SingleCellModel
from sisua.models.networks import DenseNetwork

class DeepCountAutoencoder(SingleCellModel):
    __doc__ = ' Deep Count Autoencoder\n\n  '

    def __init__(self, units, dispersion='full', xdist='zinb', xdrop=0.3, edrop=0, zdrop=0, ddrop=0, hdim=128, zdim=32, biased_latent=False, nlayers=2, batchnorm=True, linear_decoder=False, **kwargs):
        (super(DeepCountAutoencoder, self).__init__)(units=units, xdist=xdist, 
         dispersion=dispersion, 
         parameters=locals(), **kwargs)
        self.encoder = DenseNetwork(n_units=hdim, nlayers=nlayers,
          activation='relu',
          batchnorm=batchnorm,
          input_dropout=xdrop,
          output_dropout=edrop,
          seed=(self.seed),
          name='Encoder')
        if linear_decoder:
            self.decoder = Identity(name='Decoder')
        else:
            self.decoder = DenseNetwork(n_units=hdim, nlayers=nlayers,
              activation='relu',
              batchnorm=batchnorm,
              input_dropout=zdrop,
              output_dropout=ddrop,
              seed=(self.seed),
              name='Decoder')
        self.latent_layer = DenseDeterministic(zdim, use_bias=(bool(biased_latent)),
          activation='linear',
          name='Latent')
        for idx, (units, posterior, activation) in enumerate(zip(self.units, self.xdist, self.xactiv)):
            name = 'output_layer%d' % idx
            post = DenseDistribution(units=units,
              posterior=posterior,
              activation=activation,
              posterior_kwargs=dict(dispersion=(self.dispersion)))
            setattr(self, name, post)

    def _call(self, x, lmean, lvar, t, y, masks, training, n_samples):
        e = self.encoder(x, training=training)
        qZ = self.latent_layer(e)
        d = self.decoder((qZ.sample(1)), training=training)
        pX = [getattr(self, 'output_layer%d' % i)(d, mode=(Statistic.DIST)) for i in range(self.n_outputs)]
        loss_x = self.xloss[0](t, pX[0])
        loss_y = tf.convert_to_tensor(0, dtype=(x.dtype))
        for i_true, m, i_pred, fn_loss in zip(y, masks, pX[1:], self.xloss[1:]):
            loss_y += fn_loss(i_true, i_pred) * m

        loss = tf.reduce_mean(loss_x + loss_y)
        if training:
            self.add_loss(loss)
        self.add_metric(loss_x, 'mean', 'loss_x')
        if self.is_semi_supervised:
            self.add_metric(loss_y, 'mean', 'loss_y')
        return (pX, qZ)