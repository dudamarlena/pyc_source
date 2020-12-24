# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/limcv/template_matching.py
# Compiled at: 2019-12-11 22:43:06
# Size of source mod 2**32: 5146 bytes
"""模板匹配.

对用户提供的调节参数:
    1. threshod: 筛选阈值，默认为0.8
    2. rgb: 彩色三通道,进行彩色权识别.
"""
import cv2, time
from .utils import generate_result, check_source_larger_than_search, img_mat_rgb_2_gray
from .cal_confidence import cal_rgb_confidence

def print_run_time(func):

    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        ret = func(self, *args, **kwargs)
        return ret

    return wrapper


class TemplateMatching(object):
    __doc__ = '模板匹配.'
    METHOD_NAME = 'Template'
    MAX_RESULT_COUNT = 10

    def __init__(self, im_search, im_source, threshold=0.8, rgb=True):
        super(TemplateMatching, self).__init__()
        self.im_source = im_source
        self.im_search = im_search
        self.threshold = threshold
        self.rgb = rgb

    @print_run_time
    def find_all_results(self):
        """基于模板匹配查找多个目标区域的方法."""
        check_source_larger_than_search(self.im_source, self.im_search)
        res = self._get_template_result_matrix()
        result = []
        h, w = self.im_search.shape[:2]
        while 1:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            confidence = self._get_confidence_from_matrix(max_loc, max_val, w, h)
            if not confidence < self.threshold:
                if len(result) > self.MAX_RESULT_COUNT:
                    break
                middle_point, rectangle = self._get_target_rectangle(max_loc, w, h)
                one_good_match = generate_result(middle_point, rectangle, confidence)
                result.append(one_good_match)
                cv2.rectangle(res, (int(max_loc[0] - w / 2), int(max_loc[1] - h / 2)), (int(max_loc[0] + w / 2), int(max_loc[1] + h / 2)), (0,
                                                                                                                                            0,
                                                                                                                                            0), -1)

        if result:
            return result

    @print_run_time
    def find_best_result(self):
        """基于kaze进行图像识别，只筛选出最优区域."""
        check_source_larger_than_search(self.im_source, self.im_search)
        res = self._get_template_result_matrix()
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        h, w = self.im_search.shape[:2]
        confidence = self._get_confidence_from_matrix(max_loc, max_val, w, h)
        middle_point, rectangle = self._get_target_rectangle(max_loc, w, h)
        best_match = generate_result(middle_point, rectangle, confidence)
        if confidence >= self.threshold:
            return best_match

    def _get_confidence_from_matrix(self, max_loc, max_val, w, h):
        """根据结果矩阵求出confidence."""
        if self.rgb:
            img_crop = self.im_source[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w]
            confidence = cal_rgb_confidence(img_crop, self.im_search)
        else:
            confidence = max_val
        return confidence

    def _get_template_result_matrix(self):
        """求取模板匹配的结果矩阵."""
        s_gray, i_gray = img_mat_rgb_2_gray(self.im_search), img_mat_rgb_2_gray(self.im_source)
        return cv2.matchTemplate(i_gray, s_gray, cv2.TM_CCOEFF_NORMED)

    def _get_target_rectangle(self, left_top_pos, w, h):
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