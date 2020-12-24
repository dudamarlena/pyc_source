# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/utils/visualization_utils_test.py
# Compiled at: 2018-06-15 01:29:00
# Size of source mod 2**32: 5624 bytes
"""Tests for image.understanding.object_detection.core.visualization_utils.

Testing with visualization in the following colab:
https://drive.google.com/a/google.com/file/d/0B5HnKS_hMsNARERpU3MtU3I5RFE/view?usp=sharing

"""
import numpy as np, PIL.Image as Image, tensorflow as tf
from object_detection.utils import visualization_utils

class VisualizationUtilsTest(tf.test.TestCase):

    def create_colorful_test_image(self):
        """This function creates an image that can be used to test vis functions.

    It makes an image composed of four colored rectangles.

    Returns:
      colorful test numpy array image.
    """
        ch255 = np.full([100, 200, 1], 255, dtype=np.uint8)
        ch128 = np.full([100, 200, 1], 128, dtype=np.uint8)
        ch0 = np.full([100, 200, 1], 0, dtype=np.uint8)
        imr = np.concatenate((ch255, ch128, ch128), axis=2)
        img = np.concatenate((ch255, ch255, ch0), axis=2)
        imb = np.concatenate((ch255, ch0, ch255), axis=2)
        imw = np.concatenate((ch128, ch128, ch128), axis=2)
        imu = np.concatenate((imr, img), axis=1)
        imd = np.concatenate((imb, imw), axis=1)
        image = np.concatenate((imu, imd), axis=0)
        return image

    def test_draw_bounding_box_on_image(self):
        test_image = self.create_colorful_test_image()
        test_image = Image.fromarray(test_image)
        width_original, height_original = test_image.size
        ymin = 0.25
        ymax = 0.75
        xmin = 0.4
        xmax = 0.6
        visualization_utils.draw_bounding_box_on_image(test_image, ymin, xmin, ymax, xmax)
        width_final, height_final = test_image.size
        self.assertEqual(width_original, width_final)
        self.assertEqual(height_original, height_final)

    def test_draw_bounding_box_on_image_array(self):
        test_image = self.create_colorful_test_image()
        width_original = test_image.shape[0]
        height_original = test_image.shape[1]
        ymin = 0.25
        ymax = 0.75
        xmin = 0.4
        xmax = 0.6
        visualization_utils.draw_bounding_box_on_image_array(test_image, ymin, xmin, ymax, xmax)
        width_final = test_image.shape[0]
        height_final = test_image.shape[1]
        self.assertEqual(width_original, width_final)
        self.assertEqual(height_original, height_final)

    def test_draw_bounding_boxes_on_image(self):
        test_image = self.create_colorful_test_image()
        test_image = Image.fromarray(test_image)
        width_original, height_original = test_image.size
        boxes = np.array([[0.25, 0.75, 0.4, 0.6],
         [
          0.1, 0.1, 0.9, 0.9]])
        visualization_utils.draw_bounding_boxes_on_image(test_image, boxes)
        width_final, height_final = test_image.size
        self.assertEqual(width_original, width_final)
        self.assertEqual(height_original, height_final)

    def test_draw_bounding_boxes_on_image_array(self):
        test_image = self.create_colorful_test_image()
        width_original = test_image.shape[0]
        height_original = test_image.shape[1]
        boxes = np.array([[0.25, 0.75, 0.4, 0.6],
         [
          0.1, 0.1, 0.9, 0.9]])
        visualization_utils.draw_bounding_boxes_on_image_array(test_image, boxes)
        width_final = test_image.shape[0]
        height_final = test_image.shape[1]
        self.assertEqual(width_original, width_final)
        self.assertEqual(height_original, height_final)

    def test_draw_keypoints_on_image(self):
        test_image = self.create_colorful_test_image()
        test_image = Image.fromarray(test_image)
        width_original, height_original = test_image.size
        keypoints = [[0.25, 0.75], [0.4, 0.6], [0.1, 0.1], [0.9, 0.9]]
        visualization_utils.draw_keypoints_on_image(test_image, keypoints)
        width_final, height_final = test_image.size
        self.assertEqual(width_original, width_final)
        self.assertEqual(height_original, height_final)

    def test_draw_keypoints_on_image_array(self):
        test_image = self.create_colorful_test_image()
        width_original = test_image.shape[0]
        height_original = test_image.shape[1]
        keypoints = [[0.25, 0.75], [0.4, 0.6], [0.1, 0.1], [0.9, 0.9]]
        visualization_utils.draw_keypoints_on_image_array(test_image, keypoints)
        width_final = test_image.shape[0]
        height_final = test_image.shape[1]
        self.assertEqual(width_original, width_final)
        self.assertEqual(height_original, height_final)

    def test_draw_mask_on_image_array(self):
        test_image = np.asarray([[[0, 0, 0], [0, 0, 0]],
         [
          [
           0, 0, 0], [0, 0, 0]]], dtype=np.uint8)
        mask = np.asarray([[0.0, 1.0],
         [
          1.0, 1.0]], dtype=np.float32)
        expected_result = np.asarray([[[0, 0, 0], [0, 0, 127]],
         [
          [
           0, 0, 127], [0, 0, 127]]], dtype=np.uint8)
        visualization_utils.draw_mask_on_image_array(test_image, mask, color='Blue', alpha=0.5)
        self.assertAllEqual(test_image, expected_result)


if __name__ == '__main__':
    tf.test.main()