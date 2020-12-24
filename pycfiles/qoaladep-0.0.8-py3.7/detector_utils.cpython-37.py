# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoaladep/utils/detector_utils.py
# Compiled at: 2020-04-06 05:25:07
# Size of source mod 2**32: 4236 bytes
"""
    File name: utils.py.py
    Author: [Qoala Ds Team]
    Date created: / /2019
    Date last modified: //2020
    Python Version: >= 3.5
    Qoaladep version: v0.2
    Maintainer: [Qoala Ds Team]
"""
import cv2, random, numpy as np

def nms(result_detection: [float], confidence_threshold=0.75, overlap_threshold=0.3) -> [float]:
    """[summary]
    
    Arguments:
        result_detection {[type]} -- [description]
    
    Keyword Arguments:
        confidence_threshold {float} -- [description] (default: {0.75})
        overlap_threshold {float} -- [description] (default: {0.3})
    
    Returns:
        [float] -- [description]
    """
    result_box = []
    result_conf = []
    result_class = []
    final_bbox = []
    for boxes in result_detection:
        mask = boxes[:, 4] > confidence_threshold
        boxes = boxes[mask, :]
        classes = np.argmax((boxes[:, 5:]), axis=(-1))
        classes = classes.astype(np.float32).reshape((classes.shape[0], 1))
        boxes = np.concatenate((boxes[:, :5], classes), axis=(-1))
        boxes_dict = dict()
        for cls in range(16):
            mask = boxes[:, 5] == cls
            mask_shape = mask.shape
            if np.sum(mask.astype(np.int)) != 0:
                class_boxes = boxes[mask, :]
                boxes_coords = class_boxes[:, :4]
                boxes_ = boxes_coords.copy()
                boxes_[:, 2] = boxes_coords[:, 2] - boxes_coords[:, 0]
                boxes_[:, 3] = boxes_coords[:, 3] - boxes_coords[:, 1]
                boxes_ = boxes_.astype(np.int)
                boxes_conf_scores = class_boxes[:, 4:5]
                boxes_conf_scores = boxes_conf_scores.reshape(len(boxes_conf_scores))
                the_class = class_boxes[:, 5:]
                result_box.extend(boxes_.tolist())
                result_conf.extend(boxes_conf_scores.tolist())
                result_class.extend(the_class.tolist())

    indices = cv2.dnn.NMSBoxes(result_box, result_conf, confidence_threshold, overlap_threshold)
    for i in indices:
        i = i[0]
        box = result_box[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        conf = result_conf[i]
        the_class = result_class[i][0]
        final_bbox.append([left, top, width, height, conf, the_class])

    return final_bbox


def crop_image(image, bboxes: [
 [
  float]]) -> []:
    """[summary]
        
        Arguments:
            image {[type]} -- [description]
            bboxes {[type]} -- [[x1, y1, w, h, obj prob, class], [], ...], Absolute to 416x416 size
        
        Returns:
            [] -- [description]
        """
    h, w, c = image.shape
    crop_list = []
    for i in bboxes:
        x1 = int(i[0] * w / 416)
        y1 = int(i[1] * h / 416)
        w1 = int(i[2] * w / 416)
        h1 = int(i[3] * h / 416)
        crop = image[y1:y1 + h1, x1:x1 + w1]
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        crop_list.append(crop)

    return crop_list


def draw_rectangle(image, bboxes: [
 [
  float]]):
    """[summary]

    Arguments:
        image {[type]} -- [description]
        bboxes {[type]} -- [description]
    """
    for i in bboxes:
        start_point = (
         int(i[0]), int(i[1]))
        end_point = (int(i[0] + i[2]), int(i[1] + i[3]))
        rg = random.randint(0, 255)
        rb = random.randint(0, 255)
        image = cv2.rectangle(image, start_point, end_point, (rg, rb, 125), thickness=1)
        end_point = (int(i[0]), int(i[1] + i[3] / 4.0))
        image = cv2.line(image, start_point, end_point, (rg, rb, 125), thickness=2)
        end_point = (int(i[0] + i[2] / 4.0), int(i[1]))
        image = cv2.line(image, start_point, end_point, (rg, rb, 125), thickness=2)
        start_point = (int(i[0] + i[2]), int(i[1] + i[3]))
        end_point = (int(i[0] + i[2]), int(i[1] + i[3] / 2.0))
        image = cv2.line(image, start_point, end_point, (rg, rb, 125), thickness=2)
        end_point = (int(i[0] + i[2] / 2.0), int(i[1] + i[3]))
        image = cv2.line(image, start_point, end_point, (rg, rb, 125), thickness=2)

    return image