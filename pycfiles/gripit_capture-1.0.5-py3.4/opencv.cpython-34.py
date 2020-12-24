# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webcam/services/opencv.py
# Compiled at: 2017-01-06 05:25:27
# Size of source mod 2**32: 294 bytes
import cv2

class OpenCV:

    def __init__(self):
        self.capture = None

    def get_capture(self):
        if not self.capture:
            self.capture = cv2.VideoCapture(0)
        return self.capture

    def release(self):
        self.capture.release()
        self.capture = None