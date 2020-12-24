# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mai\models\detection\retinanet_utils.py
# Compiled at: 2020-03-16 20:59:07
# Size of source mod 2**32: 3185 bytes
import torch
from torchvision.ops import nms
import torch.nn as nn
import numpy as np

class BBoxTransform(nn.Module):

    def __init__(self, mean=None, std=None):
        super(BBoxTransform, self).__init__()
        if mean is None:
            self.mean = torch.from_numpy(np.array([0, 0, 0, 0]).astype(np.float32)).cuda()
        else:
            self.mean = mean
        if std is None:
            self.std = torch.from_numpy(np.array([0.1, 0.1, 0.2, 0.2]).astype(np.float32)).cuda()
        else:
            self.std = std

    def forward(self, boxes, deltas):
        widths = boxes[:, :, 2] - boxes[:, :, 0]
        heights = boxes[:, :, 3] - boxes[:, :, 1]
        ctr_x = boxes[:, :, 0] + 0.5 * widths
        ctr_y = boxes[:, :, 1] + 0.5 * heights
        dx = deltas[:, :, 0] * self.std[0] + self.mean[0]
        dy = deltas[:, :, 1] * self.std[1] + self.mean[1]
        dw = deltas[:, :, 2] * self.std[2] + self.mean[2]
        dh = deltas[:, :, 3] * self.std[3] + self.mean[3]
        pred_ctr_x = ctr_x + dx * widths
        pred_ctr_y = ctr_y + dy * heights
        pred_w = torch.exp(dw) * widths
        pred_h = torch.exp(dh) * heights
        pred_boxes_x1 = pred_ctr_x - 0.5 * pred_w
        pred_boxes_y1 = pred_ctr_y - 0.5 * pred_h
        pred_boxes_x2 = pred_ctr_x + 0.5 * pred_w
        pred_boxes_y2 = pred_ctr_y + 0.5 * pred_h
        pred_boxes = torch.stack([pred_boxes_x1, pred_boxes_y1, pred_boxes_x2, pred_boxes_y2], dim=2)
        return pred_boxes


class ClipBoxes(nn.Module):

    def __init__(self, width=None, height=None):
        super(ClipBoxes, self).__init__()

    def forward(self, boxes, img):
        batch_size, num_channels, height, width = img.shape
        boxes[:, :, 0] = torch.clamp((boxes[:, :, 0]), min=0)
        boxes[:, :, 1] = torch.clamp((boxes[:, :, 1]), min=0)
        boxes[:, :, 2] = torch.clamp((boxes[:, :, 2]), max=width)
        boxes[:, :, 3] = torch.clamp((boxes[:, :, 3]), max=height)
        return boxes


def get_box(output, img_batch):
    """获取预测的结果
    :param classification:
    :param regression:
    :param anchors:
    :param img_batch: 图片输入
    :return:
    """
    classification, regression, anchors = output
    regressBoxes = BBoxTransform()
    clipBoxes = ClipBoxes()
    transformed_anchors = regressBoxes(anchors, regression)
    transformed_anchors = clipBoxes(transformed_anchors, img_batch)
    scores = torch.max(classification, dim=2, keepdim=True)[0]
    scores_over_thresh = (scores > 0.05)[0, :, 0]
    if scores_over_thresh.sum() == 0:
        return [torch.zeros(0), torch.zeros(0), torch.zeros(0, 4)]
    classification = classification[:, scores_over_thresh, :]
    transformed_anchors = transformed_anchors[:, scores_over_thresh, :]
    scores = scores[:, scores_over_thresh, :]
    anchors_nms_idx = nms(transformed_anchors[0, :, :], scores[0, :, 0], 0.5)
    nms_scores, nms_class = classification[0, anchors_nms_idx, :].max(dim=1)
    return [
     nms_scores, nms_class, transformed_anchors[0, anchors_nms_idx, :]]