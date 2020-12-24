# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/lstm_object_detection/metrics/coco_evaluation_all_frames.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 5494 bytes
"""Class for evaluating video object detections with COCO metrics."""
import tensorflow.compat.v1 as tf
from object_detection.core import standard_fields
from object_detection.metrics import coco_evaluation
from object_detection.metrics import coco_tools

class CocoEvaluationAllFrames(coco_evaluation.CocoDetectionEvaluator):
    __doc__ = 'Class to evaluate COCO detection metrics for frame sequences.\n\n  The class overrides two functions: add_single_ground_truth_image_info and\n  add_single_detected_image_info.\n\n  For the evaluation of sequence video detection, by iterating through the\n  entire groundtruth_dict, all the frames in the unrolled frames in one LSTM\n  training sample are considered. Therefore, both groundtruth and detection\n  results of all frames are added for the evaluation. This is used when all the\n  frames are labeled in the video object detection training job.\n  '

    def add_single_ground_truth_image_info(self, image_id, groundtruth_dict):
        """Add groundtruth results of all frames to the eval pipeline.

    This method overrides the function defined in the base class.

    Args:
      image_id: A unique string/integer identifier for the image.
      groundtruth_dict: A list of dictionary containing -
        InputDataFields.groundtruth_boxes: float32 numpy array of shape
          [num_boxes, 4] containing `num_boxes` groundtruth boxes of the format
          [ymin, xmin, ymax, xmax] in absolute image coordinates.
        InputDataFields.groundtruth_classes: integer numpy array of shape
          [num_boxes] containing 1-indexed groundtruth classes for the boxes.
        InputDataFields.groundtruth_is_crowd (optional): integer numpy array of
          shape [num_boxes] containing iscrowd flag for groundtruth boxes.
    """
        for idx, gt in enumerate(groundtruth_dict):
            if not gt:
                continue
            image_frame_id = '{}_{}'.format(image_id, idx)
            if image_frame_id in self._image_ids:
                tf.logging.warning('Ignoring ground truth with image id %s since it was previously added', image_frame_id)
                continue
            self._groundtruth_list.extend(coco_tools.ExportSingleImageGroundtruthToCoco(image_id=image_frame_id,
              next_annotation_id=(self._annotation_id),
              category_id_set=(self._category_id_set),
              groundtruth_boxes=(gt[standard_fields.InputDataFields.groundtruth_boxes]),
              groundtruth_classes=(gt[standard_fields.InputDataFields.groundtruth_classes])))
            self._annotation_id += gt[standard_fields.InputDataFields.groundtruth_boxes].shape[0]
            self._image_ids[image_frame_id] = False

    def add_single_detected_image_info(self, image_id, detections_dict):
        """Add detection results of all frames to the eval pipeline.

    This method overrides the function defined in the base class.

    Args:
      image_id: A unique string/integer identifier for the image.
      detections_dict: A list of dictionary containing -
        DetectionResultFields.detection_boxes: float32 numpy array of shape
          [num_boxes, 4] containing `num_boxes` detection boxes of the format
          [ymin, xmin, ymax, xmax] in absolute image coordinates.
        DetectionResultFields.detection_scores: float32 numpy array of shape
          [num_boxes] containing detection scores for the boxes.
        DetectionResultFields.detection_classes: integer numpy array of shape
          [num_boxes] containing 1-indexed detection classes for the boxes.

    Raises:
      ValueError: If groundtruth for the image_id is not available.
    """
        for idx, det in enumerate(detections_dict):
            if not det:
                continue
            image_frame_id = '{}_{}'.format(image_id, idx)
            if image_frame_id not in self._image_ids:
                raise ValueError('Missing groundtruth for image-frame id: {}'.format(image_frame_id))
            if self._image_ids[image_frame_id]:
                tf.logging.warning('Ignoring detection with image id %s since it was previously added', image_frame_id)
                continue
            self._detection_boxes_list.extend(coco_tools.ExportSingleImageDetectionBoxesToCoco(image_id=image_frame_id,
              category_id_set=(self._category_id_set),
              detection_boxes=(det[standard_fields.DetectionResultFields.detection_boxes]),
              detection_scores=(det[standard_fields.DetectionResultFields.detection_scores]),
              detection_classes=(det[standard_fields.DetectionResultFields.detection_classes])))
            self._image_ids[image_frame_id] = True