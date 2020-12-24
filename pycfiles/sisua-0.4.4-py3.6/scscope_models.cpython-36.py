# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/models/scscope_models.py
# Compiled at: 2019-09-04 07:50:35
# Size of source mod 2**32: 2266 bytes
from __future__ import absolute_import, division, print_function
import tensorflow as tf
from odin.networks import DenseDeterministic
from sisua.models.base import SingleCellModel
from sisua.models.networks import DenseNetwork

class SCScope(SingleCellModel):

    def __init__(self, units, steps=1, dispersion='full', xdist='zinbd', zdist='normal', ldist='normal', xdrop=0.3, edrop=0, zdrop=0, ddrop=0, hdim=128, zdim=32, nlayers=2, clip_library=12, batchnorm=True, linear_decoder=False, **kwargs):
        (super(SCScope, self).__init__)(units=units, xdist=xdist, 
         dispersion=dispersion, 
         parameters=locals(), **kwargs)
        self.steps = int(steps)
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

    def _call(self, x, lmean, lvar, t, y, masks, training=None, n_samples=None):
        exit()