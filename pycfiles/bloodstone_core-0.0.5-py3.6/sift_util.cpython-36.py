# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wmpy_util/sift_util.py
# Compiled at: 2020-01-06 03:52:58
# Size of source mod 2**32: 13369 bytes
"""
@Author  : WeiWang Zhang
@Time    : 2019-09-20 12:09
@File    : sift_util.py
@Software: PyCharm
@Desc    : 基于SIFT相似度算法，将'训练图片'仿射变换为'查询图片'的大小
"""
from wmpy_util.time_util import *
from wmpy_util import img_util as iu
from wmpy_util import file_util as fu
import numpy as np, os, cv2

class CardLocateException(Exception):

    def __init__(self, err='sift error!'):
        Exception.__init__(self, err)


feature_cache = dict()

class SiftCardLocator:

    def __init__(self, save_debug=False, save_path=None, speed_up=False):
        self.save_debug = save_debug
        if save_debug:
            fu.check_dir(save_path, True)
        self.save_path = save_path
        self.sift = cv2.xfeatures2d.SIFT_create()
        self.MIN_MATCH_COUNT = 10
        self.KNN_MATCH_SUPPRESS = 0.8
        self.speed_up = speed_up

    def locate(self, query_img, train_img, train_mask=None, **kwargs):
        """
        寻找图像中的身份证并进行图像矫正（透视变换）
        :param query_img: 用于查询的图片(如，标准身份证图片)
        :param query_feature:查询图片的sift特征，如果传递该参数将不重复计算query_img的sift特征
        :param train_img: 为需要识别的图像
        :param train_mask: 训练图片掩膜，用于计算sift特征
        :return:
        """
        qh, qw = query_img.shape[:2]
        if self.speed_up:
            query_pts, train_pts = self.find_match_with_sift_fast(query_img, train_img, train_mask)
        else:
            query_pts, train_pts = self.find_match_with_sift(query_img, train_img, train_mask)
        q2t_mat, _ = cv2.findHomography(query_pts, train_pts, cv2.RANSAC, 5.0)
        query_edge = np.float32([[0, 0], [0, qh - 1], [qw - 1, qh - 1], [qw - 1, 0]]).reshape(-1, 1, 2)
        query_dege_on_train = cv2.perspectiveTransform(query_edge, q2t_mat)
        t2q_mat = np.mat(q2t_mat).I
        result_img = cv2.warpPerspective(train_img, t2q_mat, (qw, qh), borderValue=[255, 255, 255], borderMode=(cv2.BORDER_REPLICATE))
        if self.save_debug:
            train_copy = train_img.copy()
            iu.save_result(train_copy, self.save_path, 'origin.jpg')
            cv2.polylines(train_copy, [np.int32(query_dege_on_train)], True, [0, 255, 0], 2, cv2.LINE_AA)
            img_combine = iu.img_joint_with_colorgap((train_copy, result_img), axis=1,
              align=0,
              gap=2,
              gap_color=[
             255, 0, 0])
            iu.save_result(img_combine, self.save_path, 'origin_vs_transform.jpg')
        if len(query_pts) <= self.MIN_MATCH_COUNT:
            raise CardLocateException('模板匹配度不足 - %d/%d' % (len(query_pts), self.MIN_MATCH_COUNT))
        check_area_size(train_img.shape, query_dege_on_train)
        return (
         result_img, t2q_mat, query_dege_on_train)

    def find_match_with_sift(self, query_img, train_img, train_mask=None):
        """
        找到两张图片的匹配点对
        :param query_img:
        :param train_img:
        :param train_mask:
        :return:
        """
        if callable(train_mask):
            train_mask = train_mask(query_img)
        query_kp, query_des = self.get_x_feature(query_img, mask=None, cache=(self.speed_up))
        train_kp, train_des = self.get_x_feature(train_img, mask=train_mask)
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=10)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(query_des, train_des, k=2)
        good = []
        for m, n in matches:
            if m.distance < self.KNN_MATCH_SUPPRESS * n.distance:
                good.append(m)

        if self.save_debug:
            flag = cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
            tmp = cv2.drawMatches(query_img, query_kp, train_img, train_kp, good, outImg=None, flags=flag)
            pic_name = 'sift_match.jpg'
            cv2.imwrite(os.path.join(self.save_path, pic_name), tmp)
            cv2.imwrite(os.path.join(self.save_path, 'train_mask.jpg'), train_mask)
        query_pts = np.float32([query_kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        train_pts = np.float32([train_kp[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        return (query_pts, train_pts)

    def find_match_with_sift_fast(self, query_img, train_img, train_mask=None):
        """
        找到两张图片的匹配点对
        :param query_img:
        :param train_img:
        :param train_mask:
        :return:
        """
        x_feature_width = 600
        query_small, query_scall = iu.img_resize_longer_size(query_img, x_feature_width)
        train_small, train_scall = iu.img_resize_longer_size(train_img, x_feature_width)
        query_pts, train_pts = self.find_match_with_sift(query_small, train_small, train_mask=train_mask)
        query_pts = query_pts / query_scall
        train_pts = train_pts / train_scall
        return (query_pts, train_pts)

    def get_x_feature(self, img, mask=None, cache=False):
        """
        获取图像sift特征
        :param img:
        :param mask:
        :param cache: 是否使用缓存
        :return:
        """
        if cache:
            h, w = img.shape[:2]
            mid = int(w / 2)
            img_key = np.sum(img[:, mid - 5:mid + 5, :])
            x_feature = feature_cache.get(img_key, None)
            if x_feature is None:
                x_feature = self.sift.detectAndCompute(img, mask=mask)
                feature_cache[img_key] = x_feature
        else:
            x_feature = self.sift.detectAndCompute(img, mask=mask)
        kp, des = x_feature
        return (kp, des)


class BorderCardLocater:

    def __init__(self, save_debug=False, save_path=None):
        """
        基于边缘信息进行卡片抽取
        :param save_debug:
        :param save_path:
        """
        self.save_debug = save_debug
        if save_debug:
            fu.check_dir(save_path, True)
        self.save_path = save_path

    @timer
    def locate(self, query_img, train_img, **kwargs):
        qh, qw = query_img.shape[:2]
        verticles = self.find_contours(train_img)
        q2t_mat = self.find_homo_graphy(query_img, verticles)
        t2q_mat = np.mat(q2t_mat).I
        result_img = cv2.warpPerspective(train_img, t2q_mat, (qw, qh), borderValue=[255, 255, 255], borderMode=(cv2.BORDER_REPLICATE))
        if self.save_debug:
            img_combine = iu.img_joint_with_colorgap((train_img, result_img), axis=1,
              align=0,
              gap=2,
              gap_color=[
             255, 0, 0])
            iu.save_result(img_combine, self.save_path, 'border_match_transform.jpg')
        return (
         result_img, t2q_mat, verticles)

    def find_homo_graphy(self, img, points):
        h, w = img.shape[:2]
        points = np.squeeze(points)
        points_sort = sorted(points, key=(lambda x: np.sum(x)))
        lt, lb, rt, rb = points_sort
        if lb[0] > rt[0]:
            lb, rt = rt, lb
        query_pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        train_pts = np.float32([lt, lb, rb, rt]).reshape(-1, 1, 2)
        q2t_mat, _ = cv2.findHomography(query_pts, train_pts, cv2.RANSAC, 5.0)
        return q2t_mat

    def find_contours(self, img):
        img = img.copy()
        img = cv2.blur(img, (5, 5))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_canny = cv2.Canny(img_gray, 50, 100, apertureSize=3)
        dilate_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        img_canny = cv2.dilate(img_canny, dilate_rect, iterations=2)
        _, cnts, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=(cv2.contourArea), reverse=True)
        cnt = cnts[0]
        ret = cv2.boundingRect(cnt)
        _, _, h, w = ret
        epsilon = min(h, w) * 0.5
        convex_cnt = cv2.convexHull(cnt, clockwise=True)
        verticles = cv2.approxPolyDP(convex_cnt, epsilon, True)
        if self.save_debug:
            print('Find verticle number = {:d}'.format(len(verticles)))
            img_bk = img.copy()
            img_gray = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(img_gray, cnts, -1, (0, 255, 0), 2)
            cv2.drawContours(img_bk, [cnt], -1, (0, 255, 0), 2)
            cv2.drawContours(img_bk, [convex_cnt], -1, (255, 0, 0), 3)
            cv2.drawContours(img_bk, [verticles], -1, (0, 0, 255), 3)
            img_combine = iu.img_joint((img, img_gray, img_canny))
            result_img = iu.img_joint((img_bk, img_gray, img_canny))
            iu.write_image(result_img, self.save_path, 'img_border_find.jpg')
        if len(verticles) != 4:
            raise CardLocateException('边缘检测到顶点数不为4,检测到:{:d}'.format(len(verticles)))
        check_area_size(img.shape, verticles)
        return verticles


def check_area_size(shape, dst):
    """
    检测识别到的身份证区域是否有效
    :param shape: 图片尺寸 [h,w]
    :param dst:  标记身份证区域的多边形顶点
    :return:
    """
    ori_area = shape[0] * shape[1]
    card_area = cv2.contourArea(dst)
    if card_area < ori_area / 8 or card_area > ori_area * 1.5:
        raise CardLocateException('识别到卡片面积占比过大或过小: %.2f' % (card_area / ori_area))
    max_cor = np.max(dst, axis=0)
    min_cor = np.min(dst, axis=0)
    (width, height), = max_cor - min_cor
    if width < shape[1] / 4 or width > shape[1] * 1.5:
        raise CardLocateException('识别到卡片宽度过大或过小: %.2f' % (width / shape[1]))
    if height < shape[0] / 5 or height > shape[0] * 1.5:
        raise CardLocateException('识别到卡片高度过大或过小: %.2f' % (height / shape[0]))


def check_contour_inside(img, contour, padding=5):
    """
    检查边缘是否在图像外
    :param img:
    :param contour:
    :param padding
    :return:
    """
    h, w = img.shape[:2]
    contour = np.squeeze(contour)
    x_flag = (contour[:, 0] < w + padding) & (contour[:, 0] > -padding)
    y_flag = (contour[:, 1] < h + padding) & (contour[:, 1] > -padding)
    in_border = x_flag & y_flag
    return in_border


if __name__ == '__main__':
    pass