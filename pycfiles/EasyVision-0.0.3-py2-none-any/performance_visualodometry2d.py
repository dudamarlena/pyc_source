# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\python\EasyVision\EasyVision\bin\performance_visualodometry2d.py
# Compiled at: 2019-01-18 08:14:51
from EasyVision.exceptions import *
from EasyVision.engine import *
from EasyVision.processors import *
from EasyVision.vision import *
import cv2, numpy as np
from tests.common import *
if __name__ == '__main__':
    common_test_visual_odometry_kitti('ORB', mp=False, ocl=False, debug=True, color=cv2.COLOR_BGR2GRAY, odometry_class=VisualOdometry2DEngine)