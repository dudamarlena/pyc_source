# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/utils/image.py
# Compiled at: 2020-03-29 10:22:43
# Size of source mod 2**32: 9192 bytes
import colorsys, random, cv2, numpy as np, tensorflow as tf
__all__ = [
 'image_resize', 'draw_bbox', 'postprocess_boxes', 'nms',
 'boxes_iou', 'boxes_iou_np', 'boxes_iou_tf', 'boxes_giou_tf']

def image_resize(image, target_size, gt_boxes=None):
    ih, iw = target_size
    h, w, _ = image.shape
    scale = min(iw / w, ih / h)
    nw, nh = int(scale * w), int(scale * h)
    image_resized = cv2.resize(image, (nw, nh))
    image_pad = np.full(shape=[ih, iw, 3], fill_value=128.0)
    dw, dh = (iw - nw) // 2, (ih - nh) // 2
    image_pad[dh:nh + dh, dw:nw + dw, :] = image_resized
    image_pad = image_pad / 255.0
    if gt_boxes is None:
        return image_pad
    gt_boxes[:, [0, 2]] = gt_boxes[:, [0, 2]] * scale + dw
    gt_boxes[:, [1, 3]] = gt_boxes[:, [1, 3]] * scale + dh
    return (image_pad, gt_boxes)


def draw_bbox(image, boxes, classes, show_label=True):
    """
    bboxes: [x_min, y_min, x_max, y_max, probability, cls_id] format coordinates.
    """
    num_classes = len(classes)
    image_h, image_w, _ = image.shape
    hsv_tuples = [(1.0 * x / num_classes, 1.0, 1.0) for x in range(num_classes)]
    colors = list(map(lambda x: (colorsys.hsv_to_rgb)(*x), hsv_tuples))
    colors = list(map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), colors))
    random.seed(0)
    random.shuffle(colors)
    random.seed(None)
    for i, bbox in enumerate(boxes):
        coor = np.array((bbox[:4]), dtype=(np.int32))
        fontScale = 0.5
        score = bbox[4]
        class_ind = int(bbox[5])
        bbox_color = colors[class_ind]
        bbox_thick = int(0.6 * (image_h + image_w) / 600)
        c1, c2 = (coor[0], coor[1]), (coor[2], coor[3])
        cv2.rectangle(image, c1, c2, bbox_color, bbox_thick)
        if show_label:
            bbox_mess = '%s: %.2f' % (classes[class_ind], score)
            t_size = cv2.getTextSize(bbox_mess, 0, fontScale, thickness=(bbox_thick // 2))[0]
            cv2.rectangle(image, c1, (c1[0] + t_size[0], c1[1] - t_size[1] - 3), bbox_color, -1)
            cv2.putText(image, bbox_mess, (c1[0], c1[1] - 2), (cv2.FONT_HERSHEY_SIMPLEX), fontScale,
              (0, 0, 0), (bbox_thick // 2), lineType=(cv2.LINE_AA))

    return image


def boxes_iou(boxes1, boxes2):
    boxes1 = np.array(boxes1)
    boxes2 = np.array(boxes2)
    boxes1_area = (boxes1[(Ellipsis, 2)] - boxes1[(Ellipsis, 0)]) * (boxes1[(Ellipsis,
                                                                             3)] - boxes1[(Ellipsis,
                                                                                           1)])
    boxes2_area = (boxes2[(Ellipsis, 2)] - boxes2[(Ellipsis, 0)]) * (boxes2[(Ellipsis,
                                                                             3)] - boxes2[(Ellipsis,
                                                                                           1)])
    left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])
    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[(Ellipsis, 0)] * inter_section[(Ellipsis, 1)]
    union_area = boxes1_area + boxes2_area - inter_area
    ious = np.maximum(1.0 * inter_area / union_area, np.finfo(np.float32).eps)
    return ious


def boxes_iou_np(boxes1, boxes2):
    boxes1 = np.array(boxes1)
    boxes2 = np.array(boxes2)
    boxes1_area = boxes1[(Ellipsis, 2)] * boxes1[(Ellipsis, 3)]
    boxes2_area = boxes2[(Ellipsis, 2)] * boxes2[(Ellipsis, 3)]
    boxes1 = np.concatenate([boxes1[..., :2] - boxes1[..., 2:] * 0.5,
     boxes1[..., :2] + boxes1[..., 2:] * 0.5],
      axis=(-1))
    boxes2 = np.concatenate([boxes2[..., :2] - boxes2[..., 2:] * 0.5,
     boxes2[..., :2] + boxes2[..., 2:] * 0.5],
      axis=(-1))
    left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])
    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[(Ellipsis, 0)] * inter_section[(Ellipsis, 1)]
    union_area = boxes1_area + boxes2_area - inter_area
    return inter_area / union_area


def boxes_iou_tf(boxes1, boxes2):
    boxes1_area = boxes1[(Ellipsis, 2)] * boxes1[(Ellipsis, 3)]
    boxes2_area = boxes2[(Ellipsis, 2)] * boxes2[(Ellipsis, 3)]
    boxes1 = tf.concat([boxes1[..., :2] - boxes1[..., 2:] * 0.5,
     boxes1[..., :2] + boxes1[..., 2:] * 0.5],
      axis=(-1))
    boxes2 = tf.concat([boxes2[..., :2] - boxes2[..., 2:] * 0.5,
     boxes2[..., :2] + boxes2[..., 2:] * 0.5],
      axis=(-1))
    left_up = tf.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down = tf.minimum(boxes1[..., 2:], boxes2[..., 2:])
    inter_section = tf.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[(Ellipsis, 0)] * inter_section[(Ellipsis, 1)]
    union_area = boxes1_area + boxes2_area - inter_area
    return 1.0 * inter_area / union_area


def boxes_giou_tf(boxes1, boxes2):
    boxes1 = tf.concat([boxes1[..., :2] - boxes1[..., 2:] * 0.5,
     boxes1[..., :2] + boxes1[..., 2:] * 0.5],
      axis=(-1))
    boxes2 = tf.concat([boxes2[..., :2] - boxes2[..., 2:] * 0.5,
     boxes2[..., :2] + boxes2[..., 2:] * 0.5],
      axis=(-1))
    boxes1 = tf.concat([tf.minimum(boxes1[..., :2], boxes1[..., 2:]),
     tf.maximum(boxes1[..., :2], boxes1[..., 2:])],
      axis=(-1))
    boxes2 = tf.concat([tf.minimum(boxes2[..., :2], boxes2[..., 2:]),
     tf.maximum(boxes2[..., :2], boxes2[..., 2:])],
      axis=(-1))
    boxes1_area = (boxes1[(Ellipsis, 2)] - boxes1[(Ellipsis, 0)]) * (boxes1[(Ellipsis,
                                                                             3)] - boxes1[(Ellipsis,
                                                                                           1)])
    boxes2_area = (boxes2[(Ellipsis, 2)] - boxes2[(Ellipsis, 0)]) * (boxes2[(Ellipsis,
                                                                             3)] - boxes2[(Ellipsis,
                                                                                           1)])
    left_up = tf.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down = tf.minimum(boxes1[..., 2:], boxes2[..., 2:])
    inter_section = tf.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[(Ellipsis, 0)] * inter_section[(Ellipsis, 1)]
    union_area = boxes1_area + boxes2_area - inter_area
    iou = inter_area / union_area
    enclose_left_up = tf.minimum(boxes1[..., :2], boxes2[..., :2])
    enclose_right_down = tf.maximum(boxes1[..., 2:], boxes2[..., 2:])
    enclose = tf.maximum(enclose_right_down - enclose_left_up, 0.0)
    enclose_area = enclose[(Ellipsis, 0)] * enclose[(Ellipsis, 1)]
    giou = iou - 1.0 * (enclose_area - union_area) / enclose_area
    return giou


def nms(boxes, iou_threshold, sigma=0.3, method='nms'):
    """
    :param method:
    :param sigma:
    :param iou_threshold:
    :param boxes: (xmin, ymin, xmax, ymax, score, class)

    Note: soft-nms, https://arxiv.org/pdf/1704.04503.pdf
          https://github.com/bharatsingh430/soft-nms
    """
    classes_in_img = list(set(boxes[:, 5]))
    best_boxes = []
    for cls in classes_in_img:
        cls_mask = boxes[:, 5] == cls
        cls_boxes = boxes[cls_mask]
        while len(cls_boxes) > 0:
            max_ind = np.argmax(cls_boxes[:, 4])
            best_bbox = cls_boxes[max_ind]
            best_boxes.append(best_bbox)
            cls_boxes = np.concatenate([cls_boxes[:max_ind], cls_boxes[max_ind + 1:]])
            iou = boxes_iou(best_bbox[np.newaxis, :4], cls_boxes[:, :4])
            weight = np.ones((len(iou),), dtype=(np.float32))
            assert method in ('nms', 'soft-nms')
            if method == 'nms':
                iou_mask = iou > iou_threshold
                weight[iou_mask] = 0.0
            if method == 'soft-nms':
                weight = np.exp(-(1.0 * iou ** 2 / sigma))
            cls_boxes[:, 4] = cls_boxes[:, 4] * weight
            score_mask = cls_boxes[:, 4] > 0.0
            cls_boxes = cls_boxes[score_mask]

    return best_boxes


def postprocess_boxes(pred_bbox, org_img_shape, input_size, score_threshold):
    valid_scale = [
     0, np.inf]
    pred_bbox = np.array(pred_bbox)
    pred_xywh = pred_bbox[:, 0:4]
    pred_conf = pred_bbox[:, 4]
    pred_prob = pred_bbox[:, 5:]
    pred_coor = np.concatenate([pred_xywh[:, :2] - pred_xywh[:, 2:] * 0.5,
     pred_xywh[:, :2] + pred_xywh[:, 2:] * 0.5],
      axis=(-1))
    org_h, org_w = org_img_shape
    resize_ratio = min(input_size / org_w, input_size / org_h)
    dw = (input_size - resize_ratio * org_w) / 2
    dh = (input_size - resize_ratio * org_h) / 2
    pred_coor[:, 0::2] = 1.0 * (pred_coor[:, 0::2] - dw) / resize_ratio
    pred_coor[:, 1::2] = 1.0 * (pred_coor[:, 1::2] - dh) / resize_ratio
    pred_coor = np.concatenate([np.maximum(pred_coor[:, :2], [0, 0]),
     np.minimum(pred_coor[:, 2:], [org_w - 1, org_h - 1])],
      axis=(-1))
    invalid_mask = np.logical_or(pred_coor[:, 0] > pred_coor[:, 2], pred_coor[:, 1] > pred_coor[:, 3])
    pred_coor[invalid_mask] = 0
    bboxes_scale = np.sqrt(np.multiply.reduce((pred_coor[:, 2:4] - pred_coor[:, 0:2]), axis=(-1)))
    scale_mask = np.logical_and(valid_scale[0] < bboxes_scale, bboxes_scale < valid_scale[1])
    classes = np.argmax(pred_prob, axis=(-1))
    scores = pred_conf * pred_prob[(np.arange(len(pred_coor)), classes)]
    score_mask = scores > score_threshold
    mask = np.logical_and(scale_mask, score_mask)
    coors, scores, classes = pred_coor[mask], scores[mask], classes[mask]
    return np.concatenate([coors, scores[:, np.newaxis], classes[:, np.newaxis]], axis=(-1))