# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/theo/Documents/Projects/webcam-streamer/streamer/camera_mock.py
# Compiled at: 2015-02-20 10:35:43
from StringIO import StringIO
from PIL import Image

def list_camera_ids():
    return [
     '0', '1']


class Camera(object):

    def __init__(self, camera_id, size, fps):
        self.width = size[0]
        self.height = size[1]

    def get_frame(self):
        image = Image.new('RGB', (self.width, self.height), 'black')
        buf = StringIO()
        image.save(buf, 'JPEG')
        return buf.getvalue()