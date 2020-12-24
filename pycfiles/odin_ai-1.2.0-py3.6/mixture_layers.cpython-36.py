# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/bay/distribution_layers/mixture_layers.py
# Compiled at: 2019-08-21 09:47:12
# Size of source mod 2**32: 498 bytes
from __future__ import absolute_import, division, print_function
import tensorflow as tf
from tensorflow_probability.python.layers import MixtureLogistic, MixtureNormal, MixtureSameFamily
__all__ = [
 'MixtureLogisticLayer', 'MixtureNormalLayer', 'MixtureSameFamilyLayer']
MixtureLogisticLayer = MixtureLogistic
MixtureNormalLayer = MixtureNormal
MixtureSameFamilyLayer = MixtureSameFamily