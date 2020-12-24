# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/image/mp4.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 949 bytes
from .. import log
from . import file_writer
try:
    import cv2
except:
    log.error('Could not import the OpenCV Python library - install it with:\n\n    $ pip install opencv-python\n')
    cv2 = None

class Writer(file_writer.FileWriter):

    def write(self, filename, frames, fps, show=False):
        fps = max(1, fps)
        out = None
        try:
            for image in frames:
                frame = cv2.imread(image)
                if show:
                    cv2.imshow('video', frame)
                if not out:
                    height, width, channels = frame.shape
                    fourcc = (cv2.VideoWriter_fourcc)(*'mp4v')
                    out = cv2.VideoWriter(filename, fourcc, 20, (width, height))
                out.write(frame)

        finally:
            out and out.release()
            cv2.destroyAllWindows()