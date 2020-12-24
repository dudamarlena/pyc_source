# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/core/standard_fields.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 11689 bytes
"""Contains classes specifying naming conventions used for object detection.

Specifies:
  InputDataFields: standard fields used by reader/preprocessor/batcher.
  DetectionResultFields: standard fields returned by object detector.
  BoxListFields: standard field used by BoxList
  TfExampleFields: standard fields for tf-example data format (go/tf-example).
"""

class InputDataFields(object):
    __doc__ = 'Names for the input tensors.\n\n  Holds the standard data field names to use for identifying input tensors. This\n  should be used by the decoder to identify keys for the returned tensor_dict\n  containing input tensors. And it should be used by the model to identify the\n  tensors it needs.\n\n  Attributes:\n    image: image.\n    image_additional_channels: additional channels.\n    original_image: image in the original input size.\n    original_image_spatial_shape: image in the original input size.\n    key: unique key corresponding to image.\n    source_id: source of the original image.\n    filename: original filename of the dataset (without common path).\n    groundtruth_image_classes: image-level class labels.\n    groundtruth_image_confidences: image-level class confidences.\n    groundtruth_boxes: coordinates of the ground truth boxes in the image.\n    groundtruth_classes: box-level class labels.\n    groundtruth_confidences: box-level class confidences. The shape should be\n      the same as the shape of groundtruth_classes.\n    groundtruth_label_types: box-level label types (e.g. explicit negative).\n    groundtruth_is_crowd: [DEPRECATED, use groundtruth_group_of instead]\n      is the groundtruth a single object or a crowd.\n    groundtruth_area: area of a groundtruth segment.\n    groundtruth_difficult: is a `difficult` object\n    groundtruth_group_of: is a `group_of` objects, e.g. multiple objects of the\n      same class, forming a connected group, where instances are heavily\n      occluding each other.\n    proposal_boxes: coordinates of object proposal boxes.\n    proposal_objectness: objectness score of each proposal.\n    groundtruth_instance_masks: ground truth instance masks.\n    groundtruth_instance_boundaries: ground truth instance boundaries.\n    groundtruth_instance_classes: instance mask-level class labels.\n    groundtruth_keypoints: ground truth keypoints.\n    groundtruth_keypoint_visibilities: ground truth keypoint visibilities.\n    groundtruth_label_weights: groundtruth label weights.\n    groundtruth_weights: groundtruth weight factor for bounding boxes.\n    num_groundtruth_boxes: number of groundtruth boxes.\n    is_annotated: whether an image has been labeled or not.\n    true_image_shapes: true shapes of images in the resized images, as resized\n      images can be padded with zeros.\n    multiclass_scores: the label score per class for each box.\n  '
    image = 'image'
    image_additional_channels = 'image_additional_channels'
    original_image = 'original_image'
    original_image_spatial_shape = 'original_image_spatial_shape'
    key = 'key'
    source_id = 'source_id'
    filename = 'filename'
    groundtruth_image_classes = 'groundtruth_image_classes'
    groundtruth_image_confidences = 'groundtruth_image_confidences'
    groundtruth_boxes = 'groundtruth_boxes'
    groundtruth_classes = 'groundtruth_classes'
    groundtruth_confidences = 'groundtruth_confidences'
    groundtruth_label_types = 'groundtruth_label_types'
    groundtruth_is_crowd = 'groundtruth_is_crowd'
    groundtruth_area = 'groundtruth_area'
    groundtruth_difficult = 'groundtruth_difficult'
    groundtruth_group_of = 'groundtruth_group_of'
    proposal_boxes = 'proposal_boxes'
    proposal_objectness = 'proposal_objectness'
    groundtruth_instance_masks = 'groundtruth_instance_masks'
    groundtruth_instance_boundaries = 'groundtruth_instance_boundaries'
    groundtruth_instance_classes = 'groundtruth_instance_classes'
    groundtruth_keypoints = 'groundtruth_keypoints'
    groundtruth_keypoint_visibilities = 'groundtruth_keypoint_visibilities'
    groundtruth_label_weights = 'groundtruth_label_weights'
    groundtruth_weights = 'groundtruth_weights'
    num_groundtruth_boxes = 'num_groundtruth_boxes'
    is_annotated = 'is_annotated'
    true_image_shape = 'true_image_shape'
    multiclass_scores = 'multiclass_scores'


class DetectionResultFields(object):
    __doc__ = 'Naming conventions for storing the output of the detector.\n\n  Attributes:\n    source_id: source of the original image.\n    key: unique key corresponding to image.\n    detection_boxes: coordinates of the detection boxes in the image.\n    detection_scores: detection scores for the detection boxes in the image.\n    detection_multiclass_scores: class score distribution (including background)\n      for detection boxes in the image including background class.\n    detection_classes: detection-level class labels.\n    detection_masks: contains a segmentation mask for each detection box.\n    detection_boundaries: contains an object boundary for each detection box.\n    detection_keypoints: contains detection keypoints for each detection box.\n    num_detections: number of detections in the batch.\n    raw_detection_boxes: contains decoded detection boxes without Non-Max\n      suppression.\n    raw_detection_scores: contains class score logits for raw detection boxes.\n    detection_anchor_indices: The anchor indices of the detections after NMS.\n    detection_features: contains extracted features for each detected box\n      after NMS.\n  '
    source_id = 'source_id'
    key = 'key'
    detection_boxes = 'detection_boxes'
    detection_scores = 'detection_scores'
    detection_multiclass_scores = 'detection_multiclass_scores'
    detection_features = 'detection_features'
    detection_classes = 'detection_classes'
    detection_masks = 'detection_masks'
    detection_boundaries = 'detection_boundaries'
    detection_keypoints = 'detection_keypoints'
    num_detections = 'num_detections'
    raw_detection_boxes = 'raw_detection_boxes'
    raw_detection_scores = 'raw_detection_scores'
    detection_anchor_indices = 'detection_anchor_indices'


class BoxListFields(object):
    __doc__ = 'Naming conventions for BoxLists.\n\n  Attributes:\n    boxes: bounding box coordinates.\n    classes: classes per bounding box.\n    scores: scores per bounding box.\n    weights: sample weights per bounding box.\n    objectness: objectness score per bounding box.\n    masks: masks per bounding box.\n    boundaries: boundaries per bounding box.\n    keypoints: keypoints per bounding box.\n    keypoint_heatmaps: keypoint heatmaps per bounding box.\n    is_crowd: is_crowd annotation per bounding box.\n  '
    boxes = 'boxes'
    classes = 'classes'
    scores = 'scores'
    weights = 'weights'
    confidences = 'confidences'
    objectness = 'objectness'
    masks = 'masks'
    boundaries = 'boundaries'
    keypoints = 'keypoints'
    keypoint_heatmaps = 'keypoint_heatmaps'
    is_crowd = 'is_crowd'


class PredictionFields(object):
    __doc__ = 'Naming conventions for standardized prediction outputs.\n\n  Attributes:\n    feature_maps: List of feature maps for prediction.\n    anchors: Generated anchors.\n    raw_detection_boxes: Decoded detection boxes without NMS.\n    raw_detection_feature_map_indices: Feature map indices from which each raw\n      detection box was produced.\n  '
    feature_maps = 'feature_maps'
    anchors = 'anchors'
    raw_detection_boxes = 'raw_detection_boxes'
    raw_detection_feature_map_indices = 'raw_detection_feature_map_indices'


class TfExampleFields(object):
    __doc__ = 'TF-example proto feature names for object detection.\n\n  Holds the standard feature names to load from an Example proto for object\n  detection.\n\n  Attributes:\n    image_encoded: JPEG encoded string\n    image_format: image format, e.g. "JPEG"\n    filename: filename\n    channels: number of channels of image\n    colorspace: colorspace, e.g. "RGB"\n    height: height of image in pixels, e.g. 462\n    width: width of image in pixels, e.g. 581\n    source_id: original source of the image\n    image_class_text: image-level label in text format\n    image_class_label: image-level label in numerical format\n    object_class_text: labels in text format, e.g. ["person", "cat"]\n    object_class_label: labels in numbers, e.g. [16, 8]\n    object_bbox_xmin: xmin coordinates of groundtruth box, e.g. 10, 30\n    object_bbox_xmax: xmax coordinates of groundtruth box, e.g. 50, 40\n    object_bbox_ymin: ymin coordinates of groundtruth box, e.g. 40, 50\n    object_bbox_ymax: ymax coordinates of groundtruth box, e.g. 80, 70\n    object_view: viewpoint of object, e.g. ["frontal", "left"]\n    object_truncated: is object truncated, e.g. [true, false]\n    object_occluded: is object occluded, e.g. [true, false]\n    object_difficult: is object difficult, e.g. [true, false]\n    object_group_of: is object a single object or a group of objects\n    object_depiction: is object a depiction\n    object_is_crowd: [DEPRECATED, use object_group_of instead]\n      is the object a single object or a crowd\n    object_segment_area: the area of the segment.\n    object_weight: a weight factor for the object\'s bounding box.\n    instance_masks: instance segmentation masks.\n    instance_boundaries: instance boundaries.\n    instance_classes: Classes for each instance segmentation mask.\n    detection_class_label: class label in numbers.\n    detection_bbox_ymin: ymin coordinates of a detection box.\n    detection_bbox_xmin: xmin coordinates of a detection box.\n    detection_bbox_ymax: ymax coordinates of a detection box.\n    detection_bbox_xmax: xmax coordinates of a detection box.\n    detection_score: detection score for the class label and box.\n  '
    image_encoded = 'image/encoded'
    image_format = 'image/format'
    filename = 'image/filename'
    channels = 'image/channels'
    colorspace = 'image/colorspace'
    height = 'image/height'
    width = 'image/width'
    source_id = 'image/source_id'
    image_class_text = 'image/class/text'
    image_class_label = 'image/class/label'
    object_class_text = 'image/object/class/text'
    object_class_label = 'image/object/class/label'
    object_bbox_ymin = 'image/object/bbox/ymin'
    object_bbox_xmin = 'image/object/bbox/xmin'
    object_bbox_ymax = 'image/object/bbox/ymax'
    object_bbox_xmax = 'image/object/bbox/xmax'
    object_view = 'image/object/view'
    object_truncated = 'image/object/truncated'
    object_occluded = 'image/object/occluded'
    object_difficult = 'image/object/difficult'
    object_group_of = 'image/object/group_of'
    object_depiction = 'image/object/depiction'
    object_is_crowd = 'image/object/is_crowd'
    object_segment_area = 'image/object/segment/area'
    object_weight = 'image/object/weight'
    instance_masks = 'image/segmentation/object'
    instance_boundaries = 'image/boundaries/object'
    instance_classes = 'image/segmentation/object/class'
    detection_class_label = 'image/detection/label'
    detection_bbox_ymin = 'image/detection/bbox/ymin'
    detection_bbox_xmin = 'image/detection/bbox/xmin'
    detection_bbox_ymax = 'image/detection/bbox/ymax'
    detection_bbox_xmax = 'image/detection/bbox/xmax'
    detection_score = 'image/detection/score'