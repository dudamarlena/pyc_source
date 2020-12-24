# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/bbox.py
# Compiled at: 2019-08-28 02:48:51
# Size of source mod 2**32: 6106 bytes
import numpy as np

def bbox_overlaps(bboxes1, bboxes2, mode='iou'):
    """Calculate the ious between each bbox of bboxes1 and bboxes2.
    Args:
        bboxes1(ndarray): shape (n, 4)
        bboxes2(ndarray): shape (k, 4)
        mode(str): iou (intersection over union) or iof (intersection
            over foreground)
    Returns:
        ious(ndarray): shape (n, k)
    """
    from icv.data.core.bbox import BBox
    assert mode in ('iou', 'iof')
    bboxes1 = np.array([np.array(b.bbox) if isinstance(b, BBox) else b for b in bboxes1])
    bboxes2 = np.array([np.array(b.bbox) if isinstance(b, BBox) else b for b in bboxes2])
    bboxes1 = bboxes1.astype(np.float32)
    bboxes2 = bboxes2.astype(np.float32)
    rows = bboxes1.shape[0]
    cols = bboxes2.shape[0]
    ious = np.zeros((rows, cols), dtype=(np.float32))
    if rows * cols == 0:
        return ious
    else:
        exchange = False
        if bboxes1.shape[0] > bboxes2.shape[0]:
            bboxes1, bboxes2 = bboxes2, bboxes1
            ious = np.zeros((cols, rows), dtype=(np.float32))
            exchange = True
        area1 = (bboxes1[:, 2] - bboxes1[:, 0] + 1) * (bboxes1[:, 3] - bboxes1[:, 1] + 1)
        area2 = (bboxes2[:, 2] - bboxes2[:, 0] + 1) * (bboxes2[:, 3] - bboxes2[:, 1] + 1)
        for i in range(bboxes1.shape[0]):
            x_start = np.maximum(bboxes1[(i, 0)], bboxes2[:, 0])
            y_start = np.maximum(bboxes1[(i, 1)], bboxes2[:, 1])
            x_end = np.minimum(bboxes1[(i, 2)], bboxes2[:, 2])
            y_end = np.minimum(bboxes1[(i, 3)], bboxes2[:, 3])
            overlap = np.maximum(x_end - x_start + 1, 0) * np.maximum(y_end - y_start + 1, 0)
            if mode == 'iou':
                union = area1[i] + area2 - overlap
            else:
                union = area1[i] if not exchange else area2
            ious[i, :] = overlap / union

        if exchange:
            ious = ious.T
        return ious


def py_cpu_nms(dets, thresh):
    """Pure Python NMS baseline."""
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        tmp = x1[order[1:]]
        xxxx = x1[i]
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        inds = np.where(ovr <= thresh)[0]
        indsd = inds + 1
        order = order[(inds + 1)]

    return keep


def soft_nms(boxes, sigma=0.5, Nt=0.1, threshold=0.001, method=1):
    N = boxes.shape[0]
    pos = 0
    maxscore = 0
    maxpos = 0
    for i in range(N):
        maxscore = boxes[(i, 4)]
        maxpos = i
        tx1 = boxes[(i, 0)]
        ty1 = boxes[(i, 1)]
        tx2 = boxes[(i, 2)]
        ty2 = boxes[(i, 3)]
        ts = boxes[(i, 4)]
        pos = i + 1
        while pos < N:
            if maxscore < boxes[(pos, 4)]:
                maxscore = boxes[(pos, 4)]
                maxpos = pos
            pos = pos + 1

        boxes[(i, 0)] = boxes[(maxpos, 0)]
        boxes[(i, 1)] = boxes[(maxpos, 1)]
        boxes[(i, 2)] = boxes[(maxpos, 2)]
        boxes[(i, 3)] = boxes[(maxpos, 3)]
        boxes[(i, 4)] = boxes[(maxpos, 4)]
        boxes[(maxpos, 0)] = tx1
        boxes[(maxpos, 1)] = ty1
        boxes[(maxpos, 2)] = tx2
        boxes[(maxpos, 3)] = ty2
        boxes[(maxpos, 4)] = ts
        tx1 = boxes[(i, 0)]
        ty1 = boxes[(i, 1)]
        tx2 = boxes[(i, 2)]
        ty2 = boxes[(i, 3)]
        ts = boxes[(i, 4)]
        pos = i + 1
        while pos < N:
            x1 = boxes[(pos, 0)]
            y1 = boxes[(pos, 1)]
            x2 = boxes[(pos, 2)]
            y2 = boxes[(pos, 3)]
            s = boxes[(pos, 4)]
            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            iw = min(tx2, x2) - max(tx1, x1) + 1
            if iw > 0:
                ih = min(ty2, y2) - max(ty1, y1) + 1
                if ih > 0:
                    ua = float((tx2 - tx1 + 1) * (ty2 - ty1 + 1) + area - iw * ih)
                    ov = iw * ih / ua
                    if method == 1:
                        if ov > Nt:
                            weight = 1 - ov
                        else:
                            weight = 1
                    else:
                        if method == 2:
                            weight = np.exp(-(ov * ov) / sigma)
                        else:
                            if ov > Nt:
                                weight = 0
                            else:
                                weight = 1
                            boxes[(pos, 4)] = weight * boxes[(pos, 4)]
                            print(boxes[:, 4])
                            if boxes[(pos, 4)] < threshold:
                                boxes[(pos, 0)] = boxes[(N - 1, 0)]
                                boxes[(pos, 1)] = boxes[(N - 1, 1)]
                                boxes[(pos, 2)] = boxes[(N - 1, 2)]
                                boxes[(pos, 3)] = boxes[(N - 1, 3)]
                                boxes[(pos, 4)] = boxes[(N - 1, 4)]
                                N = N - 1
                                pos = pos - 1
            pos = pos + 1

    keep = [i for i in range(N)]
    return keep