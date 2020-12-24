# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Codec/RawYUVFramer.py
# Compiled at: 2008-10-19 12:19:52
"""=========================
Raw YUV video data framer
=========================

This component takes a raw stream of YUV video data and breaks it into
invidual frames. It sends them out one at a time, tagged with relevant data
such as the frame size.

Many components that expect uncompressed video require it to be structured into
frames in this way, rather than as a raw stream of continuous data. This
component fulfills that requirement.

Example Usage
-------------

Reading and encoding raw video::

    imagesize = (352, 288)        # "CIF" size video
    
    Pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
             RawYUVFramer(imagesize),
             DiracEncoder(preset="CIF"),
            ).activate()

More Detail
-----------

Receives raw yuv video data, as strings on its "inbox" inbox.

Sends out individual frames packaged in a dictionary::

    {
      "yuv" : (y_data, u_data, v_data),  # a tuple of strings
      "size" : (width, height),          # in pixels
      "pixformat" : "YUV420_planar",     # raw video data format
    }

The component will terminate if it receives a shutdownMicroprocess or
producerFinished message on its "control" inbox. The message is passed on out of
the "signal" outbox.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess

class RawYUVFramer(component):
    """
    RawYUVFramer(size,pixformat) -> raw yuv video data framing component

    Creates a component that frames a raw stream of YUV video data into frames.

    Keyword arguments:
    
    - size       -- (width,height) size of a video frame in pixels
    - pixformat  -- raw video data format (default="YUV420_Planar")
    """

    def __init__(self, size, pixformat='YUV420_planar'):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(RawYUVFramer, self).__init__()
        self.size = size
        self.pixformat = pixformat
        ysize = size[0] * size[1]
        usize = ysize / 4
        vsize = usize
        self.planes = {'y': '', 'u': '', 'v': ''}
        self.sizes = {'y': ysize, 'u': usize, 'v': vsize}

    def main(self):
        """Main loop"""
        done = False
        while not done:
            while self.dataReady('inbox'):
                raw = self.recv('inbox')
                self.packAndSend(raw)

            if self.dataReady('control'):
                msg = self.recv('control')
                if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                    self.send(msg, 'signal')
                    done = True
            if not done:
                self.pause()
            yield 1

    def flushFrame(self):
        """Send out a frame, flushing buffers"""
        frame = {'pixformat': self.pixformat, 'size': self.size, 
           'yuv': (
                 self.planes['y'], self.planes['u'], self.planes['v'])}
        self.send(frame, 'outbox')
        self.planes['y'] = ''
        self.planes['u'] = ''
        self.planes['v'] = ''

    def packAndSend(self, raw):
        """
        packAndSend(raw) -> None
        
        Pack incoming raw data into y,u,v planes, and triggers a flush when all
        planes are full.
        """
        while raw:
            filled = False
            for plane in ['y', 'u', 'v']:
                remainder = self.sizes[plane] - len(self.planes[plane])
                filled = len(raw) >= remainder
                topupsize = min(len(raw), remainder)
                if topupsize:
                    self.planes[plane] += raw[:topupsize]
                    raw = raw[topupsize:]

            if filled:
                self.flushFrame()


__kamaelia_components__ = (
 RawYUVFramer,)