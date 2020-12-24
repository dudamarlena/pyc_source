# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sail_utils\tests\cv\head\test_detection.py
# Compiled at: 2020-03-27 07:55:00
# Size of source mod 2**32: 403 bytes
"""
test module for detection
"""
from sail_utils.cv.head.detection import _Mapper

def test_mapper():
    """
    test _Calibrator class
    :return:
    """
    calibrator = _Mapper(100, 50)
    detected_box = [25, 50, 75, 100]
    expected_box = [50, 100, 150, 200]
    calibrated_box = calibrator(detected_box)
    assert expected_box == calibrated_box