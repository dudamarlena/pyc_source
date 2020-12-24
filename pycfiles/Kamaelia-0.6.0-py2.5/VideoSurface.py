# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/Pygame/VideoSurface.py
# Compiled at: 2008-10-19 12:19:52
"""====================
Pygame Video Surface
====================

Displays uncompressed RGB video data on a pygame surface using the Pygame
Display service.

Example Usage
-------------

Read raw YUV data from a file, convert it to interleaved RGB  and display it
using VideoSurface::

    imagesize = (352, 288)        # "CIF" size video
    fps = 15                      # framerate of video
    
    Pipeline(ReadFileAdapter("raw352x288video.yuv", ...other args...),
             RawYUVFramer(imagesize),
             MessageRateLimit(messages_per_second=fps, buffer=fps*2),
             ToRGB_interleaved(),
             VideoSurface(),
            ).activate()

RawYUVFramer is needed to frame raw YUV data into individual video frames.
ToRGB_interleaved is needed to convert the 3 planes of Y, U and V data to a
single plane containing RGB data interleaved (R, G, B, R, G, B, R, G, B, ...)

How does it work?
-----------------

The component waits to receive uncompressed video frames from its "inbox" inbox.

The frames must be encoded as dictionary objects in the format described below.

When the first frame is received, the component notes the size and pixel format
of the video data and requests an appropriate surface from the
Pygame Display service component, to which video can be rendered.

NOTE: Currently the only supported pixelformat is "RGB_interleaved".

When subsequent frames of video are received the rgb data is rendered to the
surface and the Pygame Display service is notified that the surface needs
redrawing.

At present, VideoSurface cannot cope with a change of pixel format or video
size mid sequence.

=========================
UNCOMPRESSED FRAME FORMAT
=========================

Uncompresed video frames must be encoded as dictionaries. VideoSurface requires
the following entries::

    {
      "rgb" : rgbdata                    # a string containing RGB video data
      "size" : (width, height)           # in pixels
      "pixformat" : "RGB_interleaved"    # format of raw video data
    }

"""
from Axon.Component import component
from Axon.Ipc import producerFinished, shutdownMicroprocess
from Axon.Ipc import WaitComplete
from Kamaelia.UI.GraphicDisplay import PygameDisplay
import pygame

class VideoSurface(component):
    """    VideoSurface([position]) -> new VideoSurface component

    Displays a pygame surface using the Pygame Display service component, for
    displaying RGB video frames sent to its "inbox" inbox.
    
    The surface is sized and configured by the first frame of (uncompressed)
    video data is receives.
    

    Keyword arguments:

   - position      -- (x,y) pixels position of top left corner (default=(0,0))
    """
    Inboxes = {'inbox': 'Video frame data structures containing RGB data', 'control': 'Shutdown messages: shutdownMicroprocess or producerFinished', 
       'callback': 'Receive callbacks from Pygame Display'}
    Outboxes = {'outbox': 'NOT USED', 
       'signal': 'Shutdown signalling: shutdownMicroprocess or producerFinished', 
       'display_signal': 'Outbox used for sending signals of various kinds to the display service'}

    def __init__(self, position=None):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(VideoSurface, self).__init__()
        self.display = None
        self.size = None
        self.pixformat = None
        if position is not None:
            self.position = position
        else:
            self.position = (0, 0)
        return

    def shutdown(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (shutdownMicroprocess, producerFinished)):
                return True

        return False

    def waitBox(self, boxname):
        """Generator. yield's 1 until data is ready on the named inbox."""
        waiting = True
        while waiting:
            if self.dataReady(boxname):
                return
            else:
                yield 1

    def formatChanged(self, frame):
        """Returns True if frame size or pixel format is new/different for this frame."""
        return frame['size'] != self.size or frame['pixformat'] != self.pixformat

    def main(self):
        """Main loop."""
        displayservice = PygameDisplay.getDisplayService()
        self.link((self, 'display_signal'), displayservice)
        while 1:
            frame = False
            while not frame:
                if self.dataReady('inbox'):
                    frame = self.recv('inbox')
                    if self.shutdown():
                        return
                if not self.anyReady():
                    self.pause()
                yield 1

            if self.formatChanged(frame):
                if self.display:
                    raise "Can't cope with a format change yet!"
                self.size = frame['size']
                self.pixformat = frame['pixformat']
                if self.pixformat != 'RGB_interleaved':
                    raise "Can't cope with any pixformat other than RGB_interleaved"
                dispRequest = {'DISPLAYREQUEST': True, 'callback': (
                              self, 'callback'), 
                   'size': self.size, 
                   'position': self.position}
                self.send(dispRequest, 'display_signal')
                yield WaitComplete(self.waitBox('callback'))
                self.display = self.recv('callback')
            image = pygame.image.fromstring(frame['rgb'], frame['size'], 'RGB', False)
            self.display.blit(image, (0, 0))
            self.send({'REDRAW': True, 'surface': self.display}, 'display_signal')
            if self.shutdown():
                return
            if not self.anyReady():
                self.pause()
                yield 1


__kamaelia_components__ = (
 VideoSurface,)
if __name__ == '__main__':
    from Kamaelia.Chassis.Pipeline import Pipeline
    from Kamaelia.File.ReadFileAdaptor import ReadFileAdaptor
    from Kamaelia.Codec.RawYUVFramer import RawYUVFramer
    from Kamaelia.UI.Pygame.VideoOverlay import VideoOverlay
    from Kamaelia.Video.PixFormatConversion import ToYUV420_planar
    from Kamaelia.Video.PixFormatConversion import ToRGB_interleaved
    from Kamaelia.Codec.Dirac import DiracDecoder
    Pipeline(ReadFileAdaptor('/data/dirac-video/snowboard-jum-352x288x75.dirac.drc', readmode='bitrate', bitrate=18247680), DiracDecoder(), ToRGB_interleaved(), ToYUV420_planar(), ToRGB_interleaved(), VideoSurface((200,
                                                                                                                                                                                                                       100))).run()