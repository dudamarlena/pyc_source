# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/models/ssd_mobilenet_v1_ppn_feature_extractor.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 3299 bytes
"""SSDFeatureExtractor for MobilenetV1 PPN features."""
import tensorflow as tf
import tensorflow.contrib as contrib_slim
from object_detection.meta_architectures import ssd_meta_arch
from object_detection.models import feature_map_generators
from object_detection.utils import context_manager
from object_detection.utils import ops
from object_detection.utils import shape_utils
from nets import mobilenet_v1
slim = contrib_slim

class SSDMobileNetV1PpnFeatureExtractor(ssd_meta_arch.SSDFeatureExtractor):
    __doc__ = 'SSD Feature Extractor using MobilenetV1 PPN features.'

    def preprocess(self, resized_inputs):
        """SSD preprocessing.

    Maps pixel values to the range [-1, 1].

    Args:
      resized_inputs: a [batch, height, width, channels] float tensor
        representing a batch of images.

    Returns:
      preprocessed_inputs: a [batch, height, width, channels] float tensor
        representing a batch of images.
    """
        return 0.00784313725490196 * resized_inputs - 1.0

    def extract_features(self, preprocessed_inputs):
        """Extract features from preprocessed inputs.

    Args:
      preprocessed_inputs: a [batch, height, width, channels] float tensor
        representing a batch of images.

    Returns:
      feature_maps: a list of tensors where the ith tensor has shape
        [batch, height_i, width_i, depth_i]
    """
        preprocessed_inputs = shape_utils.check_min_image_dim(33, preprocessed_inputs)
        with tf.variable_scope('MobilenetV1', reuse=(self._reuse_weights)) as (scope):
            with slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope(is_training=None,
              regularize_depthwise=True)):
                with slim.arg_scope(self._conv_hyperparams_fn()) if self._override_base_feature_extractor_hyperparams else context_manager.IdentityContextManager():
                    _, image_features = mobilenet_v1.mobilenet_v1_base((ops.pad_to_multiple(preprocessed_inputs, self._pad_to_multiple)),
                      final_endpoint='Conv2d_13_pointwise',
                      min_depth=(self._min_depth),
                      depth_multiplier=(self._depth_multiplier),
                      use_explicit_padding=(self._use_explicit_padding),
                      scope=scope)
            with slim.arg_scope(self._conv_hyperparams_fn()):
                feature_maps = feature_map_generators.pooling_pyramid_feature_maps(base_feature_map_depth=0,
                  num_layers=6,
                  image_features={'image_features': image_features['Conv2d_11_pointwise']})
        return feature_maps.values()