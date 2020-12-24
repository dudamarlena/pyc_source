# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webcam/camera.py
# Compiled at: 2017-02-15 07:37:04
# Size of source mod 2**32: 2107 bytes
from threading import Thread
import time
from webcam.config import Config
from webcam.data.file import File
from webcam.data.stream_buffer import StreamBuffer
from webcam.jobs.converting_job import ConvertingJob
from webcam.services.video_stream import VideoStream
from imutils.video import FPS

class Camera:

    def __init__(self):
        self.stream = VideoStream()
        self.file = File()
        self.converting_job = ConvertingJob()
        self.is_recording = False
        self.is_camera_open = False
        self.buffer = StreamBuffer()
        self.file_name = None
        self.fps = FPS()

    def is_open(self):
        return self.is_camera_open

    def access(self):
        self.is_camera_open = True
        Thread(target=self._Camera__start_reading_frames).start()

    def release(self):
        self.is_camera_open = False

    def start_recording(self):
        if self.is_open():
            print('Start RECORDING Video')
            self.fps.start()
            self.stream.start()
            self.is_recording = True

    def stop_recording(self):
        print('Stop RECORDING Video')
        self.is_recording = False
        self.stream.stop()
        self.fps.stop()
        print('[INFO] elasped time: {:.2f}'.format(self.fps.elapsed()))
        print('[INFO] approx. FPS: {:.2f}'.format(self.fps.fps()))
        Config.VIDEO_FPS = self.fps.fps()
        self.file.create(self.file_name)
        self._Camera__write_frames()

    def create_file(self, name):
        self.file_name = name

    def __start_reading_frames(self):
        print('Start READING frames')
        while self.stream.is_open() and self.is_open():
            if self.is_recording:
                frame = self.stream.read()
                if frame is not None:
                    self.buffer.insert(frame)
                    self.fps.update()
                else:
                    continue

    def __write_frames(self):
        frames = self.buffer.get()
        self.file.write(frames)