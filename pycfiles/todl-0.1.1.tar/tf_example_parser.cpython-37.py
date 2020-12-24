# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/metrics/tf_example_parser.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 6280 bytes
"""Tensorflow Example proto parser for data loading.

A parser to decode data containing serialized tensorflow.Example
protos into materialized tensors (numpy arrays).
"""
import numpy as np
from object_detection.core import data_parser
import object_detection.core as fields

class FloatParser(data_parser.DataToNumpyParser):
    __doc__ = 'Tensorflow Example float parser.'

    def __init__(self, field_name):
        self.field_name = field_name

    def parse(self, tf_example):
        if tf_example.features.feature[self.field_name].HasField('float_list'):
            return np.array((tf_example.features.feature[self.field_name].float_list.value), dtype=(np.float)).transpose()


class StringParser(data_parser.DataToNumpyParser):
    __doc__ = 'Tensorflow Example string parser.'

    def __init__(self, field_name):
        self.field_name = field_name

    def parse(self, tf_example):
        if tf_example.features.feature[self.field_name].HasField('bytes_list'):
            return ''.join(tf_example.features.feature[self.field_name].bytes_list.value)


class Int64Parser(data_parser.DataToNumpyParser):
    __doc__ = 'Tensorflow Example int64 parser.'

    def __init__(self, field_name):
        self.field_name = field_name

    def parse(self, tf_example):
        if tf_example.features.feature[self.field_name].HasField('int64_list'):
            return np.array((tf_example.features.feature[self.field_name].int64_list.value), dtype=(np.int64)).transpose()


class BoundingBoxParser(data_parser.DataToNumpyParser):
    __doc__ = 'Tensorflow Example bounding box parser.'

    def __init__(self, xmin_field_name, ymin_field_name, xmax_field_name, ymax_field_name):
        self.field_names = [
         ymin_field_name, xmin_field_name, ymax_field_name, xmax_field_name]

    def parse(self, tf_example):
        result = []
        parsed = True
        for field_name in self.field_names:
            result.append(tf_example.features.feature[field_name].float_list.value)
            parsed &= tf_example.features.feature[field_name].HasField('float_list')

        if parsed:
            return np.array(result).transpose()


class TfExampleDetectionAndGTParser(data_parser.DataToNumpyParser):
    __doc__ = 'Tensorflow Example proto parser.'

    def __init__(self):
        self.items_to_handlers = {fields.DetectionResultFields.key: StringParser(fields.TfExampleFields.source_id), 
         
         fields.InputDataFields.groundtruth_boxes: BoundingBoxParser(fields.TfExampleFields.object_bbox_xmin, fields.TfExampleFields.object_bbox_ymin, fields.TfExampleFields.object_bbox_xmax, fields.TfExampleFields.object_bbox_ymax), 
         
         fields.InputDataFields.groundtruth_classes: Int64Parser(fields.TfExampleFields.object_class_label), 
         
         fields.DetectionResultFields.detection_boxes: BoundingBoxParser(fields.TfExampleFields.detection_bbox_xmin, fields.TfExampleFields.detection_bbox_ymin, fields.TfExampleFields.detection_bbox_xmax, fields.TfExampleFields.detection_bbox_ymax), 
         
         fields.DetectionResultFields.detection_classes: Int64Parser(fields.TfExampleFields.detection_class_label), 
         
         fields.DetectionResultFields.detection_scores: FloatParser(fields.TfExampleFields.detection_score)}
        self.optional_items_to_handlers = {fields.InputDataFields.groundtruth_difficult: Int64Parser(fields.TfExampleFields.object_difficult), 
         
         fields.InputDataFields.groundtruth_group_of: Int64Parser(fields.TfExampleFields.object_group_of), 
         
         fields.InputDataFields.groundtruth_image_classes: Int64Parser(fields.TfExampleFields.image_class_label)}

    def parse(self, tf_example):
        """Parses tensorflow example and returns a tensor dictionary.

    Args:
      tf_example: a tf.Example object.

    Returns:
      A dictionary of the following numpy arrays:
      fields.DetectionResultFields.source_id - string containing original image
      id.
      fields.InputDataFields.groundtruth_boxes - a numpy array containing
      groundtruth boxes.
      fields.InputDataFields.groundtruth_classes - a numpy array containing
      groundtruth classes.
      fields.InputDataFields.groundtruth_group_of - a numpy array containing
      groundtruth group of flag (optional, None if not specified).
      fields.InputDataFields.groundtruth_difficult - a numpy array containing
      groundtruth difficult flag (optional, None if not specified).
      fields.InputDataFields.groundtruth_image_classes - a numpy array
      containing groundtruth image-level labels.
      fields.DetectionResultFields.detection_boxes - a numpy array containing
      detection boxes.
      fields.DetectionResultFields.detection_classes - a numpy array containing
      detection class labels.
      fields.DetectionResultFields.detection_scores - a numpy array containing
      detection scores.
      Returns None if tf.Example was not parsed or non-optional fields were not
      found.
    """
        results_dict = {}
        parsed = True
        for key, parser in self.items_to_handlers.items():
            results_dict[key] = parser.parse(tf_example)
            parsed &= results_dict[key] is not None

        for key, parser in self.optional_items_to_handlers.items():
            results_dict[key] = parser.parse(tf_example)

        if parsed:
            return results_dict