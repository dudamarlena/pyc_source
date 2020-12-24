# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/theo/Documents/Projects/webcam-streamer/streamer/camera.py
# Compiled at: 2015-02-18 21:50:26
import re, subprocess
from StringIO import StringIO
import cv2
from PIL import Image

def list_camera_ids():
    cameras = subprocess.Popen(['ls', '/dev/video*'], stdout=subprocess.PIPE).communicate()[0]
    return re.findall('\\d+', cameras)


class Camera(object):

    def __init__(self, camera_id, size, fps):
        self.cam = cv2.VideoCapture(int(camera_id))
        self.cam.set(cv2.CAP_PROP_FPS, fps)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    def get_frame(self):
        if not self.cam.isOpened():
            return ''
        ret, frame = self.cam.read()
        image = Image.fromarray(frame)
        buf = StringIO()
        image.save(buf, 'JPEG')
        return buf.getvalue()