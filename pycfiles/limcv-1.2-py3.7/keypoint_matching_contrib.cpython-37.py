# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/limcv/keypoint_matching_contrib.py
# Compiled at: 2019-12-11 09:22:26
# Size of source mod 2**32: 5482 bytes
"""
Detect keypoints with BRIEF/SIFT/SURF.
Need opencv-contrib module.
"""
import cv2
from .error import *
from .keypoint_base import KeypointMatching

def check_cv_version_is_new():
    """opencv版本是3.0或4.0以上, API接口与2.0的不同."""
    if cv2.__version__.startswith('3.') or cv2.__version__.startswith('4.'):
        return True
    return False


class BRIEFMatching(KeypointMatching):
    __doc__ = 'FastFeature Matching.'
    METHOD_NAME = 'BRIEF'

    def init_detector(self):
        """Init keypoint detector object."""
        if check_cv_version_is_new():
            try:
                self.star_detector = cv2.xfeatures2d.StarDetector_create()
                self.brief_extractor = cv2.xfeatures2d.BriefDescriptorExtractor_create()
            except:
                import traceback
                traceback.print_exc()
                print('to use %s, you should build contrib with opencv3.0' % self.METHOD_NAME)
                raise NoModuleError('There is no %s module in your OpenCV environment !' % self.METHOD_NAME)

        else:
            self.star_detector = cv2.FeatureDetector_create('STAR')
            self.brief_extractor = cv2.DescriptorExtractor_create('BRIEF')
        self.matcher = cv2.BFMatcher(cv2.NORM_L1)

    def get_keypoints_and_descriptors(self, image):
        """获取图像特征点和描述符."""
        kp = self.star_detector.detect(image, None)
        keypoints, descriptors = self.brief_extractor.compute(image, kp)
        return (keypoints, descriptors)

    def match_keypoints(self, des_sch, des_src):
        """Match descriptors (特征值匹配)."""
        return self.matcher.knnMatch(des_sch, des_src, k=2)


class SIFTMatching(KeypointMatching):
    __doc__ = 'SIFT Matching.'
    METHOD_NAME = 'SIFT'
    FLANN_INDEX_KDTREE = 0

    def init_detector(self):
        """Init keypoint detector object."""
        if check_cv_version_is_new():
            try:
                self.detector = cv2.xfeatures2d.SIFT_create(edgeThreshold=10)
            except:
                import traceback
                traceback.print_exc()
                raise NoModuleError('There is no %s module in your OpenCV environment, need contribmodule!' % self.METHOD_NAME)

        else:
            self.detector = cv2.SIFT(edgeThreshold=10)
        self.matcher = cv2.FlannBasedMatcher({'algorithm':self.FLANN_INDEX_KDTREE,  'trees':5}, dict(checks=50))

    def get_keypoints_and_descriptors(self, image):
        """获取图像特征点和描述符."""
        keypoints, descriptors = self.detector.detectAndCompute(image, None)
        return (keypoints, descriptors)

    def match_keypoints(self, des_sch, des_src):
        """Match descriptors (特征值匹配)."""
        return self.matcher.knnMatch(des_sch, des_src, k=2)


class SURFMatching(KeypointMatching):
    __doc__ = 'SURF Matching.'
    METHOD_NAME = 'SURF'
    UPRIGHT = 0
    HESSIAN_THRESHOLD = 400
    FLANN_INDEX_KDTREE = 0

    def init_detector(self):
        """Init keypoint detector object."""
        if check_cv_version_is_new():
            try:
                self.detector = cv2.xfeatures2d.SURF_create((self.HESSIAN_THRESHOLD), upright=(self.UPRIGHT))
            except:
                import traceback
                traceback.print_exc()
                raise NoModuleError('There is no %s module in your OpenCV environment, need contribmodule!' % self.METHOD_NAME)

        else:
            self.detector = cv2.SURF((self.HESSIAN_THRESHOLD), upright=(self.UPRIGHT))
        self.matcher = cv2.FlannBasedMatcher({'algorithm':self.FLANN_INDEX_KDTREE,  'trees':5}, dict(checks=50))

    def get_keypoints_and_descriptors(self, image):
        """获取图像特征点和描述符."""
        keypoints, descriptors = self.detector.detectAndCompute(image, None)
        return (keypoints, descriptors)

    def match_keypoints(self, des_sch, des_src):
        """Match descriptors (特征值匹配)."""
        return self.matcher.knnMatch(des_sch, des_src, k=2)