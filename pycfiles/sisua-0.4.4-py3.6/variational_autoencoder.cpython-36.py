# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/models/variational_autoencoder.py
# Compiled at: 2019-08-30 04:27:19
# Size of source mod 2**32: 4321 bytes
from __future__ import absolute_import, division, print_function
import inspect, tensorflow as tf
from tensorflow.python.keras.layers import Layer
from odin.bay import Statistic, kl_divergence, print_dist
from odin.networks import DenseDistribution, Identity
from sisua.models.base import SingleCellModel
from sisua.models.latents import get_latent
from sisua.models.networks import DenseNetwork

class VariationalAutoEncoder(SingleCellModel):
    __doc__ = ' Variational Auto Encoder\n  '

    def __init__(self, units, dispersion='full', xdist='zinb', zdist='normal', xdrop=0.3, edrop=0, zdrop=0, ddrop=0, hdim=128, zdim=32, nlayers=2, batchnorm=True, linear_decoder=False, **kwargs):
        (super(VariationalAutoEncoder, self).__init__)(units=units, xdist=xdist, 
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
            self.decoder = Identity(name='LinearDecoder')
        else:
            self.decoder = DenseNetwork(n_units=hdim, nlayers=nlayers,
              activation='relu',
              batchnorm=batchnorm,
              input_dropout=zdrop,
              output_dropout=ddrop,
              seed=(self.seed),
              name='Decoder')
        self.latent = get_latent(zdist)(units=zdim, name=(self.name + 'Latent'))
        for idx, (units, posterior, activation) in enumerate(zip(self.units, self.xdist, self.xactiv)):
            name = 'output_layer%d' % idx
            post = DenseDistribution(units=units,
              posterior=posterior,
              activation=activation,
              posterior_kwargs=dict(dispersion=(self.dispersion)))
            setattr(self, name, post)

    def _call(self, x, lmean, lvar, t, y, masks, training, n_samples):
        e = self.encoder(x, training=training)
        qZ = self.latent(e, training=training,
          n_samples=n_samples,
          mode=(Statistic.DIST))
        d = self.decoder((qZ.sample(n_samples)), training=training)
        pX = [getattr(self, 'output_layer%d' % i)(d, mode=(Statistic.DIST)) for i in range(self.n_outputs)]
        loss_x = self.xloss[0](t, pX[0])
        loss_y = tf.convert_to_tensor(0, dtype=(x.dtype))
        for i_true, m, i_pred, fn_loss in zip(y, masks, pX[1:], self.xloss[1:]):
            loss_y += fn_loss(i_true, i_pred) * m

        kl = self.latent.kl_divergence(analytic_kl=(self.kl_analytic), n_samples=n_samples)
        elbo = -loss_x - loss_y - kl * self.kl_weight
        elbo = tf.reduce_logsumexp(elbo, axis=0)
        loss = tf.reduce_mean(-elbo)
        if training:
            self.add_loss(loss)
        self.add_metric((tf.reduce_mean(kl)), aggregation='mean', name='KLqp')
        self.add_metric((tf.reduce_mean(loss_x)), aggregation='mean', name='nllk_x')
        if self.is_semi_supervised:
            self.add_metric((tf.reduce_mean(loss_y)), aggregation='mean', name='nllk_y')
        return (pX, qZ)