# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\python\EasyVision\EasyVision\bin\performance_mp_stereo_calibrated.py
# Compiled at: 2019-01-19 08:31:43
from EasyVision.exceptions import *
from EasyVision.engine import *
from EasyVision.processors import *
from EasyVision.vision import *
import cv2, numpy as np
from tests.test_processors_mp_calibratedstereocamera import test_stereo_calibrated_mp, test_stereo_calibrated_mp_dummy
if __name__ == '__main__':
    test_stereo_calibrated_mp_dummy()
    test_stereo_calibrated_mp()