# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/lstm_object_detection/models/mobilenet_defs.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 5619 bytes
"""Definitions for modified MobileNet models used in LSTD."""
import tensorflow.compat.v1 as tf
import tensorflow.contrib as contrib_slim
from nets import mobilenet_v1
import nets.mobilenet as mobilenet_convs
import nets.mobilenet as mobilenet
slim = contrib_slim

def mobilenet_v1_lite_def(depth_multiplier, low_res=False):
    """Conv definitions for a lite MobileNet v1 model.

  Args:
    depth_multiplier: float depth multiplier for MobileNet.
    low_res: An option of low-res conv input for interleave model.

  Returns:
    Array of convolutions.

  Raises:
    ValueError: On invalid channels with provided depth multiplier.
  """
    conv = mobilenet_v1.Conv
    sep_conv = mobilenet_v1.DepthSepConv

    def _find_target_depth(original, depth_multiplier):
        pseudo_target = int(original / depth_multiplier)
        for target in range(pseudo_target - 1, pseudo_target + 2):
            if int(target * depth_multiplier) == original:
                return target

        raise ValueError('Cannot have %d channels with depth multiplier %0.2f' % (
         original, depth_multiplier))

    return [
     conv(kernel=[3, 3], stride=2, depth=32),
     sep_conv(kernel=[3, 3], stride=1, depth=64),
     sep_conv(kernel=[3, 3], stride=2, depth=128),
     sep_conv(kernel=[3, 3], stride=1, depth=128),
     sep_conv(kernel=[3, 3], stride=2, depth=256),
     sep_conv(kernel=[3, 3], stride=1, depth=256),
     sep_conv(kernel=[3, 3], stride=2, depth=512),
     sep_conv(kernel=[3, 3], stride=1, depth=512),
     sep_conv(kernel=[3, 3], stride=1, depth=512),
     sep_conv(kernel=[3, 3], stride=1, depth=512),
     sep_conv(kernel=[3, 3], stride=1, depth=512),
     sep_conv(kernel=[3, 3], stride=1, depth=512),
     sep_conv(kernel=[3, 3], stride=(1 if low_res else 2), depth=1024),
     sep_conv(kernel=[
      3, 3],
       stride=1,
       depth=(int(_find_target_depth(1024, depth_multiplier))))]


def mobilenet_v2_lite_def(reduced=False, is_quantized=False, low_res=False):
    """Conv definitions for a lite MobileNet v2 model.

  Args:
    reduced: Determines the scaling factor for expanded conv. If True, a factor
        of 6 is used. If False, a factor of 3 is used.
    is_quantized: Whether the model is trained in quantized mode.
    low_res: Whether the input to the model is of half resolution.

  Returns:
    Array of convolutions.
  """
    expanded_conv = mobilenet_convs.expanded_conv
    expand_input = mobilenet_convs.expand_input_by_factor
    op = mobilenet.op
    return dict(defaults={(
 slim.batch_norm,): {'center':True, 
                            'scale':True}, 
     
     (
 slim.conv2d, slim.fully_connected, slim.separable_conv2d): {'normalizer_fn':slim.batch_norm, 
                                                                    'activation_fn':tf.nn.relu6}, 
     
     (
 expanded_conv,): {'expansion_size':expand_input(6), 
                          'split_expansion':1, 
                          'normalizer_fn':slim.batch_norm, 
                          'residual':True}, 
     
     (
 slim.conv2d, slim.separable_conv2d): {'padding': 'SAME'}},
      spec=[
     op((slim.conv2d), stride=2, num_outputs=32, kernel_size=[3, 3]),
     op(expanded_conv, expansion_size=expand_input(1, divisible_by=1),
       num_outputs=16),
     op(expanded_conv, expansion_size=(expand_input(3, divisible_by=1) if reduced else expand_input(6)),
       stride=2,
       num_outputs=24),
     op(expanded_conv, expansion_size=(expand_input(3, divisible_by=1) if reduced else expand_input(6)),
       stride=1,
       num_outputs=24),
     op(expanded_conv, stride=2, num_outputs=32),
     op(expanded_conv, stride=1, num_outputs=32),
     op(expanded_conv, stride=1, num_outputs=32),
     op(expanded_conv, stride=2, num_outputs=64),
     op(expanded_conv, stride=1, num_outputs=64),
     op(expanded_conv, stride=1, num_outputs=64),
     op(expanded_conv, stride=1, num_outputs=64),
     op(expanded_conv, stride=1, num_outputs=96),
     op(expanded_conv, stride=1, num_outputs=96),
     op(expanded_conv, stride=1, num_outputs=96),
     op(expanded_conv, stride=(1 if low_res else 2), num_outputs=160),
     op(expanded_conv, stride=1, num_outputs=160),
     op(expanded_conv, stride=1, num_outputs=160),
     op(expanded_conv, stride=1,
       num_outputs=320,
       project_activation_fn=(tf.nn.relu6 if is_quantized else tf.identity))])