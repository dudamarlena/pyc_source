# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/wangtf/Projects/pascal_voc_tools/pascal_voc_tools/utils/nms.py
# Compiled at: 2019-07-08 05:31:16
# Size of source mod 2**32: 5434 bytes
"""
@File : nms.py
@Time : 2019/03/05 10:35:46
@Author : wangtf
@Version : 1.0
@Desc : None
"""
import numpy as np

def nms(dets, thresh):
    """Apply classic DPM-style greedy NMS."""
    if dets.shape[0] == 0:
        return []
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    scores = dets[:, 4]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]
    ndets = dets.shape[0]
    suppressed = np.zeros(ndets, dtype=(np.int))
    for _i in range(ndets):
        i = order[_i]
        if suppressed[i] == 1:
            continue
        ix1 = x1[i]
        iy1 = y1[i]
        ix2 = x2[i]
        iy2 = y2[i]
        iarea = areas[i]
        for _j in range(_i + 1, ndets):
            j = order[_j]
            if suppressed[j] == 1:
                continue
            xx1 = np.maximum(ix1, x1[j])
            yy1 = np.maximum(iy1, y1[j])
            xx2 = np.minimum(ix2, x2[j])
            yy2 = np.minimum(iy2, y2[j])
            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            ovr = inter / (iarea + areas[j] - inter)
            if ovr >= thresh:
                suppressed[j] = 1

    return np.where(suppressed == 0)[0]


def soft_nms(boxes_in, sigma=0.5, Nt=0.3, threshold=0.001, method=0):
    """methods = {'hard': 0, 'linear': 1, 'gaussian': 2}
    """
    if boxes_in.shape[0] == 0:
        return (
         boxes_in, [])
    boxes = boxes_in.copy()
    N = boxes.shape[0]
    pos = 0
    maxscore = 0
    maxpos = 0
    inds = np.arange(N)
    for i in range(N):
        maxscore = boxes[(i, 4)]
        maxpos = i
        tx1 = boxes[(i, 0)]
        ty1 = boxes[(i, 1)]
        tx2 = boxes[(i, 2)]
        ty2 = boxes[(i, 3)]
        ts = boxes[(i, 4)]
        ti = inds[i]
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
        inds[i] = inds[maxpos]
        boxes[(maxpos, 0)] = tx1
        boxes[(maxpos, 1)] = ty1
        boxes[(maxpos, 2)] = tx2
        boxes[(maxpos, 3)] = ty2
        boxes[(maxpos, 4)] = ts
        inds[maxpos] = ti
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
            iw = np.minimum(tx2, x2) - np.maximum(tx1, x1) + 1
            if iw > 0:
                ih = np.minimum(ty2, y2) - np.maximum(ty1, y1) + 1
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
                    if boxes[(pos, 4)] < threshold:
                        boxes[(pos, 0)] = boxes[(N - 1, 0)]
                        boxes[(pos, 1)] = boxes[(N - 1, 1)]
                        boxes[(pos, 2)] = boxes[(N - 1, 2)]
                        boxes[(pos, 3)] = boxes[(N - 1, 3)]
                        boxes[(pos, 4)] = boxes[(N - 1, 4)]
                        inds[pos] = inds[(N - 1)]
                        N = N - 1
                        pos = pos - 1
            pos = pos + 1

    return (
     boxes[:N], inds[:N])