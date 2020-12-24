# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/anchor_generator_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 8189 bytes
"""Tests for anchor_generator_builder."""
import tensorflow as tf
from google.protobuf import text_format
from object_detection.anchor_generators import grid_anchor_generator
from object_detection.anchor_generators import multiple_grid_anchor_generator
from object_detection.builders import anchor_generator_builder
from object_detection.protos import anchor_generator_pb2

class AnchorGeneratorBuilderTest(tf.test.TestCase):

    def assert_almost_list_equal(self, expected_list, actual_list, delta=None):
        self.assertEqual(len(expected_list), len(actual_list))
        for expected_item, actual_item in zip(expected_list, actual_list):
            self.assertAlmostEqual(expected_item, actual_item, delta=delta)

    def test_build_grid_anchor_generator_with_defaults(self):
        anchor_generator_text_proto = '\n      grid_anchor_generator {\n      }\n     '
        anchor_generator_proto = anchor_generator_pb2.AnchorGenerator()
        text_format.Merge(anchor_generator_text_proto, anchor_generator_proto)
        anchor_generator_object = anchor_generator_builder.build(anchor_generator_proto)
        self.assertTrue(isinstance(anchor_generator_object, grid_anchor_generator.GridAnchorGenerator))
        self.assertListEqual(anchor_generator_object._scales, [])
        self.assertListEqual(anchor_generator_object._aspect_ratios, [])
        with self.test_session() as (sess):
            base_anchor_size, anchor_offset, anchor_stride = sess.run([
             anchor_generator_object._base_anchor_size,
             anchor_generator_object._anchor_offset,
             anchor_generator_object._anchor_stride])
        self.assertAllEqual(anchor_offset, [0, 0])
        self.assertAllEqual(anchor_stride, [16, 16])
        self.assertAllEqual(base_anchor_size, [256, 256])

    def test_build_grid_anchor_generator_with_non_default_parameters(self):
        anchor_generator_text_proto = '\n      grid_anchor_generator {\n        height: 128\n        width: 512\n        height_stride: 10\n        width_stride: 20\n        height_offset: 30\n        width_offset: 40\n        scales: [0.4, 2.2]\n        aspect_ratios: [0.3, 4.5]\n      }\n     '
        anchor_generator_proto = anchor_generator_pb2.AnchorGenerator()
        text_format.Merge(anchor_generator_text_proto, anchor_generator_proto)
        anchor_generator_object = anchor_generator_builder.build(anchor_generator_proto)
        self.assertTrue(isinstance(anchor_generator_object, grid_anchor_generator.GridAnchorGenerator))
        self.assert_almost_list_equal(anchor_generator_object._scales, [
         0.4, 2.2])
        self.assert_almost_list_equal(anchor_generator_object._aspect_ratios, [
         0.3, 4.5])
        with self.test_session() as (sess):
            base_anchor_size, anchor_offset, anchor_stride = sess.run([
             anchor_generator_object._base_anchor_size,
             anchor_generator_object._anchor_offset,
             anchor_generator_object._anchor_stride])
        self.assertAllEqual(anchor_offset, [30, 40])
        self.assertAllEqual(anchor_stride, [10, 20])
        self.assertAllEqual(base_anchor_size, [128, 512])

    def test_build_ssd_anchor_generator_with_defaults(self):
        anchor_generator_text_proto = '\n      ssd_anchor_generator {\n        aspect_ratios: [1.0]\n      }\n    '
        anchor_generator_proto = anchor_generator_pb2.AnchorGenerator()
        text_format.Merge(anchor_generator_text_proto, anchor_generator_proto)
        anchor_generator_object = anchor_generator_builder.build(anchor_generator_proto)
        self.assertTrue(isinstance(anchor_generator_object, multiple_grid_anchor_generator.MultipleGridAnchorGenerator))
        for actual_scales, expected_scales in zip(list(anchor_generator_object._scales), [
         (0.1, 0.2, 0.2),
         (0.35, 0.418),
         (0.499, 0.57),
         (0.649, 0.721),
         (0.799, 0.871),
         (0.949, 0.974)]):
            self.assert_almost_list_equal(expected_scales, actual_scales, delta=0.01)

        for actual_aspect_ratio, expected_aspect_ratio in zip(list(anchor_generator_object._aspect_ratios), [
         (1.0, 2.0, 0.5)] + 5 * [(1.0, 1.0)]):
            self.assert_almost_list_equal(expected_aspect_ratio, actual_aspect_ratio)

        with self.test_session() as (sess):
            base_anchor_size = sess.run(anchor_generator_object._base_anchor_size)
        self.assertAllClose(base_anchor_size, [1.0, 1.0])

    def test_build_ssd_anchor_generator_withoud_reduced_boxes(self):
        anchor_generator_text_proto = '\n      ssd_anchor_generator {\n        aspect_ratios: [1.0]\n        reduce_boxes_in_lowest_layer: false\n      }\n    '
        anchor_generator_proto = anchor_generator_pb2.AnchorGenerator()
        text_format.Merge(anchor_generator_text_proto, anchor_generator_proto)
        anchor_generator_object = anchor_generator_builder.build(anchor_generator_proto)
        self.assertTrue(isinstance(anchor_generator_object, multiple_grid_anchor_generator.MultipleGridAnchorGenerator))
        for actual_scales, expected_scales in zip(list(anchor_generator_object._scales), [
         (0.2, 0.264),
         (0.35, 0.418),
         (0.499, 0.57),
         (0.649, 0.721),
         (0.799, 0.871),
         (0.949, 0.974)]):
            self.assert_almost_list_equal(expected_scales, actual_scales, delta=0.01)

        for actual_aspect_ratio, expected_aspect_ratio in zip(list(anchor_generator_object._aspect_ratios), 6 * [(1.0, 1.0)]):
            self.assert_almost_list_equal(expected_aspect_ratio, actual_aspect_ratio)

        with self.test_session() as (sess):
            base_anchor_size = sess.run(anchor_generator_object._base_anchor_size)
        self.assertAllClose(base_anchor_size, [1.0, 1.0])

    def test_build_ssd_anchor_generator_with_non_default_parameters(self):
        anchor_generator_text_proto = '\n      ssd_anchor_generator {\n        num_layers: 2\n        min_scale: 0.3\n        max_scale: 0.8\n        aspect_ratios: [2.0]\n      }\n    '
        anchor_generator_proto = anchor_generator_pb2.AnchorGenerator()
        text_format.Merge(anchor_generator_text_proto, anchor_generator_proto)
        anchor_generator_object = anchor_generator_builder.build(anchor_generator_proto)
        self.assertTrue(isinstance(anchor_generator_object, multiple_grid_anchor_generator.MultipleGridAnchorGenerator))
        for actual_scales, expected_scales in zip(list(anchor_generator_object._scales), [
         (0.1, 0.3, 0.3), (0.8, )]):
            self.assert_almost_list_equal(expected_scales, actual_scales, delta=0.01)

        for actual_aspect_ratio, expected_aspect_ratio in zip(list(anchor_generator_object._aspect_ratios), [
         (1.0, 2.0, 0.5), (2.0, )]):
            self.assert_almost_list_equal(expected_aspect_ratio, actual_aspect_ratio)

        with self.test_session() as (sess):
            base_anchor_size = sess.run(anchor_generator_object._base_anchor_size)
        self.assertAllClose(base_anchor_size, [1.0, 1.0])

    def test_raise_value_error_on_empty_anchor_genertor(self):
        anchor_generator_text_proto = '\n    '
        anchor_generator_proto = anchor_generator_pb2.AnchorGenerator()
        text_format.Merge(anchor_generator_text_proto, anchor_generator_proto)
        with self.assertRaises(ValueError):
            anchor_generator_builder.build(anchor_generator_proto)


if __name__ == '__main__':
    tf.test.main()