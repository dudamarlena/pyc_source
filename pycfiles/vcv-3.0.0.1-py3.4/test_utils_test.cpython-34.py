# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/utils/test_utils_test.py
# Compiled at: 2018-06-15 01:29:01
# Size of source mod 2**32: 2678 bytes
"""Tests for object_detection.utils.test_utils."""
import numpy as np, tensorflow as tf
from object_detection.utils import test_utils

class TestUtilsTest(tf.test.TestCase):

    def test_diagonal_gradient_image(self):
        """Tests if a good pyramid image is created."""
        pyramid_image = test_utils.create_diagonal_gradient_image(3, 4, 2)
        expected_first_channel = np.array([[3, 2, 1, 0],
         [
          4, 3, 2, 1],
         [
          5, 4, 3, 2]], dtype=np.float32)
        self.assertAllEqual(np.squeeze(pyramid_image[:, :, 0]), expected_first_channel)
        expected_image = np.array([
         [[3, 30],
          [
           2, 20],
          [
           1, 10],
          [
           0, 0]],
         [
          [
           4, 40],
          [
           3, 30],
          [
           2, 20],
          [
           1, 10]],
         [
          [
           5, 50],
          [
           4, 40],
          [
           3, 30],
          [
           2, 20]]], dtype=np.float32)
        self.assertAllEqual(pyramid_image, expected_image)

    def test_random_boxes(self):
        """Tests if valid random boxes are created."""
        num_boxes = 1000
        max_height = 3
        max_width = 5
        boxes = test_utils.create_random_boxes(num_boxes, max_height, max_width)
        true_column = np.ones(shape=num_boxes) == 1
        self.assertAllEqual(boxes[:, 0] < boxes[:, 2], true_column)
        self.assertAllEqual(boxes[:, 1] < boxes[:, 3], true_column)
        self.assertTrue(boxes[:, 0].min() >= 0)
        self.assertTrue(boxes[:, 1].min() >= 0)
        self.assertTrue(boxes[:, 2].max() <= max_height)
        self.assertTrue(boxes[:, 3].max() <= max_width)


if __name__ == '__main__':
    tf.test.main()