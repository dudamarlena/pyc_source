# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bullseye/dc1394_capture.py
# Compiled at: 2012-03-02 05:34:47
from traits.api import Float, Int, Str, Range, Instance, on_trait_change
from pydc1394 import camera2 as dc1394
import logging
from .capture import BaseCapture

class DC1394Capture(BaseCapture):
    cam = Instance(dc1394.Camera)
    pixelsize = Float(3.75)
    maxval = Int(255)
    mode_name = Str('1280x960_Y8')

    def __init__(self, guid=None, **k):
        self.cam = dc1394.Camera(guid)
        super(DC1394Capture, self).__init__(**k)

    def setup(self):
        self.cam.setup(active=False, exposure=None, brightness=None)
        self.cam.setup(active=True, mode='manual', absolute=True, framerate=None, gain=None, shutter=None)
        self.mode = self.cam.modes_dict[self.mode_name]
        self.cam.mode = self.mode
        self.cam.rate = 7.5
        self.width = int(self.mode.image_size[0])
        self.height = int(self.mode.image_size[1])
        self.min_shutter = 1e-05
        self.max_shutter = 0.1
        self.add_trait('shutter', Range(self.min_shutter, self.max_shutter, self.cam.shutter.absolute))
        self.max_framerate = 10
        self.add_trait('framerate', Range(1, 10, int(self.cam.framerate.absolute)))
        self.add_trait('gain', Range(0, round(self.cam.gain.absolute_range[1], 0), self.cam.gain.absolute))
        return

    def start(self):
        try:
            self.cam.start_capture()
        except dc1394.DC1394Error:
            logging.debug('camera capture already running')

        self.cam.start_video()

    def stop(self):
        self.cam.stop_video()
        self.cam.stop_capture()

    @on_trait_change('framerate')
    def _do_framerate(self, val):
        self.cam.framerate.absolute = val

    @on_trait_change('shutter')
    def _do_shutter(self, val):
        self.cam.shutter.absolute = val

    @on_trait_change('gain')
    def _do_gain(self, val):
        self.cam.gain.absolute = val

    def dequeue(self):
        im = None
        im_ = self.cam.dequeue()
        while im_ is not None:
            if im is not None:
                im.enqueue()
                logging.debug('dropped frame')
            im = im_
            im_ = self.cam.dequeue(poll=True)

        return im

    def enqueue(self, im):
        im.enqueue()

    def flush(self):
        self.cam.flush()