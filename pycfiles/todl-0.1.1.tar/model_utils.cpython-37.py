# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/models/keras_models/model_utils.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 1903 bytes
"""Utils for Keras models."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections, tensorflow as tf
ConvDefs = collections.namedtuple('ConvDefs', ['conv_name', 'filters'])

def get_conv_def(conv_defs, layer_name):
    """Get the custom config for some layer of the model structure.

  Args:
    conv_defs: A named tuple to specify the custom config of the model
      network. See `ConvDefs` for details.
    layer_name: A string, the name of the layer to be customized.

  Returns:
    The number of filters for the layer, or `None` if there is no custom
    config for the requested layer.
  """
    for conv_def in conv_defs:
        if layer_name == conv_def.conv_name:
            return conv_def.filters


def input_layer(shape, placeholder_with_default):
    if tf.executing_eagerly():
        return tf.keras.layers.Input(shape=shape)
    return tf.keras.layers.Input(tensor=placeholder_with_default)