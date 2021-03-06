# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/box_coders/keypoint_box_coder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 5900 bytes
"""Tests for object_detection.box_coder.keypoint_box_coder."""
import tensorflow as tf
from object_detection.box_coders import keypoint_box_coder
from object_detection.core import box_list
from object_detection.core import standard_fields as fields

class KeypointBoxCoderTest(tf.test.TestCase):

    def test_get_correct_relative_codes_after_encoding(self):
        boxes = [
         [
          10.0, 10.0, 20.0, 15.0],
         [
          0.2, 0.1, 0.5, 0.4]]
        keypoints = [[[15.0, 12.0], [10.0, 15.0]],
         [
          [
           0.5, 0.3], [0.2, 0.4]]]
        num_keypoints = len(keypoints[0])
        anchors = [[15.0, 12.0, 30.0, 18.0],
         [
          0.1, 0.0, 0.7, 0.9]]
        expected_rel_codes = [
         [
          -0.5, -0.416666, -0.405465, -0.182321,
          -0.5, -0.5, -0.833333, 0.0],
         [
          -0.083333, -0.222222, -0.693147, -1.098612,
          0.166667, -0.166667, -0.333333, -0.055556]]
        boxes = box_list.BoxList(tf.constant(boxes))
        boxes.add_field(fields.BoxListFields.keypoints, tf.constant(keypoints))
        anchors = box_list.BoxList(tf.constant(anchors))
        coder = keypoint_box_coder.KeypointBoxCoder(num_keypoints)
        rel_codes = coder.encode(boxes, anchors)
        with self.test_session() as (sess):
            rel_codes_out, = sess.run([rel_codes])
            self.assertAllClose(rel_codes_out, expected_rel_codes)

    def test_get_correct_relative_codes_after_encoding_with_scaling(self):
        boxes = [[10.0, 10.0, 20.0, 15.0],
         [
          0.2, 0.1, 0.5, 0.4]]
        keypoints = [[[15.0, 12.0], [10.0, 15.0]],
         [
          [
           0.5, 0.3], [0.2, 0.4]]]
        num_keypoints = len(keypoints[0])
        anchors = [[15.0, 12.0, 30.0, 18.0],
         [
          0.1, 0.0, 0.7, 0.9]]
        scale_factors = [2, 3, 4, 5]
        expected_rel_codes = [
         [
          -1.0, -1.25, -1.62186, -0.911608,
          -1.0, -1.5, -1.666667, 0.0],
         [
          -0.166667, -0.666667, -2.772588, -5.493062,
          0.333333, -0.5, -0.666667, -0.166667]]
        boxes = box_list.BoxList(tf.constant(boxes))
        boxes.add_field(fields.BoxListFields.keypoints, tf.constant(keypoints))
        anchors = box_list.BoxList(tf.constant(anchors))
        coder = keypoint_box_coder.KeypointBoxCoder(num_keypoints, scale_factors=scale_factors)
        rel_codes = coder.encode(boxes, anchors)
        with self.test_session() as (sess):
            rel_codes_out, = sess.run([rel_codes])
            self.assertAllClose(rel_codes_out, expected_rel_codes)

    def test_get_correct_boxes_after_decoding(self):
        anchors = [[15.0, 12.0, 30.0, 18.0],
         [
          0.1, 0.0, 0.7, 0.9]]
        rel_codes = [
         [
          -0.5, -0.416666, -0.405465, -0.182321,
          -0.5, -0.5, -0.833333, 0.0],
         [
          -0.083333, -0.222222, -0.693147, -1.098612,
          0.166667, -0.166667, -0.333333, -0.055556]]
        expected_boxes = [
         [
          10.0, 10.0, 20.0, 15.0],
         [
          0.2, 0.1, 0.5, 0.4]]
        expected_keypoints = [[[15.0, 12.0], [10.0, 15.0]],
         [
          [
           0.5, 0.3], [0.2, 0.4]]]
        num_keypoints = len(expected_keypoints[0])
        anchors = box_list.BoxList(tf.constant(anchors))
        coder = keypoint_box_coder.KeypointBoxCoder(num_keypoints)
        boxes = coder.decode(rel_codes, anchors)
        with self.test_session() as (sess):
            boxes_out, keypoints_out = sess.run([
             boxes.get(), boxes.get_field(fields.BoxListFields.keypoints)])
            self.assertAllClose(boxes_out, expected_boxes)
            self.assertAllClose(keypoints_out, expected_keypoints)

    def test_get_correct_boxes_after_decoding_with_scaling(self):
        anchors = [[15.0, 12.0, 30.0, 18.0],
         [
          0.1, 0.0, 0.7, 0.9]]
        rel_codes = [
         [
          -1.0, -1.25, -1.62186, -0.911608,
          -1.0, -1.5, -1.666667, 0.0],
         [
          -0.166667, -0.666667, -2.772588, -5.493062,
          0.333333, -0.5, -0.666667, -0.166667]]
        scale_factors = [
         2, 3, 4, 5]
        expected_boxes = [[10.0, 10.0, 20.0, 15.0],
         [
          0.2, 0.1, 0.5, 0.4]]
        expected_keypoints = [[[15.0, 12.0], [10.0, 15.0]],
         [
          [
           0.5, 0.3], [0.2, 0.4]]]
        num_keypoints = len(expected_keypoints[0])
        anchors = box_list.BoxList(tf.constant(anchors))
        coder = keypoint_box_coder.KeypointBoxCoder(num_keypoints, scale_factors=scale_factors)
        boxes = coder.decode(rel_codes, anchors)
        with self.test_session() as (sess):
            boxes_out, keypoints_out = sess.run([
             boxes.get(), boxes.get_field(fields.BoxListFields.keypoints)])
            self.assertAllClose(boxes_out, expected_boxes)
            self.assertAllClose(keypoints_out, expected_keypoints)

    def test_very_small_width_nan_after_encoding(self):
        boxes = [[10.0, 10.0, 10.0000001, 20.0]]
        keypoints = [[[10.0, 10.0], [10.0000001, 20.0]]]
        anchors = [[15.0, 12.0, 30.0, 18.0]]
        expected_rel_codes = [
         [-0.833333, 0.0, -21.128731, 0.510826,
          -0.833333, -0.833333, -0.833333, 0.833333]]
        boxes = box_list.BoxList(tf.constant(boxes))
        boxes.add_field(fields.BoxListFields.keypoints, tf.constant(keypoints))
        anchors = box_list.BoxList(tf.constant(anchors))
        coder = keypoint_box_coder.KeypointBoxCoder(2)
        rel_codes = coder.encode(boxes, anchors)
        with self.test_session() as (sess):
            rel_codes_out, = sess.run([rel_codes])
            self.assertAllClose(rel_codes_out, expected_rel_codes)


if __name__ == '__main__':
    tf.test.main()