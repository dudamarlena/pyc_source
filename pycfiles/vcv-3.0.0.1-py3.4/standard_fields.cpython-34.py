# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/core/standard_fields.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 6234 bytes
"""Contains classes specifying naming conventions used for object detection.

Specifies:
  InputDataFields: standard fields used by reader/preprocessor/batcher.
  BoxListFields: standard field used by BoxList
  TfExampleFields: standard fields for tf-example data format (go/tf-example).
"""

class InputDataFields(object):
    __doc__ = 'Names for the input tensors.\n\n  Holds the standard data field names to use for identifying input tensors. This\n  should be used by the decoder to identify keys for the returned tensor_dict\n  containing input tensors. And it should be used by the model to identify the\n  tensors it needs.\n\n  Attributes:\n    image: image.\n    original_image: image in the original input size.\n    key: unique key corresponding to image.\n    source_id: source of the original image.\n    filename: original filename of the dataset (without common path).\n    groundtruth_image_classes: image-level class labels.\n    groundtruth_boxes: coordinates of the ground truth boxes in the image.\n    groundtruth_classes: box-level class labels.\n    groundtruth_label_types: box-level label types (e.g. explicit negative).\n    groundtruth_is_crowd: is the groundtruth a single object or a crowd.\n    groundtruth_area: area of a groundtruth segment.\n    groundtruth_difficult: is a `difficult` object\n    proposal_boxes: coordinates of object proposal boxes.\n    proposal_objectness: objectness score of each proposal.\n    groundtruth_instance_masks: ground truth instance masks.\n    groundtruth_instance_classes: instance mask-level class labels.\n    groundtruth_keypoints: ground truth keypoints.\n    groundtruth_keypoint_visibilities: ground truth keypoint visibilities.\n    groundtruth_label_scores: groundtruth label scores.\n  '
    image = 'image'
    original_image = 'original_image'
    key = 'key'
    source_id = 'source_id'
    filename = 'filename'
    groundtruth_image_classes = 'groundtruth_image_classes'
    groundtruth_boxes = 'groundtruth_boxes'
    groundtruth_classes = 'groundtruth_classes'
    groundtruth_label_types = 'groundtruth_label_types'
    groundtruth_is_crowd = 'groundtruth_is_crowd'
    groundtruth_area = 'groundtruth_area'
    groundtruth_difficult = 'groundtruth_difficult'
    proposal_boxes = 'proposal_boxes'
    proposal_objectness = 'proposal_objectness'
    groundtruth_instance_masks = 'groundtruth_instance_masks'
    groundtruth_instance_classes = 'groundtruth_instance_classes'
    groundtruth_keypoints = 'groundtruth_keypoints'
    groundtruth_keypoint_visibilities = 'groundtruth_keypoint_visibilities'
    groundtruth_label_scores = 'groundtruth_label_scores'


class BoxListFields(object):
    __doc__ = 'Naming conventions for BoxLists.\n\n  Attributes:\n    boxes: bounding box coordinates.\n    classes: classes per bounding box.\n    scores: scores per bounding box.\n    weights: sample weights per bounding box.\n    objectness: objectness score per bounding box.\n    masks: masks per bounding box.\n    keypoints: keypoints per bounding box.\n    keypoint_heatmaps: keypoint heatmaps per bounding box.\n  '
    boxes = 'boxes'
    classes = 'classes'
    scores = 'scores'
    weights = 'weights'
    objectness = 'objectness'
    masks = 'masks'
    keypoints = 'keypoints'
    keypoint_heatmaps = 'keypoint_heatmaps'


class TfExampleFields(object):
    __doc__ = 'TF-example proto feature names for object detection.\n\n  Holds the standard feature names to load from an Example proto for object\n  detection.\n\n  Attributes:\n    image_encoded: JPEG encoded string\n    image_format: image format, e.g. "JPEG"\n    filename: filename\n    channels: number of channels of image\n    colorspace: colorspace, e.g. "RGB"\n    height: height of image in pixels, e.g. 462\n    width: width of image in pixels, e.g. 581\n    source_id: original source of the image\n    object_class_text: labels in text format, e.g. ["person", "cat"]\n    object_class_text: labels in numbers, e.g. [16, 8]\n    object_bbox_xmin: xmin coordinates of groundtruth box, e.g. 10, 30\n    object_bbox_xmax: xmax coordinates of groundtruth box, e.g. 50, 40\n    object_bbox_ymin: ymin coordinates of groundtruth box, e.g. 40, 50\n    object_bbox_ymax: ymax coordinates of groundtruth box, e.g. 80, 70\n    object_view: viewpoint of object, e.g. ["frontal", "left"]\n    object_truncated: is object truncated, e.g. [true, false]\n    object_occluded: is object occluded, e.g. [true, false]\n    object_difficult: is object difficult, e.g. [true, false]\n    object_is_crowd: is the object a single object or a crowd\n    object_segment_area: the area of the segment.\n    instance_masks: instance segmentation masks.\n    instance_classes: Classes for each instance segmentation mask.\n  '
    image_encoded = 'image/encoded'
    image_format = 'image/format'
    filename = 'image/filename'
    channels = 'image/channels'
    colorspace = 'image/colorspace'
    height = 'image/height'
    width = 'image/width'
    source_id = 'image/source_id'
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
    object_is_crowd = 'image/object/is_crowd'
    object_segment_area = 'image/object/segment/area'
    instance_masks = 'image/segmentation/object'
    instance_classes = 'image/segmentation/object/class'