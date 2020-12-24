# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Projects\python\EasyVision\EasyVision\bin\mp.py
# Compiled at: 2018-12-29 05:20:15
from tests.test_processors_multiprocessing import test_capture_mp_images, test_capture_mp_camera
from tests.test_engine_mp_objectrecognition import test_match_mp_images_ORB
from tests.test_processors_calibratedstereocamera import test_stereo_calibrate, test_stereo_calibrated
from tests.test_processors_mp_calibratedstereocamera import test_stereo_calibrated_mp
if __name__ == '__main__':
    test_stereo_calibrated_mp()