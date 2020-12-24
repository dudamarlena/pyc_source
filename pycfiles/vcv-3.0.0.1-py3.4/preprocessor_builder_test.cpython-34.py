# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/builders/preprocessor_builder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 16634 bytes
"""Tests for preprocessor_builder."""
import tensorflow as tf
from google.protobuf import text_format
from object_detection.builders import preprocessor_builder
from object_detection.core import preprocessor
from object_detection.protos import preprocessor_pb2

class PreprocessorBuilderTest(tf.test.TestCase):

    def assert_dictionary_close(self, dict1, dict2):
        """Helper to check if two dicts with floatst or integers are close."""
        self.assertEqual(sorted(dict1.keys()), sorted(dict2.keys()))
        for key in dict1:
            value = dict1[key]
            if isinstance(value, float):
                self.assertAlmostEqual(value, dict2[key])
            else:
                self.assertEqual(value, dict2[key])

    def test_build_normalize_image(self):
        preprocessor_text_proto = '\n    normalize_image {\n      original_minval: 0.0\n      original_maxval: 255.0\n      target_minval: -1.0\n      target_maxval: 1.0\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.normalize_image)
        self.assertEqual(args, {'original_minval': 0.0, 
         'original_maxval': 255.0, 
         'target_minval': -1.0, 
         'target_maxval': 1.0})

    def test_build_random_horizontal_flip(self):
        preprocessor_text_proto = '\n    random_horizontal_flip {\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_horizontal_flip)
        self.assertEqual(args, {})

    def test_build_random_pixel_value_scale(self):
        preprocessor_text_proto = '\n    random_pixel_value_scale {\n      minval: 0.8\n      maxval: 1.2\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_pixel_value_scale)
        self.assert_dictionary_close(args, {'minval': 0.8,  'maxval': 1.2})

    def test_build_random_image_scale(self):
        preprocessor_text_proto = '\n    random_image_scale {\n      min_scale_ratio: 0.8\n      max_scale_ratio: 2.2\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_image_scale)
        self.assert_dictionary_close(args, {'min_scale_ratio': 0.8,  'max_scale_ratio': 2.2})

    def test_build_random_rgb_to_gray(self):
        preprocessor_text_proto = '\n    random_rgb_to_gray {\n      probability: 0.8\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_rgb_to_gray)
        self.assert_dictionary_close(args, {'probability': 0.8})

    def test_build_random_adjust_brightness(self):
        preprocessor_text_proto = '\n    random_adjust_brightness {\n      max_delta: 0.2\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_adjust_brightness)
        self.assert_dictionary_close(args, {'max_delta': 0.2})

    def test_build_random_adjust_contrast(self):
        preprocessor_text_proto = '\n    random_adjust_contrast {\n      min_delta: 0.7\n      max_delta: 1.1\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_adjust_contrast)
        self.assert_dictionary_close(args, {'min_delta': 0.7,  'max_delta': 1.1})

    def test_build_random_adjust_hue(self):
        preprocessor_text_proto = '\n    random_adjust_hue {\n      max_delta: 0.01\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_adjust_hue)
        self.assert_dictionary_close(args, {'max_delta': 0.01})

    def test_build_random_adjust_saturation(self):
        preprocessor_text_proto = '\n    random_adjust_saturation {\n      min_delta: 0.75\n      max_delta: 1.15\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_adjust_saturation)
        self.assert_dictionary_close(args, {'min_delta': 0.75,  'max_delta': 1.15})

    def test_build_random_distort_color(self):
        preprocessor_text_proto = '\n    random_distort_color {\n      color_ordering: 1\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_distort_color)
        self.assertEqual(args, {'color_ordering': 1})

    def test_build_random_jitter_boxes(self):
        preprocessor_text_proto = '\n    random_jitter_boxes {\n      ratio: 0.1\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_jitter_boxes)
        self.assert_dictionary_close(args, {'ratio': 0.1})

    def test_build_random_crop_image(self):
        preprocessor_text_proto = '\n    random_crop_image {\n      min_object_covered: 0.75\n      min_aspect_ratio: 0.75\n      max_aspect_ratio: 1.5\n      min_area: 0.25\n      max_area: 0.875\n      overlap_thresh: 0.5\n      random_coef: 0.125\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_crop_image)
        self.assertEqual(args, {'min_object_covered': 0.75, 
         'aspect_ratio_range': (0.75, 1.5), 
         'area_range': (0.25, 0.875), 
         'overlap_thresh': 0.5, 
         'random_coef': 0.125})

    def test_build_random_pad_image(self):
        preprocessor_text_proto = '\n    random_pad_image {\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_pad_image)
        self.assertEqual(args, {'min_image_size': None, 
         'max_image_size': None, 
         'pad_color': None})

    def test_build_random_crop_pad_image(self):
        preprocessor_text_proto = '\n    random_crop_pad_image {\n      min_object_covered: 0.75\n      min_aspect_ratio: 0.75\n      max_aspect_ratio: 1.5\n      min_area: 0.25\n      max_area: 0.875\n      overlap_thresh: 0.5\n      random_coef: 0.125\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_crop_pad_image)
        self.assertEqual(args, {'min_object_covered': 0.75, 
         'aspect_ratio_range': (0.75, 1.5), 
         'area_range': (0.25, 0.875), 
         'overlap_thresh': 0.5, 
         'random_coef': 0.125, 
         'min_padded_size_ratio': None, 
         'max_padded_size_ratio': None, 
         'pad_color': None})

    def test_build_random_crop_to_aspect_ratio(self):
        preprocessor_text_proto = '\n    random_crop_to_aspect_ratio {\n      aspect_ratio: 0.85\n      overlap_thresh: 0.35\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_crop_to_aspect_ratio)
        self.assert_dictionary_close(args, {'aspect_ratio': 0.85,  'overlap_thresh': 0.35})

    def test_build_random_black_patches(self):
        preprocessor_text_proto = '\n    random_black_patches {\n      max_black_patches: 20\n      probability: 0.95\n      size_to_image_ratio: 0.12\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_black_patches)
        self.assert_dictionary_close(args, {'max_black_patches': 20,  'probability': 0.95, 
         'size_to_image_ratio': 0.12})

    def test_build_random_resize_method(self):
        preprocessor_text_proto = '\n    random_resize_method {\n      target_height: 75\n      target_width: 100\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.random_resize_method)
        self.assert_dictionary_close(args, {'target_size': [75, 100]})

    def test_build_scale_boxes_to_pixel_coordinates(self):
        preprocessor_text_proto = '\n    scale_boxes_to_pixel_coordinates {}\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.scale_boxes_to_pixel_coordinates)
        self.assertEqual(args, {})

    def test_build_resize_image(self):
        preprocessor_text_proto = '\n    resize_image {\n      new_height: 75\n      new_width: 100\n      method: BICUBIC\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.resize_image)
        self.assertEqual(args, {'new_height': 75,  'new_width': 100, 
         'method': tf.image.ResizeMethod.BICUBIC})

    def test_build_subtract_channel_mean(self):
        preprocessor_text_proto = '\n    subtract_channel_mean {\n      means: [1.0, 2.0, 3.0]\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.subtract_channel_mean)
        self.assertEqual(args, {'means': [1.0, 2.0, 3.0]})

    def test_build_ssd_random_crop(self):
        preprocessor_text_proto = '\n    ssd_random_crop {\n      operations {\n        min_object_covered: 0.0\n        min_aspect_ratio: 0.875\n        max_aspect_ratio: 1.125\n        min_area: 0.5\n        max_area: 1.0\n        overlap_thresh: 0.0\n        random_coef: 0.375\n      }\n      operations {\n        min_object_covered: 0.25\n        min_aspect_ratio: 0.75\n        max_aspect_ratio: 1.5\n        min_area: 0.5\n        max_area: 1.0\n        overlap_thresh: 0.25\n        random_coef: 0.375\n      }\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.ssd_random_crop)
        self.assertEqual(args, {'min_object_covered': [0.0, 0.25],  'aspect_ratio_range': [
                                (0.875, 1.125), (0.75, 1.5)], 
         'area_range': [
                        (0.5, 1.0), (0.5, 1.0)], 
         'overlap_thresh': [
                            0.0, 0.25], 
         'random_coef': [
                         0.375, 0.375]})

    def test_build_ssd_random_crop_empty_operations(self):
        preprocessor_text_proto = '\n    ssd_random_crop {\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.ssd_random_crop)
        self.assertEqual(args, {})

    def test_build_ssd_random_crop_pad(self):
        preprocessor_text_proto = '\n    ssd_random_crop_pad {\n      operations {\n        min_object_covered: 0.0\n        min_aspect_ratio: 0.875\n        max_aspect_ratio: 1.125\n        min_area: 0.5\n        max_area: 1.0\n        overlap_thresh: 0.0\n        random_coef: 0.375\n        min_padded_size_ratio: [0.0, 0.0]\n        max_padded_size_ratio: [2.0, 2.0]\n        pad_color_r: 0.5\n        pad_color_g: 0.5\n        pad_color_b: 0.5\n      }\n      operations {\n        min_object_covered: 0.25\n        min_aspect_ratio: 0.75\n        max_aspect_ratio: 1.5\n        min_area: 0.5\n        max_area: 1.0\n        overlap_thresh: 0.25\n        random_coef: 0.375\n        min_padded_size_ratio: [0.0, 0.0]\n        max_padded_size_ratio: [2.0, 2.0]\n        pad_color_r: 0.5\n        pad_color_g: 0.5\n        pad_color_b: 0.5\n      }\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.ssd_random_crop_pad)
        self.assertEqual(args, {'min_object_covered': [0.0, 0.25],  'aspect_ratio_range': [
                                (0.875, 1.125), (0.75, 1.5)], 
         'area_range': [
                        (0.5, 1.0), (0.5, 1.0)], 
         'overlap_thresh': [
                            0.0, 0.25], 
         'random_coef': [
                         0.375, 0.375], 
         'min_padded_size_ratio': [
                                   (0.0, 0.0), (0.0, 0.0)], 
         'max_padded_size_ratio': [
                                   (2.0, 2.0), (2.0, 2.0)], 
         'pad_color': [
                       (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)]})

    def test_build_ssd_random_crop_fixed_aspect_ratio(self):
        preprocessor_text_proto = '\n    ssd_random_crop_fixed_aspect_ratio {\n      operations {\n        min_object_covered: 0.0\n        min_area: 0.5\n        max_area: 1.0\n        overlap_thresh: 0.0\n        random_coef: 0.375\n      }\n      operations {\n        min_object_covered: 0.25\n        min_area: 0.5\n        max_area: 1.0\n        overlap_thresh: 0.25\n        random_coef: 0.375\n      }\n      aspect_ratio: 0.875\n    }\n    '
        preprocessor_proto = preprocessor_pb2.PreprocessingStep()
        text_format.Merge(preprocessor_text_proto, preprocessor_proto)
        function, args = preprocessor_builder.build(preprocessor_proto)
        self.assertEqual(function, preprocessor.ssd_random_crop_fixed_aspect_ratio)
        self.assertEqual(args, {'min_object_covered': [0.0, 0.25],  'aspect_ratio': 0.875, 
         'area_range': [
                        (0.5, 1.0), (0.5, 1.0)], 
         'overlap_thresh': [
                            0.0, 0.25], 
         'random_coef': [
                         0.375, 0.375]})


if __name__ == '__main__':
    tf.test.main()