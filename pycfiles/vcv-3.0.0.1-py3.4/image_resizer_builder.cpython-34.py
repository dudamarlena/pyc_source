# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/image_resizer_builder.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 2714 bytes
"""Builder function for image resizing operations."""
import functools
from object_detection.core import preprocessor
from object_detection.protos import image_resizer_pb2

def build(image_resizer_config):
    """Builds callable for image resizing operations.

  Args:
    image_resizer_config: image_resizer.proto object containing parameters for
      an image resizing operation.

  Returns:
    image_resizer_fn: Callable for image resizing.  This callable always takes
      a rank-3 image tensor (corresponding to a single image) and returns a
      rank-3 image tensor, possibly with new spatial dimensions.

  Raises:
    ValueError: if `image_resizer_config` is of incorrect type.
    ValueError: if `image_resizer_config.image_resizer_oneof` is of expected
      type.
    ValueError: if min_dimension > max_dimension when keep_aspect_ratio_resizer
      is used.
  """
    if not isinstance(image_resizer_config, image_resizer_pb2.ImageResizer):
        raise ValueError('image_resizer_config not of type image_resizer_pb2.ImageResizer.')
    if image_resizer_config.WhichOneof('image_resizer_oneof') == 'keep_aspect_ratio_resizer':
        keep_aspect_ratio_config = image_resizer_config.keep_aspect_ratio_resizer
        if not keep_aspect_ratio_config.min_dimension <= keep_aspect_ratio_config.max_dimension:
            raise ValueError('min_dimension > max_dimension')
        return functools.partial(preprocessor.resize_to_range, min_dimension=keep_aspect_ratio_config.min_dimension, max_dimension=keep_aspect_ratio_config.max_dimension)
    if image_resizer_config.WhichOneof('image_resizer_oneof') == 'fixed_shape_resizer':
        fixed_shape_resizer_config = image_resizer_config.fixed_shape_resizer
        return functools.partial(preprocessor.resize_image, new_height=fixed_shape_resizer_config.height, new_width=fixed_shape_resizer_config.width)
    raise ValueError('Invalid image resizer option.')