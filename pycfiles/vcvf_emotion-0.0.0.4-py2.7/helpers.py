# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vcvf_emotion/face_utils/helpers.py
# Compiled at: 2018-08-01 08:04:54
from collections import OrderedDict
import numpy as np, cv2
FACIAL_LANDMARKS_IDXS = OrderedDict([
 (
  'mouth', (48, 68)),
 (
  'right_eyebrow', (17, 22)),
 (
  'left_eyebrow', (22, 27)),
 (
  'right_eye', (36, 42)),
 (
  'left_eye', (42, 48)),
 (
  'nose', (27, 36)),
 (
  'jaw', (0, 17))])

def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (
     x, y, w, h)


def shape_to_np(shape, dtype='int'):
    coords = np.zeros((shape.num_parts, 2), dtype=dtype)
    for i in range(0, shape.num_parts):
        coords[i] = (
         shape.part(i).x, shape.part(i).y)

    return coords


def visualize_facial_landmarks(image, shape, colors=None, alpha=0.75):
    overlay = image.copy()
    output = image.copy()
    if colors is None:
        colors = [
         (19, 199, 109), (79, 76, 240), (230, 159, 23),
         (168, 100, 168), (158, 163, 32),
         (163, 38, 32), (180, 42, 220)]
    for i, name in enumerate(FACIAL_LANDMARKS_IDXS.keys()):
        j, k = FACIAL_LANDMARKS_IDXS[name]
        pts = shape[j:k]
        if name == 'jaw':
            for l in range(1, len(pts)):
                ptA = tuple(pts[(l - 1)])
                ptB = tuple(pts[l])
                cv2.line(overlay, ptA, ptB, colors[i], 2)

        else:
            hull = cv2.convexHull(pts)
            cv2.drawContours(overlay, [hull], -1, colors[i], -1)

    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    return output