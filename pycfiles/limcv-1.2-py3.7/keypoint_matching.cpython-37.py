# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/limcv/keypoint_matching.py
# Compiled at: 2019-12-11 09:22:26
# Size of source mod 2**32: 1405 bytes
"""
Detect keypoints with KAZE/AKAZE/BRISK/ORB.
No need for opencv-contrib module.
"""
import cv2
from .keypoint_base import KeypointMatching

class KAZEMatching(KeypointMatching):
    __doc__ = 'KAZE Matching.'


class BRISKMatching(KeypointMatching):
    __doc__ = 'BRISK Matching.'
    METHOD_NAME = 'BRISK'

    def init_detector(self):
        """Init keypoint detector object."""
        self.detector = cv2.BRISK_create()
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING)


class AKAZEMatching(KeypointMatching):
    __doc__ = 'AKAZE Matching.'
    METHOD_NAME = 'AKAZE'

    def init_detector(self):
        """Init keypoint detector object."""
        self.detector = cv2.AKAZE_create()
        self.matcher = cv2.BFMatcher(cv2.NORM_L1)


class ORBMatching(KeypointMatching):
    __doc__ = 'ORB Matching.'
    METHOD_NAME = 'ORB'

    def init_detector(self):
        """Init keypoint detector object."""
        self.detector = cv2.ORB_create()
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING)