# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webcam/services/video_stream.py
# Compiled at: 2017-02-16 05:11:53
# Size of source mod 2**32: 892 bytes
from threading import Thread
from webcam.services.opencv import OpenCV

class VideoStream:

    def __init__(self):
        self.cv = OpenCV()
        self.stream = self.cv.get_capture()
        self.current_frame = None
        self.is_reading = True

    def is_open(self):
        return self.stream.isOpened()

    def start(self):
        self.is_reading = True
        self.stream.set(3, 1280)
        self.stream.set(4, 720)
        Thread(target=self._VideoStream__start_reading_frames).start()

    def stop(self):
        self.is_reading = False

    def release(self):
        self.cv.release()

    def read(self):
        frame = self.current_frame
        self.current_frame = None
        return frame

    def __start_reading_frames(self):
        while True:
            if self.is_reading is False:
                return
            _grabbed, self.current_frame = self.stream.read()