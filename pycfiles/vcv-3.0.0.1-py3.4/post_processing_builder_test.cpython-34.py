# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/post_processing_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 3017 bytes
"""Tests for post_processing_builder."""
import tensorflow as tf
from google.protobuf import text_format
from object_detection.builders import post_processing_builder
from object_detection.protos import post_processing_pb2

class PostProcessingBuilderTest(tf.test.TestCase):

    def test_build_non_max_suppressor_with_correct_parameters(self):
        post_processing_text_proto = '\n      batch_non_max_suppression {\n        score_threshold: 0.7\n        iou_threshold: 0.6\n        max_detections_per_class: 100\n        max_total_detections: 300\n      }\n    '
        post_processing_config = post_processing_pb2.PostProcessing()
        text_format.Merge(post_processing_text_proto, post_processing_config)
        non_max_suppressor, _ = post_processing_builder.build(post_processing_config)
        self.assertEqual(non_max_suppressor.keywords['max_size_per_class'], 100)
        self.assertEqual(non_max_suppressor.keywords['max_total_size'], 300)
        self.assertAlmostEqual(non_max_suppressor.keywords['score_thresh'], 0.7)
        self.assertAlmostEqual(non_max_suppressor.keywords['iou_thresh'], 0.6)

    def test_build_identity_score_converter(self):
        post_processing_text_proto = '\n      score_converter: IDENTITY\n    '
        post_processing_config = post_processing_pb2.PostProcessing()
        text_format.Merge(post_processing_text_proto, post_processing_config)
        _, score_converter = post_processing_builder.build(post_processing_config)
        self.assertEqual(score_converter, tf.identity)

    def test_build_sigmoid_score_converter(self):
        post_processing_text_proto = '\n      score_converter: SIGMOID\n    '
        post_processing_config = post_processing_pb2.PostProcessing()
        text_format.Merge(post_processing_text_proto, post_processing_config)
        _, score_converter = post_processing_builder.build(post_processing_config)
        self.assertEqual(score_converter, tf.sigmoid)

    def test_build_softmax_score_converter(self):
        post_processing_text_proto = '\n      score_converter: SOFTMAX\n    '
        post_processing_config = post_processing_pb2.PostProcessing()
        text_format.Merge(post_processing_text_proto, post_processing_config)
        _, score_converter = post_processing_builder.build(post_processing_config)
        self.assertEqual(score_converter, tf.nn.softmax)


if __name__ == '__main__':
    tf.test.main()