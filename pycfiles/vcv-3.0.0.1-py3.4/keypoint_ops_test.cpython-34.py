# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/core/keypoint_ops_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 5545 bytes
"""Tests for object_detection.core.keypoint_ops."""
import numpy as np, tensorflow as tf
from object_detection.core import keypoint_ops

class KeypointOpsTest(tf.test.TestCase):
    __doc__ = 'Tests for common keypoint operations.'

    def test_scale(self):
        keypoints = tf.constant([
         [
          [
           0.0, 0.0], [100.0, 200.0]],
         [
          [
           50.0, 120.0], [100.0, 140.0]]])
        y_scale = tf.constant(0.01)
        x_scale = tf.constant(0.005)
        expected_keypoints = tf.constant([
         [
          [
           0.0, 0.0], [1.0, 1.0]],
         [
          [
           0.5, 0.6], [1.0, 0.7]]])
        output = keypoint_ops.scale(keypoints, y_scale, x_scale)
        with self.test_session() as (sess):
            output_, expected_keypoints_ = sess.run([output, expected_keypoints])
            self.assertAllClose(output_, expected_keypoints_)

    def test_clip_to_window(self):
        keypoints = tf.constant([
         [
          [
           0.25, 0.5], [0.75, 0.75]],
         [
          [
           0.5, 0.0], [1.0, 1.0]]])
        window = tf.constant([0.25, 0.25, 0.75, 0.75])
        expected_keypoints = tf.constant([
         [
          [
           0.25, 0.5], [0.75, 0.75]],
         [
          [
           0.5, 0.25], [0.75, 0.75]]])
        output = keypoint_ops.clip_to_window(keypoints, window)
        with self.test_session() as (sess):
            output_, expected_keypoints_ = sess.run([output, expected_keypoints])
            self.assertAllClose(output_, expected_keypoints_)

    def test_prune_outside_window(self):
        keypoints = tf.constant([
         [
          [
           0.25, 0.5], [0.75, 0.75]],
         [
          [
           0.5, 0.0], [1.0, 1.0]]])
        window = tf.constant([0.25, 0.25, 0.75, 0.75])
        expected_keypoints = tf.constant([[[0.25, 0.5], [0.75, 0.75]],
         [
          [
           np.nan, np.nan], [np.nan, np.nan]]])
        output = keypoint_ops.prune_outside_window(keypoints, window)
        with self.test_session() as (sess):
            output_, expected_keypoints_ = sess.run([output, expected_keypoints])
            self.assertAllClose(output_, expected_keypoints_)

    def test_change_coordinate_frame(self):
        keypoints = tf.constant([
         [
          [
           0.25, 0.5], [0.75, 0.75]],
         [
          [
           0.5, 0.0], [1.0, 1.0]]])
        window = tf.constant([0.25, 0.25, 0.75, 0.75])
        expected_keypoints = tf.constant([
         [
          [
           0, 0.5], [1.0, 1.0]],
         [
          [
           0.5, -0.5], [1.5, 1.5]]])
        output = keypoint_ops.change_coordinate_frame(keypoints, window)
        with self.test_session() as (sess):
            output_, expected_keypoints_ = sess.run([output, expected_keypoints])
            self.assertAllClose(output_, expected_keypoints_)

    def test_to_normalized_coordinates(self):
        keypoints = tf.constant([
         [
          [
           10.0, 30.0], [30.0, 45.0]],
         [
          [
           20.0, 0.0], [40.0, 60.0]]])
        output = keypoint_ops.to_normalized_coordinates(keypoints, 40, 60)
        expected_keypoints = tf.constant([
         [
          [
           0.25, 0.5], [0.75, 0.75]],
         [
          [
           0.5, 0.0], [1.0, 1.0]]])
        with self.test_session() as (sess):
            output_, expected_keypoints_ = sess.run([output, expected_keypoints])
            self.assertAllClose(output_, expected_keypoints_)

    def test_to_normalized_coordinates_already_normalized(self):
        keypoints = tf.constant([
         [
          [
           0.25, 0.5], [0.75, 0.75]],
         [
          [
           0.5, 0.0], [1.0, 1.0]]])
        output = keypoint_ops.to_normalized_coordinates(keypoints, 40, 60)
        with self.test_session() as (sess):
            with self.assertRaisesOpError('assertion failed'):
                sess.run(output)

    def test_to_absolute_coordinates(self):
        keypoints = tf.constant([
         [
          [
           0.25, 0.5], [0.75, 0.75]],
         [
          [
           0.5, 0.0], [1.0, 1.0]]])
        output = keypoint_ops.to_absolute_coordinates(keypoints, 40, 60)
        expected_keypoints = tf.constant([
         [
          [
           10.0, 30.0], [30.0, 45.0]],
         [
          [
           20.0, 0.0], [40.0, 60.0]]])
        with self.test_session() as (sess):
            output_, expected_keypoints_ = sess.run([output, expected_keypoints])
            self.assertAllClose(output_, expected_keypoints_)

    def test_to_absolute_coordinates_already_absolute(self):
        keypoints = tf.constant([
         [
          [
           10.0, 30.0], [30.0, 45.0]],
         [
          [
           20.0, 0.0], [40.0, 60.0]]])
        output = keypoint_ops.to_absolute_coordinates(keypoints, 40, 60)
        with self.test_session() as (sess):
            with self.assertRaisesOpError('assertion failed'):
                sess.run(output)

    def test_flip_horizontal(self):
        keypoints = tf.constant([
         [
          [
           0.1, 0.1], [0.2, 0.2], [0.3, 0.3]],
         [
          [
           0.4, 0.4], [0.5, 0.5], [0.6, 0.6]]])
        flip_permutation = [
         0, 2, 1]
        expected_keypoints = tf.constant([
         [
          [
           0.1, 0.9], [0.3, 0.7], [0.2, 0.8]],
         [
          [
           0.4, 0.6], [0.6, 0.4], [0.5, 0.5]]])
        output = keypoint_ops.flip_horizontal(keypoints, 0.5, flip_permutation)
        with self.test_session() as (sess):
            output_, expected_keypoints_ = sess.run([output, expected_keypoints])
            self.assertAllClose(output_, expected_keypoints_)


if __name__ == '__main__':
    tf.test.main()