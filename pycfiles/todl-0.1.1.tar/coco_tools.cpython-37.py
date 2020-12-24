# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/metrics/coco_tools.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 37864 bytes
"""Wrappers for third party pycocotools to be used within object_detection.

Note that nothing in this file is tensorflow related and thus cannot
be called directly as a slim metric, for example.

TODO(jonathanhuang): wrap as a slim metric in metrics.py

Usage example: given a set of images with ids in the list image_ids
and corresponding lists of numpy arrays encoding groundtruth (boxes and classes)
and detections (boxes, scores and classes), where elements of each list
correspond to detections/annotations of a single image,
then evaluation (in multi-class mode) can be invoked as follows:

  groundtruth_dict = coco_tools.ExportGroundtruthToCOCO(
      image_ids, groundtruth_boxes_list, groundtruth_classes_list,
      max_num_classes, output_path=None)
  detections_list = coco_tools.ExportDetectionsToCOCO(
      image_ids, detection_boxes_list, detection_scores_list,
      detection_classes_list, output_path=None)
  groundtruth = coco_tools.COCOWrapper(groundtruth_dict)
  detections = groundtruth.LoadAnnotations(detections_list)
  evaluator = coco_tools.COCOEvalWrapper(groundtruth, detections,
                                         agnostic_mode=False)
  metrics = evaluator.ComputeMetrics()

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import OrderedDict
import copy, time, numpy as np
from pycocotools import coco
from pycocotools import cocoeval
from pycocotools import mask
from six.moves import range
from six.moves import zip
import tensorflow as tf
from object_detection.utils import json_utils

class COCOWrapper(coco.COCO):
    __doc__ = 'Wrapper for the pycocotools COCO class.'

    def __init__(self, dataset, detection_type='bbox'):
        """COCOWrapper constructor.

    See http://mscoco.org/dataset/#format for a description of the format.
    By default, the coco.COCO class constructor reads from a JSON file.
    This function duplicates the same behavior but loads from a dictionary,
    allowing us to perform evaluation without writing to external storage.

    Args:
      dataset: a dictionary holding bounding box annotations in the COCO format.
      detection_type: type of detections being wrapped. Can be one of ['bbox',
        'segmentation']

    Raises:
      ValueError: if detection_type is unsupported.
    """
        supported_detection_types = [
         'bbox', 'segmentation']
        if detection_type not in supported_detection_types:
            raise ValueError('Unsupported detection type: {}. Supported values are: {}'.format(detection_type, supported_detection_types))
        self._detection_type = detection_type
        coco.COCO.__init__(self)
        self.dataset = dataset
        self.createIndex()

    def LoadAnnotations(self, annotations):
        """Load annotations dictionary into COCO datastructure.

    See http://mscoco.org/dataset/#format for a description of the annotations
    format.  As above, this function replicates the default behavior of the API
    but does not require writing to external storage.

    Args:
      annotations: python list holding object detection results where each
        detection is encoded as a dict with required keys ['image_id',
        'category_id', 'score'] and one of ['bbox', 'segmentation'] based on
        `detection_type`.

    Returns:
      a coco.COCO datastructure holding object detection annotations results

    Raises:
      ValueError: if annotations is not a list
      ValueError: if annotations do not correspond to the images contained
        in self.
    """
        results = coco.COCO()
        results.dataset['images'] = [img for img in self.dataset['images']]
        tf.logging.info('Loading and preparing annotation results...')
        tic = time.time()
        if not isinstance(annotations, list):
            raise ValueError('annotations is not a list of objects')
        annotation_img_ids = [ann['image_id'] for ann in annotations]
        if set(annotation_img_ids) != set(annotation_img_ids) & set(self.getImgIds()):
            raise ValueError('Results do not correspond to current coco set')
        results.dataset['categories'] = copy.deepcopy(self.dataset['categories'])
        if self._detection_type == 'bbox':
            for idx, ann in enumerate(annotations):
                bb = ann['bbox']
                ann['area'] = bb[2] * bb[3]
                ann['id'] = idx + 1
                ann['iscrowd'] = 0

        else:
            if self._detection_type == 'segmentation':
                for idx, ann in enumerate(annotations):
                    ann['area'] = mask.area(ann['segmentation'])
                    ann['bbox'] = mask.toBbox(ann['segmentation'])
                    ann['id'] = idx + 1
                    ann['iscrowd'] = 0

        tf.logging.info('DONE (t=%0.2fs)', time.time() - tic)
        results.dataset['annotations'] = annotations
        results.createIndex()
        return results


class COCOEvalWrapper(cocoeval.COCOeval):
    __doc__ = 'Wrapper for the pycocotools COCOeval class.\n\n  To evaluate, create two objects (groundtruth_dict and detections_list)\n  using the conventions listed at http://mscoco.org/dataset/#format.\n  Then call evaluation as follows:\n\n    groundtruth = coco_tools.COCOWrapper(groundtruth_dict)\n    detections = groundtruth.LoadAnnotations(detections_list)\n    evaluator = coco_tools.COCOEvalWrapper(groundtruth, detections,\n                                           agnostic_mode=False)\n\n    metrics = evaluator.ComputeMetrics()\n  '

    def __init__(self, groundtruth=None, detections=None, agnostic_mode=False, iou_type='bbox'):
        """COCOEvalWrapper constructor.

    Note that for the area-based metrics to be meaningful, detection and
    groundtruth boxes must be in image coordinates measured in pixels.

    Args:
      groundtruth: a coco.COCO (or coco_tools.COCOWrapper) object holding
        groundtruth annotations
      detections: a coco.COCO (or coco_tools.COCOWrapper) object holding
        detections
      agnostic_mode: boolean (default: False).  If True, evaluation ignores
        class labels, treating all detections as proposals.
      iou_type: IOU type to use for evaluation. Supports `bbox` or `segm`.
    """
        cocoeval.COCOeval.__init__(self, groundtruth, detections, iouType=iou_type)
        if agnostic_mode:
            self.params.useCats = 0

    def GetCategory(self, category_id):
        """Fetches dictionary holding category information given category id.

    Args:
      category_id: integer id
    Returns:
      dictionary holding 'id', 'name'.
    """
        return self.cocoGt.cats[category_id]

    def GetAgnosticMode(self):
        """Returns true if COCO Eval is configured to evaluate in agnostic mode."""
        return self.params.useCats == 0

    def GetCategoryIdList(self):
        """Returns list of valid category ids."""
        return self.params.catIds

    def ComputeMetrics(self, include_metrics_per_category=False, all_metrics_per_category=False):
        """Computes detection metrics.

    Args:
      include_metrics_per_category: If True, will include metrics per category.
      all_metrics_per_category: If true, include all the summery metrics for
        each category in per_category_ap. Be careful with setting it to true if
        you have more than handful of categories, because it will pollute
        your mldash.

    Returns:
      1. summary_metrics: a dictionary holding:
        'Precision/mAP': mean average precision over classes averaged over IOU
          thresholds ranging from .5 to .95 with .05 increments
        'Precision/mAP@.50IOU': mean average precision at 50% IOU
        'Precision/mAP@.75IOU': mean average precision at 75% IOU
        'Precision/mAP (small)': mean average precision for small objects
                        (area < 32^2 pixels)
        'Precision/mAP (medium)': mean average precision for medium sized
                        objects (32^2 pixels < area < 96^2 pixels)
        'Precision/mAP (large)': mean average precision for large objects
                        (96^2 pixels < area < 10000^2 pixels)
        'Recall/AR@1': average recall with 1 detection
        'Recall/AR@10': average recall with 10 detections
        'Recall/AR@100': average recall with 100 detections
        'Recall/AR@100 (small)': average recall for small objects with 100
          detections
        'Recall/AR@100 (medium)': average recall for medium objects with 100
          detections
        'Recall/AR@100 (large)': average recall for large objects with 100
          detections
      2. per_category_ap: a dictionary holding category specific results with
        keys of the form: 'Precision mAP ByCategory/category'
        (without the supercategory part if no supercategories exist).
        For backward compatibility 'PerformanceByCategory' is included in the
        output regardless of all_metrics_per_category.
        If evaluating class-agnostic mode, per_category_ap is an empty
        dictionary.

    Raises:
      ValueError: If category_stats does not exist.
    """
        self.evaluate()
        self.accumulate()
        self.summarize()
        summary_metrics = OrderedDict([
         (
          'Precision/mAP', self.stats[0]),
         (
          'Precision/mAP@.50IOU', self.stats[1]),
         (
          'Precision/mAP@.75IOU', self.stats[2]),
         (
          'Precision/mAP (small)', self.stats[3]),
         (
          'Precision/mAP (medium)', self.stats[4]),
         (
          'Precision/mAP (large)', self.stats[5]),
         (
          'Recall/AR@1', self.stats[6]),
         (
          'Recall/AR@10', self.stats[7]),
         (
          'Recall/AR@100', self.stats[8]),
         (
          'Recall/AR@100 (small)', self.stats[9]),
         (
          'Recall/AR@100 (medium)', self.stats[10]),
         (
          'Recall/AR@100 (large)', self.stats[11])])
        if not include_metrics_per_category:
            return (
             summary_metrics, {})
        if not hasattr(self, 'category_stats'):
            raise ValueError('Category stats do not exist')
        per_category_ap = OrderedDict([])
        if self.GetAgnosticMode():
            return (
             summary_metrics, per_category_ap)
        for category_index, category_id in enumerate(self.GetCategoryIdList()):
            category = self.GetCategory(category_id)['name']
            per_category_ap['PerformanceByCategory/mAP/{}'.format(category)] = self.category_stats[0][category_index]
            if all_metrics_per_category:
                per_category_ap['Precision mAP ByCategory/{}'.format(category)] = self.category_stats[0][category_index]
                per_category_ap['Precision mAP@.50IOU ByCategory/{}'.format(category)] = self.category_stats[1][category_index]
                per_category_ap['Precision mAP@.75IOU ByCategory/{}'.format(category)] = self.category_stats[2][category_index]
                per_category_ap['Precision mAP (small) ByCategory/{}'.format(category)] = self.category_stats[3][category_index]
                per_category_ap['Precision mAP (medium) ByCategory/{}'.format(category)] = self.category_stats[4][category_index]
                per_category_ap['Precision mAP (large) ByCategory/{}'.format(category)] = self.category_stats[5][category_index]
                per_category_ap['Recall AR@1 ByCategory/{}'.format(category)] = self.category_stats[6][category_index]
                per_category_ap['Recall AR@10 ByCategory/{}'.format(category)] = self.category_stats[7][category_index]
                per_category_ap['Recall AR@100 ByCategory/{}'.format(category)] = self.category_stats[8][category_index]
                per_category_ap['Recall AR@100 (small) ByCategory/{}'.format(category)] = self.category_stats[9][category_index]
                per_category_ap['Recall AR@100 (medium) ByCategory/{}'.format(category)] = self.category_stats[10][category_index]
                per_category_ap['Recall AR@100 (large) ByCategory/{}'.format(category)] = self.category_stats[11][category_index]

        return (
         summary_metrics, per_category_ap)


def _ConvertBoxToCOCOFormat(box):
    """Converts a box in [ymin, xmin, ymax, xmax] format to COCO format.

  This is a utility function for converting from our internal
  [ymin, xmin, ymax, xmax] convention to the convention used by the COCO API
  i.e., [xmin, ymin, width, height].

  Args:
    box: a [ymin, xmin, ymax, xmax] numpy array

  Returns:
    a list of floats representing [xmin, ymin, width, height]
  """
    return [
     float(box[1]), float(box[0]), float(box[3] - box[1]),
     float(box[2] - box[0])]


def _RleCompress(masks):
    """Compresses mask using Run-length encoding provided by pycocotools.

  Args:
    masks: uint8 numpy array of shape [mask_height, mask_width] with values in
    {0, 1}.

  Returns:
    A pycocotools Run-length encoding of the mask.
  """
    return mask.encode(np.asfortranarray(masks))


def ExportSingleImageGroundtruthToCoco(image_id, next_annotation_id, category_id_set, groundtruth_boxes, groundtruth_classes, groundtruth_masks=None, groundtruth_is_crowd=None):
    """Export groundtruth of a single image to COCO format.

  This function converts groundtruth detection annotations represented as numpy
  arrays to dictionaries that can be ingested by the COCO evaluation API. Note
  that the image_ids provided here must match the ones given to
  ExportSingleImageDetectionsToCoco. We assume that boxes and classes are in
  correspondence - that is: groundtruth_boxes[i, :], and
  groundtruth_classes[i] are associated with the same groundtruth annotation.

  In the exported result, "area" fields are always set to the area of the
  groundtruth bounding box.

  Args:
    image_id: a unique image identifier either of type integer or string.
    next_annotation_id: integer specifying the first id to use for the
      groundtruth annotations. All annotations are assigned a continuous integer
      id starting from this value.
    category_id_set: A set of valid class ids. Groundtruth with classes not in
      category_id_set are dropped.
    groundtruth_boxes: numpy array (float32) with shape [num_gt_boxes, 4]
    groundtruth_classes: numpy array (int) with shape [num_gt_boxes]
    groundtruth_masks: optional uint8 numpy array of shape [num_detections,
      image_height, image_width] containing detection_masks.
    groundtruth_is_crowd: optional numpy array (int) with shape [num_gt_boxes]
      indicating whether groundtruth boxes are crowd.

  Returns:
    a list of groundtruth annotations for a single image in the COCO format.

  Raises:
    ValueError: if (1) groundtruth_boxes and groundtruth_classes do not have the
      right lengths or (2) if each of the elements inside these lists do not
      have the correct shapes or (3) if image_ids are not integers
  """
    if len(groundtruth_classes.shape) != 1:
        raise ValueError('groundtruth_classes is expected to be of rank 1.')
    else:
        if len(groundtruth_boxes.shape) != 2:
            raise ValueError('groundtruth_boxes is expected to be of rank 2.')
        if groundtruth_boxes.shape[1] != 4:
            raise ValueError('groundtruth_boxes should have shape[1] == 4.')
        num_boxes = groundtruth_classes.shape[0]
        if num_boxes != groundtruth_boxes.shape[0]:
            raise ValueError('Corresponding entries in groundtruth_classes, and groundtruth_boxes should have compatible shapes (i.e., agree on the 0th dimension).Classes shape: %d. Boxes shape: %d. Image ID: %s' % (
             groundtruth_classes.shape[0],
             groundtruth_boxes.shape[0], image_id))
        has_is_crowd = groundtruth_is_crowd is not None
        if has_is_crowd and len(groundtruth_is_crowd.shape) != 1:
            raise ValueError('groundtruth_is_crowd is expected to be of rank 1.')
    groundtruth_list = []
    for i in range(num_boxes):
        if groundtruth_classes[i] in category_id_set:
            iscrowd = groundtruth_is_crowd[i] if has_is_crowd else 0
            export_dict = {'id':next_annotation_id + i, 
             'image_id':image_id, 
             'category_id':int(groundtruth_classes[i]), 
             'bbox':list(_ConvertBoxToCOCOFormat(groundtruth_boxes[i, :])), 
             'area':float((groundtruth_boxes[(i, 2)] - groundtruth_boxes[(i, 0)]) * (groundtruth_boxes[(i, 3)] - groundtruth_boxes[(i, 1)])), 
             'iscrowd':iscrowd}
            if groundtruth_masks is not None:
                export_dict['segmentation'] = _RleCompress(groundtruth_masks[i])
            groundtruth_list.append(export_dict)

    return groundtruth_list


def ExportGroundtruthToCOCO(image_ids, groundtruth_boxes, groundtruth_classes, categories, output_path=None):
    """Export groundtruth detection annotations in numpy arrays to COCO API.

  This function converts a set of groundtruth detection annotations represented
  as numpy arrays to dictionaries that can be ingested by the COCO API.
  Inputs to this function are three lists: image ids for each groundtruth image,
  groundtruth boxes for each image and groundtruth classes respectively.
  Note that the image_ids provided here must match the ones given to the
  ExportDetectionsToCOCO function in order for evaluation to work properly.
  We assume that for each image, boxes, scores and classes are in
  correspondence --- that is: image_id[i], groundtruth_boxes[i, :] and
  groundtruth_classes[i] are associated with the same groundtruth annotation.

  In the exported result, "area" fields are always set to the area of the
  groundtruth bounding box and "iscrowd" fields are always set to 0.
  TODO(jonathanhuang): pass in "iscrowd" array for evaluating on COCO dataset.

  Args:
    image_ids: a list of unique image identifier either of type integer or
      string.
    groundtruth_boxes: list of numpy arrays with shape [num_gt_boxes, 4]
      (note that num_gt_boxes can be different for each entry in the list)
    groundtruth_classes: list of numpy arrays (int) with shape [num_gt_boxes]
      (note that num_gt_boxes can be different for each entry in the list)
    categories: a list of dictionaries representing all possible categories.
        Each dict in this list has the following keys:
          'id': (required) an integer id uniquely identifying this category
          'name': (required) string representing category name
            e.g., 'cat', 'dog', 'pizza'
          'supercategory': (optional) string representing the supercategory
            e.g., 'animal', 'vehicle', 'food', etc
    output_path: (optional) path for exporting result to JSON
  Returns:
    dictionary that can be read by COCO API
  Raises:
    ValueError: if (1) groundtruth_boxes and groundtruth_classes do not have the
      right lengths or (2) if each of the elements inside these lists do not
      have the correct shapes or (3) if image_ids are not integers
  """
    category_id_set = set([cat['id'] for cat in categories])
    groundtruth_export_list = []
    image_export_list = []
    if not len(image_ids) == len(groundtruth_boxes) == len(groundtruth_classes):
        raise ValueError('Input lists must have the same length')
    annotation_id = 1
    for image_id, boxes, classes in zip(image_ids, groundtruth_boxes, groundtruth_classes):
        image_export_list.append({'id': image_id})
        groundtruth_export_list.extend(ExportSingleImageGroundtruthToCoco(image_id, annotation_id, category_id_set, boxes, classes))
        num_boxes = classes.shape[0]
        annotation_id += num_boxes

    groundtruth_dict = {'annotations':groundtruth_export_list, 
     'images':image_export_list, 
     'categories':categories}
    if output_path:
        with tf.gfile.GFile(output_path, 'w') as (fid):
            json_utils.Dump(groundtruth_dict, fid, float_digits=4, indent=2)
    return groundtruth_dict


def ExportSingleImageDetectionBoxesToCoco(image_id, category_id_set, detection_boxes, detection_scores, detection_classes):
    """Export detections of a single image to COCO format.

  This function converts detections represented as numpy arrays to dictionaries
  that can be ingested by the COCO evaluation API. Note that the image_ids
  provided here must match the ones given to the
  ExporSingleImageDetectionBoxesToCoco. We assume that boxes, and classes are in
  correspondence - that is: boxes[i, :], and classes[i]
  are associated with the same groundtruth annotation.

  Args:
    image_id: unique image identifier either of type integer or string.
    category_id_set: A set of valid class ids. Detections with classes not in
      category_id_set are dropped.
    detection_boxes: float numpy array of shape [num_detections, 4] containing
      detection boxes.
    detection_scores: float numpy array of shape [num_detections] containing
      scored for the detection boxes.
    detection_classes: integer numpy array of shape [num_detections] containing
      the classes for detection boxes.

  Returns:
    a list of detection annotations for a single image in the COCO format.

  Raises:
    ValueError: if (1) detection_boxes, detection_scores and detection_classes
      do not have the right lengths or (2) if each of the elements inside these
      lists do not have the correct shapes or (3) if image_ids are not integers.
  """
    if len(detection_classes.shape) != 1 or len(detection_scores.shape) != 1:
        raise ValueError('All entries in detection_classes and detection_scoresexpected to be of rank 1.')
    if len(detection_boxes.shape) != 2:
        raise ValueError('All entries in detection_boxes expected to be of rank 2.')
    if detection_boxes.shape[1] != 4:
        raise ValueError('All entries in detection_boxes should have shape[1] == 4.')
    num_boxes = detection_classes.shape[0]
    if not num_boxes == detection_boxes.shape[0] == detection_scores.shape[0]:
        raise ValueError('Corresponding entries in detection_classes, detection_scores and detection_boxes should have compatible shapes (i.e., agree on the 0th dimension). Classes shape: %d. Boxes shape: %d. Scores shape: %d' % (
         detection_classes.shape[0], detection_boxes.shape[0],
         detection_scores.shape[0]))
    detections_list = []
    for i in range(num_boxes):
        if detection_classes[i] in category_id_set:
            detections_list.append({'image_id':image_id, 
             'category_id':int(detection_classes[i]), 
             'bbox':list(_ConvertBoxToCOCOFormat(detection_boxes[i, :])), 
             'score':float(detection_scores[i])})

    return detections_list


def ExportSingleImageDetectionMasksToCoco(image_id, category_id_set, detection_masks, detection_scores, detection_classes):
    """Export detection masks of a single image to COCO format.

  This function converts detections represented as numpy arrays to dictionaries
  that can be ingested by the COCO evaluation API. We assume that
  detection_masks, detection_scores, and detection_classes are in correspondence
  - that is: detection_masks[i, :], detection_classes[i] and detection_scores[i]
    are associated with the same annotation.

  Args:
    image_id: unique image identifier either of type integer or string.
    category_id_set: A set of valid class ids. Detections with classes not in
      category_id_set are dropped.
    detection_masks: uint8 numpy array of shape [num_detections, image_height,
      image_width] containing detection_masks.
    detection_scores: float numpy array of shape [num_detections] containing
      scores for detection masks.
    detection_classes: integer numpy array of shape [num_detections] containing
      the classes for detection masks.

  Returns:
    a list of detection mask annotations for a single image in the COCO format.

  Raises:
    ValueError: if (1) detection_masks, detection_scores and detection_classes
      do not have the right lengths or (2) if each of the elements inside these
      lists do not have the correct shapes or (3) if image_ids are not integers.
  """
    if len(detection_classes.shape) != 1 or len(detection_scores.shape) != 1:
        raise ValueError('All entries in detection_classes and detection_scoresexpected to be of rank 1.')
    num_boxes = detection_classes.shape[0]
    if not num_boxes == len(detection_masks) == detection_scores.shape[0]:
        raise ValueError('Corresponding entries in detection_classes, detection_scores and detection_masks should have compatible lengths and shapes Classes length: %d.  Masks length: %d. Scores length: %d' % (
         detection_classes.shape[0], len(detection_masks),
         detection_scores.shape[0]))
    detections_list = []
    for i in range(num_boxes):
        if detection_classes[i] in category_id_set:
            detections_list.append({'image_id':image_id, 
             'category_id':int(detection_classes[i]), 
             'segmentation':_RleCompress(detection_masks[i]), 
             'score':float(detection_scores[i])})

    return detections_list


def ExportDetectionsToCOCO--- This code section failed: ---

 L. 660         0  LOAD_GLOBAL              set
                2  LOAD_LISTCOMP            '<code_object <listcomp>>'
                4  LOAD_STR                 'ExportDetectionsToCOCO.<locals>.<listcomp>'
                6  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                8  LOAD_FAST                'categories'
               10  GET_ITER         
               12  CALL_FUNCTION_1       1  '1 positional argument'
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  STORE_FAST               'category_id_set'

 L. 661        18  BUILD_LIST_0          0 
               20  STORE_FAST               'detections_export_list'

 L. 662        22  LOAD_GLOBAL              len
               24  LOAD_FAST                'image_ids'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  LOAD_GLOBAL              len
               30  LOAD_FAST                'detection_boxes'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  DUP_TOP          
               36  ROT_THREE        
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    68  'to 68'
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'detection_scores'
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  DUP_TOP          
               50  ROT_THREE        
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    68  'to 68'

 L. 663        56  LOAD_GLOBAL              len
               58  LOAD_FAST                'detection_classes'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_TRUE     78  'to 78'
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            54  '54'
             68_1  COME_FROM            40  '40'
               68  POP_TOP          
             70_0  COME_FROM            66  '66'

 L. 664        70  LOAD_GLOBAL              ValueError
               72  LOAD_STR                 'Input lists must have the same length'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            64  '64'

 L. 665        78  SETUP_LOOP          132  'to 132'
               80  LOAD_GLOBAL              zip
               82  LOAD_FAST                'image_ids'
               84  LOAD_FAST                'detection_boxes'

 L. 666        86  LOAD_FAST                'detection_scores'

 L. 667        88  LOAD_FAST                'detection_classes'
               90  CALL_FUNCTION_4       4  '4 positional arguments'
               92  GET_ITER         
               94  FOR_ITER            130  'to 130'
               96  UNPACK_SEQUENCE_4     4 
               98  STORE_FAST               'image_id'
              100  STORE_FAST               'boxes'
              102  STORE_FAST               'scores'
              104  STORE_FAST               'classes'

 L. 668       106  LOAD_FAST                'detections_export_list'
              108  LOAD_METHOD              extend
              110  LOAD_GLOBAL              ExportSingleImageDetectionBoxesToCoco

 L. 669       112  LOAD_FAST                'image_id'

 L. 670       114  LOAD_FAST                'category_id_set'

 L. 671       116  LOAD_FAST                'boxes'

 L. 672       118  LOAD_FAST                'scores'

 L. 673       120  LOAD_FAST                'classes'
              122  CALL_FUNCTION_5       5  '5 positional arguments'
              124  CALL_METHOD_1         1  '1 positional argument'
              126  POP_TOP          
              128  JUMP_BACK            94  'to 94'
              130  POP_BLOCK        
            132_0  COME_FROM_LOOP       78  '78'

 L. 674       132  LOAD_FAST                'output_path'
              134  POP_JUMP_IF_FALSE   180  'to 180'

 L. 675       136  LOAD_GLOBAL              tf
              138  LOAD_ATTR                gfile
              140  LOAD_METHOD              GFile
              142  LOAD_FAST                'output_path'
              144  LOAD_STR                 'w'
              146  CALL_METHOD_2         2  '2 positional arguments'
              148  SETUP_WITH          174  'to 174'
              150  STORE_FAST               'fid'

 L. 676       152  LOAD_GLOBAL              json_utils
              154  LOAD_ATTR                Dump
              156  LOAD_FAST                'detections_export_list'
              158  LOAD_FAST                'fid'
              160  LOAD_CONST               4
              162  LOAD_CONST               2
              164  LOAD_CONST               ('float_digits', 'indent')
              166  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              168  POP_TOP          
              170  POP_BLOCK        
              172  LOAD_CONST               None
            174_0  COME_FROM_WITH      148  '148'
              174  WITH_CLEANUP_START
              176  WITH_CLEANUP_FINISH
              178  END_FINALLY      
            180_0  COME_FROM           134  '134'

 L. 677       180  LOAD_FAST                'detections_export_list'
              182  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 68


def ExportSegmentsToCOCO--- This code section failed: ---

 L. 728         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'image_ids'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  LOAD_GLOBAL              len
                8  LOAD_FAST                'detection_masks'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  DUP_TOP          
               14  ROT_THREE        
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    46  'to 46'
               20  LOAD_GLOBAL              len
               22  LOAD_FAST                'detection_scores'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  DUP_TOP          
               28  ROT_THREE        
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    46  'to 46'

 L. 729        34  LOAD_GLOBAL              len
               36  LOAD_FAST                'detection_classes'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_TRUE     56  'to 56'
               44  JUMP_FORWARD         48  'to 48'
             46_0  COME_FROM            32  '32'
             46_1  COME_FROM            18  '18'
               46  POP_TOP          
             48_0  COME_FROM            44  '44'

 L. 730        48  LOAD_GLOBAL              ValueError
               50  LOAD_STR                 'Input lists must have the same length'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            42  '42'

 L. 732        56  BUILD_LIST_0          0 
               58  STORE_FAST               'segment_export_list'

 L. 733        60  SETUP_LOOP          260  'to 260'
               62  LOAD_GLOBAL              zip
               64  LOAD_FAST                'image_ids'
               66  LOAD_FAST                'detection_masks'

 L. 734        68  LOAD_FAST                'detection_scores'

 L. 735        70  LOAD_FAST                'detection_classes'
               72  CALL_FUNCTION_4       4  '4 positional arguments'
               74  GET_ITER         
               76  FOR_ITER            258  'to 258'
               78  UNPACK_SEQUENCE_4     4 
               80  STORE_FAST               'image_id'
               82  STORE_FAST               'masks'
               84  STORE_FAST               'scores'
               86  STORE_FAST               'classes'

 L. 737        88  LOAD_GLOBAL              len
               90  LOAD_FAST                'classes'
               92  LOAD_ATTR                shape
               94  CALL_FUNCTION_1       1  '1 positional argument'
               96  LOAD_CONST               1
               98  COMPARE_OP               !=
              100  POP_JUMP_IF_TRUE    116  'to 116'
              102  LOAD_GLOBAL              len
              104  LOAD_FAST                'scores'
              106  LOAD_ATTR                shape
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  LOAD_CONST               1
              112  COMPARE_OP               !=
              114  POP_JUMP_IF_FALSE   124  'to 124'
            116_0  COME_FROM           100  '100'

 L. 738       116  LOAD_GLOBAL              ValueError
              118  LOAD_STR                 'All entries in detection_classes and detection_scoresexpected to be of rank 1.'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  RAISE_VARARGS_1       1  'exception instance'
            124_0  COME_FROM           114  '114'

 L. 740       124  LOAD_GLOBAL              len
              126  LOAD_FAST                'masks'
              128  LOAD_ATTR                shape
              130  CALL_FUNCTION_1       1  '1 positional argument'
              132  LOAD_CONST               4
              134  COMPARE_OP               !=
              136  POP_JUMP_IF_FALSE   154  'to 154'

 L. 741       138  LOAD_GLOBAL              ValueError
              140  LOAD_STR                 'All entries in masks expected to be of rank 4. Given {}'
              142  LOAD_METHOD              format

 L. 742       144  LOAD_FAST                'masks'
              146  LOAD_ATTR                shape
              148  CALL_METHOD_1         1  '1 positional argument'
              150  CALL_FUNCTION_1       1  '1 positional argument'
              152  RAISE_VARARGS_1       1  'exception instance'
            154_0  COME_FROM           136  '136'

 L. 744       154  LOAD_FAST                'classes'
              156  LOAD_ATTR                shape
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  STORE_FAST               'num_boxes'

 L. 745       164  LOAD_FAST                'num_boxes'
              166  LOAD_FAST                'masks'
              168  LOAD_ATTR                shape
              170  LOAD_CONST               0
              172  BINARY_SUBSCR    
              174  DUP_TOP          
              176  ROT_THREE        
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   196  'to 196'
              182  LOAD_FAST                'scores'
              184  LOAD_ATTR                shape
              186  LOAD_CONST               0
              188  BINARY_SUBSCR    
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_TRUE    206  'to 206'
              194  JUMP_FORWARD        198  'to 198'
            196_0  COME_FROM           180  '180'
              196  POP_TOP          
            198_0  COME_FROM           194  '194'

 L. 746       198  LOAD_GLOBAL              ValueError
              200  LOAD_STR                 'Corresponding entries in segment_classes, detection_scores and detection_boxes should have compatible shapes (i.e., agree on the 0th dimension).'
              202  CALL_FUNCTION_1       1  '1 positional argument'
              204  RAISE_VARARGS_1       1  'exception instance'
            206_0  COME_FROM           192  '192'

 L. 750       206  LOAD_GLOBAL              set
              208  LOAD_LISTCOMP            '<code_object <listcomp>>'
              210  LOAD_STR                 'ExportSegmentsToCOCO.<locals>.<listcomp>'
              212  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              214  LOAD_FAST                'categories'
              216  GET_ITER         
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  CALL_FUNCTION_1       1  '1 positional argument'
              222  STORE_FAST               'category_id_set'

 L. 751       224  LOAD_FAST                'segment_export_list'
              226  LOAD_METHOD              extend
              228  LOAD_GLOBAL              ExportSingleImageDetectionMasksToCoco

 L. 752       230  LOAD_FAST                'image_id'
              232  LOAD_FAST                'category_id_set'
              234  LOAD_GLOBAL              np
              236  LOAD_ATTR                squeeze
              238  LOAD_FAST                'masks'
              240  LOAD_CONST               3
              242  LOAD_CONST               ('axis',)
              244  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              246  LOAD_FAST                'scores'
              248  LOAD_FAST                'classes'
              250  CALL_FUNCTION_5       5  '5 positional arguments'
              252  CALL_METHOD_1         1  '1 positional argument'
              254  POP_TOP          
              256  JUMP_BACK            76  'to 76'
              258  POP_BLOCK        
            260_0  COME_FROM_LOOP       60  '60'

 L. 754       260  LOAD_FAST                'output_path'
          262_264  POP_JUMP_IF_FALSE   310  'to 310'

 L. 755       266  LOAD_GLOBAL              tf
              268  LOAD_ATTR                gfile
              270  LOAD_METHOD              GFile
              272  LOAD_FAST                'output_path'
              274  LOAD_STR                 'w'
              276  CALL_METHOD_2         2  '2 positional arguments'
              278  SETUP_WITH          304  'to 304'
              280  STORE_FAST               'fid'

 L. 756       282  LOAD_GLOBAL              json_utils
              284  LOAD_ATTR                Dump
              286  LOAD_FAST                'segment_export_list'
              288  LOAD_FAST                'fid'
              290  LOAD_CONST               4
              292  LOAD_CONST               2
              294  LOAD_CONST               ('float_digits', 'indent')
              296  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              298  POP_TOP          
              300  POP_BLOCK        
              302  LOAD_CONST               None
            304_0  COME_FROM_WITH      278  '278'
              304  WITH_CLEANUP_START
              306  WITH_CLEANUP_FINISH
              308  END_FINALLY      
            310_0  COME_FROM           262  '262'

 L. 757       310  LOAD_FAST                'segment_export_list'
              312  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 46


def ExportKeypointsToCOCO--- This code section failed: ---

 L. 806         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'image_ids'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  LOAD_GLOBAL              len
                8  LOAD_FAST                'detection_keypoints'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  DUP_TOP          
               14  ROT_THREE        
               16  COMPARE_OP               ==
               18  POP_JUMP_IF_FALSE    46  'to 46'

 L. 807        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'detection_scores'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  DUP_TOP          
               28  ROT_THREE        
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    46  'to 46'
               34  LOAD_GLOBAL              len
               36  LOAD_FAST                'detection_classes'
               38  CALL_FUNCTION_1       1  '1 positional argument'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_TRUE     56  'to 56'
               44  JUMP_FORWARD         48  'to 48'
             46_0  COME_FROM            32  '32'
             46_1  COME_FROM            18  '18'
               46  POP_TOP          
             48_0  COME_FROM            44  '44'

 L. 808        48  LOAD_GLOBAL              ValueError
               50  LOAD_STR                 'Input lists must have the same length'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  RAISE_VARARGS_1       1  'exception instance'
             56_0  COME_FROM            42  '42'

 L. 810        56  BUILD_LIST_0          0 
               58  STORE_FAST               'keypoints_export_list'

 L. 811     60_62  SETUP_LOOP          416  'to 416'
               64  LOAD_GLOBAL              zip

 L. 812        66  LOAD_FAST                'image_ids'
               68  LOAD_FAST                'detection_keypoints'
               70  LOAD_FAST                'detection_scores'
               72  LOAD_FAST                'detection_classes'
               74  CALL_FUNCTION_4       4  '4 positional arguments'
               76  GET_ITER         
            78_80  FOR_ITER            414  'to 414'
               82  UNPACK_SEQUENCE_4     4 
               84  STORE_FAST               'image_id'
               86  STORE_FAST               'keypoints'
               88  STORE_FAST               'scores'
               90  STORE_FAST               'classes'

 L. 814        92  LOAD_GLOBAL              len
               94  LOAD_FAST                'classes'
               96  LOAD_ATTR                shape
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  LOAD_CONST               1
              102  COMPARE_OP               !=
              104  POP_JUMP_IF_TRUE    120  'to 120'
              106  LOAD_GLOBAL              len
              108  LOAD_FAST                'scores'
              110  LOAD_ATTR                shape
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  LOAD_CONST               1
              116  COMPARE_OP               !=
              118  POP_JUMP_IF_FALSE   128  'to 128'
            120_0  COME_FROM           104  '104'

 L. 815       120  LOAD_GLOBAL              ValueError
              122  LOAD_STR                 'All entries in detection_classes and detection_scoresexpected to be of rank 1.'
              124  CALL_FUNCTION_1       1  '1 positional argument'
              126  RAISE_VARARGS_1       1  'exception instance'
            128_0  COME_FROM           118  '118'

 L. 817       128  LOAD_GLOBAL              len
              130  LOAD_FAST                'keypoints'
              132  LOAD_ATTR                shape
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  LOAD_CONST               3
              138  COMPARE_OP               !=
              140  POP_JUMP_IF_FALSE   158  'to 158'

 L. 818       142  LOAD_GLOBAL              ValueError
              144  LOAD_STR                 'All entries in keypoints expected to be of rank 3. Given {}'
              146  LOAD_METHOD              format

 L. 819       148  LOAD_FAST                'keypoints'
              150  LOAD_ATTR                shape
              152  CALL_METHOD_1         1  '1 positional argument'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  RAISE_VARARGS_1       1  'exception instance'
            158_0  COME_FROM           140  '140'

 L. 821       158  LOAD_FAST                'classes'
              160  LOAD_ATTR                shape
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  STORE_FAST               'num_boxes'

 L. 822       168  LOAD_FAST                'num_boxes'
              170  LOAD_FAST                'keypoints'
              172  LOAD_ATTR                shape
              174  LOAD_CONST               0
              176  BINARY_SUBSCR    
              178  DUP_TOP          
              180  ROT_THREE        
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   200  'to 200'
              186  LOAD_FAST                'scores'
              188  LOAD_ATTR                shape
              190  LOAD_CONST               0
              192  BINARY_SUBSCR    
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_TRUE    210  'to 210'
              198  JUMP_FORWARD        202  'to 202'
            200_0  COME_FROM           184  '184'
              200  POP_TOP          
            202_0  COME_FROM           198  '198'

 L. 823       202  LOAD_GLOBAL              ValueError
              204  LOAD_STR                 'Corresponding entries in detection_classes, detection_keypoints, and detection_scores should have compatible shapes (i.e., agree on the 0th dimension).'
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  RAISE_VARARGS_1       1  'exception instance'
            210_0  COME_FROM           196  '196'

 L. 827       210  LOAD_GLOBAL              set
              212  LOAD_LISTCOMP            '<code_object <listcomp>>'
              214  LOAD_STR                 'ExportKeypointsToCOCO.<locals>.<listcomp>'
              216  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              218  LOAD_FAST                'categories'
              220  GET_ITER         
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  STORE_FAST               'category_id_set'

 L. 828       228  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              230  LOAD_STR                 'ExportKeypointsToCOCO.<locals>.<dictcomp>'
              232  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 829       234  LOAD_FAST                'categories'
              236  GET_ITER         
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  STORE_FAST               'category_id_to_num_keypoints_map'

 L. 832       242  SETUP_LOOP          412  'to 412'
              244  LOAD_GLOBAL              range
              246  LOAD_FAST                'num_boxes'
              248  CALL_FUNCTION_1       1  '1 positional argument'
              250  GET_ITER         
            252_0  COME_FROM           288  '288'
              252  FOR_ITER            410  'to 410'
              254  STORE_FAST               'i'

 L. 833       256  LOAD_FAST                'classes'
              258  LOAD_FAST                'i'
              260  BINARY_SUBSCR    
              262  LOAD_FAST                'category_id_set'
              264  COMPARE_OP               not-in
          266_268  POP_JUMP_IF_FALSE   278  'to 278'

 L. 834       270  LOAD_GLOBAL              ValueError
              272  LOAD_STR                 'class id should be in category_id_set\n'
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  RAISE_VARARGS_1       1  'exception instance'
            278_0  COME_FROM           266  '266'

 L. 836       278  LOAD_FAST                'classes'
              280  LOAD_FAST                'i'
              282  BINARY_SUBSCR    
              284  LOAD_FAST                'category_id_to_num_keypoints_map'
              286  COMPARE_OP               in
              288  POP_JUMP_IF_FALSE   252  'to 252'

 L. 837       290  LOAD_FAST                'category_id_to_num_keypoints_map'
              292  LOAD_FAST                'classes'
              294  LOAD_FAST                'i'
              296  BINARY_SUBSCR    
              298  BINARY_SUBSCR    
              300  STORE_FAST               'num_keypoints'

 L. 840       302  LOAD_GLOBAL              np
              304  LOAD_ATTR                concatenate

 L. 841       306  LOAD_FAST                'keypoints'
              308  LOAD_FAST                'i'
              310  LOAD_CONST               0
              312  LOAD_FAST                'num_keypoints'
              314  BUILD_SLICE_2         2 
              316  LOAD_CONST               None
              318  LOAD_CONST               None
              320  BUILD_SLICE_2         2 
              322  BUILD_TUPLE_3         3 
              324  BINARY_SUBSCR    

 L. 842       326  LOAD_GLOBAL              np
              328  LOAD_ATTR                expand_dims
              330  LOAD_GLOBAL              np
              332  LOAD_METHOD              ones
              334  LOAD_FAST                'num_keypoints'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  LOAD_CONST               1
              340  LOAD_CONST               ('axis',)
              342  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              344  BUILD_LIST_2          2 

 L. 843       346  LOAD_CONST               1
              348  LOAD_CONST               ('axis',)
              350  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              352  LOAD_METHOD              astype
              354  LOAD_GLOBAL              int
              356  CALL_METHOD_1         1  '1 positional argument'
              358  STORE_FAST               'instance_keypoints'

 L. 845       360  LOAD_FAST                'instance_keypoints'
              362  LOAD_METHOD              flatten
              364  CALL_METHOD_0         0  '0 positional arguments'
              366  LOAD_METHOD              tolist
              368  CALL_METHOD_0         0  '0 positional arguments'
              370  STORE_FAST               'instance_keypoints'

 L. 846       372  LOAD_FAST                'keypoints_export_list'
              374  LOAD_METHOD              append

 L. 847       376  LOAD_FAST                'image_id'

 L. 848       378  LOAD_GLOBAL              int
              380  LOAD_FAST                'classes'
              382  LOAD_FAST                'i'
              384  BINARY_SUBSCR    
              386  CALL_FUNCTION_1       1  '1 positional argument'

 L. 849       388  LOAD_FAST                'instance_keypoints'

 L. 850       390  LOAD_GLOBAL              float
              392  LOAD_FAST                'scores'
              394  LOAD_FAST                'i'
              396  BINARY_SUBSCR    
              398  CALL_FUNCTION_1       1  '1 positional argument'
              400  LOAD_CONST               ('image_id', 'category_id', 'keypoints', 'score')
              402  BUILD_CONST_KEY_MAP_4     4 
              404  CALL_METHOD_1         1  '1 positional argument'
              406  POP_TOP          
              408  JUMP_BACK           252  'to 252'
              410  POP_BLOCK        
            412_0  COME_FROM_LOOP      242  '242'
              412  JUMP_BACK            78  'to 78'
              414  POP_BLOCK        
            416_0  COME_FROM_LOOP       60  '60'

 L. 853       416  LOAD_FAST                'output_path'
          418_420  POP_JUMP_IF_FALSE   466  'to 466'

 L. 854       422  LOAD_GLOBAL              tf
              424  LOAD_ATTR                gfile
              426  LOAD_METHOD              GFile
              428  LOAD_FAST                'output_path'
              430  LOAD_STR                 'w'
              432  CALL_METHOD_2         2  '2 positional arguments'
              434  SETUP_WITH          460  'to 460'
              436  STORE_FAST               'fid'

 L. 855       438  LOAD_GLOBAL              json_utils
              440  LOAD_ATTR                Dump
              442  LOAD_FAST                'keypoints_export_list'
              444  LOAD_FAST                'fid'
              446  LOAD_CONST               4
              448  LOAD_CONST               2
              450  LOAD_CONST               ('float_digits', 'indent')
              452  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              454  POP_TOP          
              456  POP_BLOCK        
              458  LOAD_CONST               None
            460_0  COME_FROM_WITH      434  '434'
              460  WITH_CLEANUP_START
              462  WITH_CLEANUP_FINISH
              464  END_FINALLY      
            466_0  COME_FROM           418  '418'

 L. 856       466  LOAD_FAST                'keypoints_export_list'
              468  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 46