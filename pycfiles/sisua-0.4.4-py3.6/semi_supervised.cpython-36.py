# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/sisua/models/semi_supervised.py
# Compiled at: 2019-09-23 04:47:24
# Size of source mod 2**32: 2703 bytes
from __future__ import absolute_import, division, print_function
from typing import Iterable, List, Text, Union
import tensorflow as tf
from tensorflow.python.keras.layers import Layer
from odin.bay import Statistic
from odin.bay.distribution_alias import parse_distribution
from odin.networks import DenseDistribution, Parallel
from odin.utils import as_tuple
from sisua.models.autoencoder import DeepCountAutoencoder
from sisua.models.base import SingleCellModel
from sisua.models.scvi_models import SCVI
from sisua.models.variational_autoencoder import VariationalAutoEncoder

class MultitaskAutoEncoder(DeepCountAutoencoder):
    __doc__ = ' Multitask Auto Encoder\n  '

    def __init__(self, units, dispersion='full', xdist=[
 'zinb', 'nb'], xdrop=0.3, edrop=0, zdrop=0, ddrop=0, hdim=128, zdim=32, biased_latent=False, nlayers=2, batchnorm=True, linear_decoder=False, **kwargs):
        kw = dict(locals())
        del kw['self']
        del kw['__class__']
        del kw['kwargs']
        kw.update(kwargs)
        (super(MultitaskAutoEncoder, self).__init__)(**kw)


class MultitaskVAE(VariationalAutoEncoder):
    __doc__ = ' Variational autoencoder with multitask learning extension\n  '

    def __init__(self, units, dispersion='full', xdist=[
 'zinb', 'nb'], zdist='normal', xdrop=0.3, edrop=0, zdrop=0, ddrop=0, hdim=128, zdim=32, nlayers=2, batchnorm=True, linear_decoder=False, **kwargs):
        kw = dict(locals())
        del kw['self']
        del kw['__class__']
        del kw['kwargs']
        kw.update(kwargs)
        (super(MultitaskVAE, self).__init__)(**kw)


class MultitaskVI(SCVI):
    __doc__ = ' Semi-supervised implementation of scVI\n  '

    def __init__(self, units, dispersion='full', xdist=[
 'zinbd', 'nb'], zdist='normal', ldist='normal', xdrop=0.3, edrop=0, zdrop=0, ddrop=0, hdim=128, zdim=32, nlayers=2, clip_library=12, batchnorm=True, linear_decoder=False, **kwargs):
        kw = dict(locals())
        del kw['self']
        del kw['__class__']
        del kw['kwargs']
        kw.update(kwargs)
        (super(MultitaskVI, self).__init__)(**kw)