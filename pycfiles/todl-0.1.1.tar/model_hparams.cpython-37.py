# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/model_hparams.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1616 bytes
"""Hyperparameters for the object detection model in TF.learn.

This file consolidates and documents the hyperparameters used by the model.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf

def create_hparams(hparams_overrides=None):
    """Returns hyperparameters, including any flag value overrides.

  Args:
    hparams_overrides: Optional hparams overrides, represented as a
      string containing comma-separated hparam_name=value pairs.

  Returns:
    The hyperparameters as a tf.HParams object.
  """
    hparams = tf.contrib.training.HParams(load_pretrained=True)
    if hparams_overrides:
        hparams = hparams.parse(hparams_overrides)
    return hparams