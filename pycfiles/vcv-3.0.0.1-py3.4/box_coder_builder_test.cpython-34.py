# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/box_coder_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 4008 bytes
"""Tests for box_coder_builder."""
import tensorflow as tf
from google.protobuf import text_format
from object_detection.box_coders import faster_rcnn_box_coder
from object_detection.box_coders import mean_stddev_box_coder
from object_detection.box_coders import square_box_coder
from object_detection.builders import box_coder_builder
from object_detection.protos import box_coder_pb2

class BoxCoderBuilderTest(tf.test.TestCase):

    def test_build_faster_rcnn_box_coder_with_defaults(self):
        box_coder_text_proto = '\n      faster_rcnn_box_coder {\n      }\n    '
        box_coder_proto = box_coder_pb2.BoxCoder()
        text_format.Merge(box_coder_text_proto, box_coder_proto)
        box_coder_object = box_coder_builder.build(box_coder_proto)
        self.assertTrue(isinstance(box_coder_object, faster_rcnn_box_coder.FasterRcnnBoxCoder))
        self.assertEqual(box_coder_object._scale_factors, [10.0, 10.0, 5.0, 5.0])

    def test_build_faster_rcnn_box_coder_with_non_default_parameters(self):
        box_coder_text_proto = '\n      faster_rcnn_box_coder {\n        y_scale: 6.0\n        x_scale: 3.0\n        height_scale: 7.0\n        width_scale: 8.0\n      }\n    '
        box_coder_proto = box_coder_pb2.BoxCoder()
        text_format.Merge(box_coder_text_proto, box_coder_proto)
        box_coder_object = box_coder_builder.build(box_coder_proto)
        self.assertTrue(isinstance(box_coder_object, faster_rcnn_box_coder.FasterRcnnBoxCoder))
        self.assertEqual(box_coder_object._scale_factors, [6.0, 3.0, 7.0, 8.0])

    def test_build_mean_stddev_box_coder(self):
        box_coder_text_proto = '\n      mean_stddev_box_coder {\n      }\n    '
        box_coder_proto = box_coder_pb2.BoxCoder()
        text_format.Merge(box_coder_text_proto, box_coder_proto)
        box_coder_object = box_coder_builder.build(box_coder_proto)
        self.assertTrue(isinstance(box_coder_object, mean_stddev_box_coder.MeanStddevBoxCoder))

    def test_build_square_box_coder_with_defaults(self):
        box_coder_text_proto = '\n      square_box_coder {\n      }\n    '
        box_coder_proto = box_coder_pb2.BoxCoder()
        text_format.Merge(box_coder_text_proto, box_coder_proto)
        box_coder_object = box_coder_builder.build(box_coder_proto)
        self.assertTrue(isinstance(box_coder_object, square_box_coder.SquareBoxCoder))
        self.assertEqual(box_coder_object._scale_factors, [10.0, 10.0, 5.0])

    def test_build_square_box_coder_with_non_default_parameters(self):
        box_coder_text_proto = '\n      square_box_coder {\n        y_scale: 6.0\n        x_scale: 3.0\n        length_scale: 7.0\n      }\n    '
        box_coder_proto = box_coder_pb2.BoxCoder()
        text_format.Merge(box_coder_text_proto, box_coder_proto)
        box_coder_object = box_coder_builder.build(box_coder_proto)
        self.assertTrue(isinstance(box_coder_object, square_box_coder.SquareBoxCoder))
        self.assertEqual(box_coder_object._scale_factors, [6.0, 3.0, 7.0])

    def test_raise_error_on_empty_box_coder(self):
        box_coder_text_proto = '\n    '
        box_coder_proto = box_coder_pb2.BoxCoder()
        text_format.Merge(box_coder_text_proto, box_coder_proto)
        with self.assertRaises(ValueError):
            box_coder_builder.build(box_coder_proto)


if __name__ == '__main__':
    tf.test.main()