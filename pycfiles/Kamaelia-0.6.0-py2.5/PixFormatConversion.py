# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Video/PixFormatConversion.py
# Compiled at: 2008-10-19 12:19:52
"""===========================================
Converting the pixel format of video frames
===========================================

These components convert the pixel format of video frames, for example, from
interleaved RGB to planar YUV 420.

Example Usage
-------------

Decoding a Dirac encoded video file, then converting it to RGB for display on
a pygame display surface::

    Pipeline( RateControlledFileReader("video.drc",readmode="bytes", rate=100000),
              DiracDecoder(),
              ToRGB_interleaved(),
              VideoSurface(),
            ).run()

Which component for which conversion?
-------------------------------------

The components here are currently capable of the following pixel format
conversions:

=====================  =====================  ===========================
From                   To                     Which component?
=====================  =====================  ===========================
"RGB_interleaved"      "RGB_interleaved"      ToRGB_interleaved
"YUV420_planar"        "RGB_interleaved"      ToRGB_interleaved
"YUV422_planar"        "RGB_interleaved"      ToRGB_interleaved

"RGB_interleaved"      "YUV420_planar"        ToYUV420_planar
"YUV420_planar"        "YUV420_planar"        ToYUV420_planar
=====================  =====================  ===========================

More details
------------

Send video frames to the "inbox" inbox of these components. They will be
converted to the destination pixel format and sent out of the "outbox" outbox.
Video frames are dictionaries, they must have the following keys:
    
    * "rgb" or "yuv"  -- containing the pixel data
    * "pixformat"     -- the pixel format
    * "size"          -- (width,height) in pixels

Any other fields will be transparently passed through, unmodified.

These components support sending data out of its outbox to a size limited inbox.
If the size limited inbox is full, these components will pause until able to
send out the data. Data will not be consumed from the inbox if these components
are waiting to send to the outbox.

If a producerFinished message is received on the "control" inbox, these components
will complete converting and frames pending in its inbox, and finish sending any
resulting data to its outbox. They will then send the producerFinished message
on out of its "signal" outbox and terminate.

If a shutdownMicroprocess message is received on the "control" inbox, these
components will immediately send it on out of its "signal" outbox and immediately
terminate. It will not complete processing, or sending on any pending data.

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.AxonExceptions import noSpaceInBox
from Kamaelia.Support.Optimised.Video.PixFormatConvert import rgbi_to_yuv420p
from Kamaelia.Support.Optimised.Video.PixFormatConvert import yuv420p_to_rgbi
from Kamaelia.Support.Optimised.Video.PixFormatConvert import yuv422p_to_rgbi

class ToRGB_interleaved(component):
    """"    ToRGB_interleaved() -> new ToRGB_interleaved component.
    
    Converts video frames sent to its "inbox" inbox, to "RGB_interleaved" pixel
    format and sends them out of its "outbox"
    
    Supports conversion from:
    
    * YUV420_planar
    * YUV422_planar
    * RGB_interleaved (passthrough)
    """
    Inboxes = {'inbox': 'Video frame', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'RGB_interleaved pixel format video frame', 'signal': 'Shutdown signalling'}

    def handleControl(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished, shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)

    def waitSend(self, data, boxname):
        while 1:
            try:
                self.send(data, boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise 'STOP'
                self.pause()
                yield 1
                if self.mustStop():
                    raise 'STOP'

    def main(self):
        """Main loop."""
        self.shutdownMsg = None
        try:
            while 1:
                while self.dataReady('inbox'):
                    frame = self.recv('inbox')
                    (Y, U, V) = frame['yuv']
                    (W, H) = frame['size']
                    newframe = {'size': (
                              W, H), 
                       'pixformat': 'RGB_interleaved'}
                    if frame['pixformat'] == 'RGB_interleaved':
                        for _ in self.waitSend(frame, 'outbox'):
                            yield _

                    if frame['pixformat'] == 'YUV420_planar':
                        newframe['rgb'] = yuv420p_to_rgbi(Y, U, V, W, H)
                    if frame['pixformat'] == 'YUV422_planar':
                        newframe['rgb'] = yuv422p_to_rgbi(Y, U, V, W, H)
                    for key in frame.keys():
                        if key not in newframe:
                            newframe[key] = frame[key]

                    for _ in self.waitSend(newframe, 'outbox'):
                        yield _

                if self.canStop():
                    raise 'STOP'
                self.pause()
                yield 1

        except 'STOP':
            self.send(self.shutdownMsg, 'signal')

        return


class ToYUV420_planar(component):
    """"    ToYUV420_planar() -> new ToYUV420_planar component.
    
    Converts video frames sent to its "inbox" inbox, to "ToYUV420_planar" pixel
    format and sends them out of its "outbox"
    
    Supports conversion from:
    
    * RGB_interleaved
    * YUV420_planar (passthrough)
    """
    Inboxes = {'inbox': 'Video frame', 'control': 'Shutdown signalling'}
    Outboxes = {'outbox': 'YUV420_planar pixel format video frame', 'signal': 'Shutdown signalling'}

    def handleControl(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, producerFinished) and not isinstance(self.shutdownMsg, shutdownMicroprocess):
                self.shutdownMsg = msg
            elif isinstance(msg, shutdownMicroprocess):
                self.shutdownMsg = msg

    def canStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, (producerFinished, shutdownMicroprocess))

    def mustStop(self):
        self.handleControl()
        return isinstance(self.shutdownMsg, shutdownMicroprocess)

    def waitSend(self, data, boxname):
        while 1:
            try:
                self.send(data, boxname)
                return
            except noSpaceInBox:
                if self.mustStop():
                    raise 'STOP'
                self.pause()
                yield 1
                if self.mustStop():
                    raise 'STOP'

    def main(self):
        """Main loop."""
        self.shutdownMsg = None
        try:
            while 1:
                while self.dataReady('inbox'):
                    frame = self.recv('inbox')
                    if frame['pixformat'] == 'YUV420_planar':
                        for _ in self.waitSend(frame, 'outbox'):
                            yield _

                    elif frame['pixformat'] == 'RGB_interleaved':
                        rgb = frame['rgb']
                        (W, H) = frame['size']
                        newframe = {'yuv': rgbi_to_yuv420p(rgb, W, H), 
                           'size': (
                                  W, H), 
                           'pixformat': 'YUV420_planar', 
                           'chroma_size': (
                                         W / 2, H / 2)}
                        for key in frame.keys():
                            if key not in newframe and key != 'rgb':
                                newframe[key] = frame[key]

                        for _ in self.waitSend(newframe, 'outbox'):
                            yield _

                if self.canStop():
                    raise 'STOP'
                self.pause()
                yield 1

        except 'STOP':
            self.send(self.shutdownMsg, 'signal')

        return


__kamaelia_components__ = (ToRGB_interleaved, ToYUV420_planar)