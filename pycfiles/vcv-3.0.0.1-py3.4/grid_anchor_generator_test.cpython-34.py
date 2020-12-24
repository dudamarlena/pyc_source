# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/anchor_generators/grid_anchor_generator_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 2950 bytes
"""Tests for object_detection.grid_anchor_generator."""
import tensorflow as tf
from object_detection.anchor_generators import grid_anchor_generator

class GridAnchorGeneratorTest(tf.test.TestCase):

    def test_construct_single_anchor(self):
        """Builds a 1x1 anchor grid to test the size of the output boxes."""
        scales = [
         0.5, 1.0, 2.0]
        aspect_ratios = [0.25, 1.0, 4.0]
        anchor_offset = [7, -3]
        exp_anchor_corners = [[-121, -35, 135, 29], [-249, -67, 263, 61],
         [
          -505, -131, 519, 125], [-57, -67, 71, 61],
         [
          -121, -131, 135, 125], [-249, -259, 263, 253],
         [
          -25, -131, 39, 125], [-57, -259, 71, 253],
         [
          -121, -515, 135, 509]]
        anchor_generator = grid_anchor_generator.GridAnchorGenerator(scales, aspect_ratios, anchor_offset=anchor_offset)
        anchors = anchor_generator.generate(feature_map_shape_list=[(1, 1)])
        anchor_corners = anchors.get()
        with self.test_session():
            anchor_corners_out = anchor_corners.eval()
            self.assertAllClose(anchor_corners_out, exp_anchor_corners)

    def test_construct_anchor_grid(self):
        base_anchor_size = [10, 10]
        anchor_stride = [19, 19]
        anchor_offset = [0, 0]
        scales = [0.5, 1.0, 2.0]
        aspect_ratios = [1.0]
        exp_anchor_corners = [
         [
          -2.5, -2.5, 2.5, 2.5], [-5.0, -5.0, 5.0, 5.0],
         [
          -10.0, -10.0, 10.0, 10.0], [-2.5, 16.5, 2.5, 21.5],
         [
          -5.0, 14.0, 5, 24], [-10.0, 9.0, 10, 29],
         [
          16.5, -2.5, 21.5, 2.5], [14.0, -5.0, 24, 5],
         [
          9.0, -10.0, 29, 10], [16.5, 16.5, 21.5, 21.5],
         [
          14.0, 14.0, 24, 24], [9.0, 9.0, 29, 29]]
        anchor_generator = grid_anchor_generator.GridAnchorGenerator(scales, aspect_ratios, base_anchor_size=base_anchor_size, anchor_stride=anchor_stride, anchor_offset=anchor_offset)
        anchors = anchor_generator.generate(feature_map_shape_list=[(2, 2)])
        anchor_corners = anchors.get()
        with self.test_session():
            anchor_corners_out = anchor_corners.eval()
            self.assertAllClose(anchor_corners_out, exp_anchor_corners)


if __name__ == '__main__':
    tf.test.main()