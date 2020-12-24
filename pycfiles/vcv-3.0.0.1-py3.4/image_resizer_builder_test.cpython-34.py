# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/image_resizer_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 2611 bytes
"""Tests for object_detection.builders.image_resizer_builder."""
import tensorflow as tf
from google.protobuf import text_format
from object_detection.builders import image_resizer_builder
from object_detection.protos import image_resizer_pb2

class ImageResizerBuilderTest(tf.test.TestCase):

    def _shape_of_resized_random_image_given_text_proto(self, input_shape, text_proto):
        image_resizer_config = image_resizer_pb2.ImageResizer()
        text_format.Merge(text_proto, image_resizer_config)
        image_resizer_fn = image_resizer_builder.build(image_resizer_config)
        images = tf.to_float(tf.random_uniform(input_shape, minval=0, maxval=255, dtype=tf.int32))
        resized_images = image_resizer_fn(images)
        with self.test_session() as (sess):
            return sess.run(resized_images).shape

    def test_built_keep_aspect_ratio_resizer_returns_expected_shape(self):
        image_resizer_text_proto = '\n      keep_aspect_ratio_resizer {\n        min_dimension: 10\n        max_dimension: 20\n      }\n    '
        input_shape = (50, 25, 3)
        expected_output_shape = (20, 10, 3)
        output_shape = self._shape_of_resized_random_image_given_text_proto(input_shape, image_resizer_text_proto)
        self.assertEqual(output_shape, expected_output_shape)

    def test_built_fixed_shape_resizer_returns_expected_shape(self):
        image_resizer_text_proto = '\n      fixed_shape_resizer {\n        height: 10\n        width: 20\n      }\n    '
        input_shape = (50, 25, 3)
        expected_output_shape = (10, 20, 3)
        output_shape = self._shape_of_resized_random_image_given_text_proto(input_shape, image_resizer_text_proto)
        self.assertEqual(output_shape, expected_output_shape)

    def test_raises_error_on_invalid_input(self):
        invalid_input = 'invalid_input'
        with self.assertRaises(ValueError):
            image_resizer_builder.build(invalid_input)


if __name__ == '__main__':
    tf.test.main()