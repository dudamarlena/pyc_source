# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zeus/PyTorch-Hackathon-2019/rectifai/tools/utils_posenet.py
# Compiled at: 2019-09-16 16:01:48
# Size of source mod 2**32: 3735 bytes
import cv2, numpy as np, math, subprocess, time
from rectifai.models.posenet.settings import *

def valid_resolution(width, height, output_stride=16):
    target_width = int(width) // output_stride * output_stride + 1
    target_height = int(height) // output_stride * output_stride + 1
    return (target_width, target_height)


def _process_input(source_img, scale_factor=0.7125, output_stride=16):
    target_width, target_height = valid_resolution((source_img.shape[1] * scale_factor),
      (source_img.shape[0] * scale_factor), output_stride=output_stride)
    scale = np.array([source_img.shape[0] / target_height, source_img.shape[1] / target_width])
    input_img = cv2.resize(source_img, (target_width, target_height), interpolation=(cv2.INTER_LINEAR))
    input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB).astype(np.float32)
    input_img = input_img * 0.00784313725490196 - 1.0
    input_img = input_img.transpose((2, 0, 1)).reshape(1, 3, target_height, target_width)
    return (input_img, source_img, scale)


def read_cap(cap, scale_factor=1.0, output_stride=16):
    res, img = cap.read()
    if not res:
        raise IOError('webcam failure')
    return _process_input(img, scale_factor, output_stride)


def read_imgfile(path, scale_factor=1.0, output_stride=16):
    img = cv2.imread(path)
    return _process_input(img, scale_factor, output_stride)


def draw_keypoints(img, instance_scores, keypoint_scores, keypoint_coords, min_pose_confidence=0.5, min_part_confidence=0.5):
    print('draw_keypoints')
    cv_keypoints = []
    for ii, score in enumerate(instance_scores):
        if score < min_pose_confidence:
            continue
        for ks, kc in zip(keypoint_scores[ii, :], keypoint_coords[ii, :, :]):
            if ks < min_part_confidence:
                continue
            cv_keypoints.append(cv2.KeyPoint(kc[1], kc[0], 10.0 * ks))

    out_img = cv2.drawKeypoints(img, cv_keypoints, outImage=(np.array([])))
    return out_img


cache = [
 240]

def get_adjacent_keypoints(keypoint_scores, keypoint_coords, min_confidence=0.1):
    results = []
    status = [
     'status', 'here']
    for left, right in CONNECTED_PART_INDICES:
        if not keypoint_scores[left] < min_confidence:
            keypoint_scores[right] < min_confidence or results.append(np.array([keypoint_coords[left][::-1], keypoint_coords[right][::-1]]).astype(np.int32))

    return (
     results, status)


def draw_skeleton_and_keypoints(img, instance_scores, keypoint_scores, keypoint_coords, min_pose_score=0.15, min_part_score=0.1):
    out_img = img
    adjacent_keypoints = []
    cv_keypoints = []
    status = ['status', 'here']
    for ii, score in enumerate(instance_scores):
        if score < min_pose_score:
            continue
        new_keypoints, status = get_adjacent_keypoints(keypoint_scores[ii, :], keypoint_coords[ii, :, :], min_part_score)
        adjacent_keypoints.extend(new_keypoints)
        for ks, kc in zip(keypoint_scores[ii, :], keypoint_coords[ii, :, :]):
            if ks < min_part_score:
                continue
            cv_keypoints.append(cv2.KeyPoint(kc[1], kc[0], 10.0 * ks))

    if cv_keypoints:
        out_img = cv2.drawKeypoints(out_img,
          cv_keypoints, outImage=(np.array([])), color=(0, 0, 255), flags=(cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
    out_img = cv2.polylines(out_img, adjacent_keypoints, isClosed=False, color=(0,
                                                                                0,
                                                                                255))
    if cv_keypoints:
        import pdb
        pdb.set_trace()
    return (out_img, cv_keypoints, status)