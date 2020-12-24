# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/limcv/template.py
# Compiled at: 2019-12-11 22:37:24
# Size of source mod 2**32: 5408 bytes
"""模板匹配.

对用户提供的调节参数:
    1. threshod: 筛选阈值，默认为0.8
    2. rgb: 彩色三通道,进行彩色权识别.
"""
import os, cv2
from six import PY2, PY3
import numpy as np, json
from .utils import generate_result, check_source_larger_than_search, img_mat_rgb_2_gray
from .cal_confidence import cal_rgb_confidence
from .match import get_perfect_scale
from .sift import find_sift
from .aircv import imread, resize

def find(im_source_path, im_search_path):
    im_source = imread(im_source_path)
    im_search = imread(im_search_path)
    result = find_all_template_multy_scale(im_source, im_search)
    if result:
        return result
    result = find_sift(im_source, im_search)
    return result


def find_by_sift(im_source_path, im_search_path):
    im_source = imread(im_source_path)
    im_search = imread(im_search_path)
    result = find_sift(im_source, im_search)
    return result


def find_all_template_multy_scale(im_source, im_search):
    result = []
    result = find_all_template(im_source, im_search)
    if result == None:
        scale = get_perfect_scale(im_source, im_search)
        result = find_all_template(im_source, im_search, scale=scale)
    return result


def find_template(im_source, im_search, threshold=0.8, scale=1.0, rgb=False):
    """函数功能：找到最优结果."""
    if scale == 0:
        scale = 1
    if scale != 1:
        im_source = resize(im_source, scale)
    check_source_larger_than_search(im_source, im_search)
    res = _get_template_result_matrix(im_source, im_search)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    h, w = im_search.shape[:2]
    confidence = _get_confidence_from_matrix(im_source, im_search, max_loc, max_val, w, h, rgb)
    middle_point, rectangle = _get_target_rectangle(max_loc, w, h)
    best_match = generate_result(middle_point, rectangle, confidence)
    if confidence >= threshold:
        return best_match


def find_all_template(im_source, im_search, threshold=0.8, scale=1.0, rgb=False, max_count=10):
    """根据输入图片和参数设置,返回所有的图像识别结果."""
    if scale == 0:
        scale = 1
    if scale != 1:
        im_source = resize(im_source, scale)
    check_source_larger_than_search(im_source, im_search)
    res = _get_template_result_matrix(im_source, im_search)
    result = []
    h, w = im_search.shape[:2]
    while 1:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        confidence = _get_confidence_from_matrix(im_source, im_search, max_loc, max_val, w, h, rgb)
        if not confidence < threshold:
            if len(result) > max_count:
                break
            middle_point, rectangle = _get_target_rectangle(max_loc, w, h)
            one_good_match = generate_result(middle_point, rectangle, confidence)
            result.append(one_good_match)
            cv2.rectangle(res, (int(max_loc[0] - w / 2), int(max_loc[1] - h / 2)), (int(max_loc[0] + w / 2), int(max_loc[1] + h / 2)), (0,
                                                                                                                                        0,
                                                                                                                                        0), -1)

    if result:
        return result


def _get_confidence_from_matrix(im_source, im_search, max_loc, max_val, w, h, rgb):
    """根据结果矩阵求出confidence."""
    if rgb:
        img_crop = im_source[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w]
        confidence = cal_rgb_confidence(img_crop, im_search)
    else:
        confidence = max_val
    return confidence


def _get_template_result_matrix(im_source, im_search):
    """求取模板匹配的结果矩阵."""
    s_gray, i_gray = img_mat_rgb_2_gray(im_search), img_mat_rgb_2_gray(im_source)
    return cv2.matchTemplate(i_gray, s_gray, cv2.TM_CCOEFF_NORMED)


def _get_target_rectangle(left_top_pos, w, h):
    """根据左上角点和宽高求出目标区域."""
    x_min, y_min = left_top_pos
    x_middle, y_middle = int(x_min + w / 2), int(y_min + h / 2)
    left_bottom_pos, right_bottom_pos = (
     x_min, y_min + h), (x_min + w, y_min + h)
    right_top_pos = (x_min + w, y_min)
    middle_point = (
     x_middle, y_middle)
    rectangle = (
     left_top_pos, left_bottom_pos, right_bottom_pos, right_top_pos)
    return (
     middle_point, rectangle)