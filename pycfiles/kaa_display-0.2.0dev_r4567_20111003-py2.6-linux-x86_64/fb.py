# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/display/fb.py
# Compiled at: 2008-12-02 10:36:36
__all__ = [
 'PAL_768x576', 'PAL_800x600', 'NTSC_640x480', 'NTSC_768x576',
 'NTSC_800x600', 'Framebuffer']
import _FBmodule as fb
PAL_768x576 = (768, 576, 768, 576, 0, 0, 0, 0, 38400, 20, 10, 30, 10, 10, 34, 19, 0)
PAL_800x600 = (800, 600, 800, 600, 0, 0, 0, 0, 38400, 48, 24, 70, 32, 2, 40, 19, 0)
NTSC_640x480 = (640, 480, 640, 480, 0, 0, 0, 0, 35000, 36, 6, 22, 22, 1, 46, 0, 0)
NTSC_768x576 = (768, 576, 768, 576, 0, 0, 0, 0, 35000, 36, 6, 39, 10, 4, 46, 0, 0)
NTSC_800x600 = (800, 600, 800, 600, 0, 0, 0, 0, 39721, 48, 24, 80, 32, 2, 40, 1, 0)
FB_800x600 = (800, 600, 800, 600, 0, 0, 0, 0, 20203, 160, 16, 21, 1, 80, 3, 0, 0)
FB_1024x768 = (1024, 768, 1024, 768, 0, 0, 0, 0, 13334, 104, 24, 29, 3, 136, 6, 0,
               0)
FB_1280x1024 = (1280, 1024, 1280, 3264, 0, 0, 0, 0, 7414, 232, 64, 38, 1, 112, 3, 0,
                0)
FB_1600x1200 = (1600, 1200, 1600, 1200, 0, 0, 0, 0, 6411, 256, 32, 52, 10, 160, 8,
                0, 0)

class _Framebuffer(object):
    """
    Basic framebuffer class.
    The 'mode' argument can either be a size (width, height) matching one of
    the specified framebuffer resolutions, a list for fbset or None. If set to
    None, the current framebuffer size will be used.
    """

    def __init__(self, mode=None):
        self.signals = []
        if mode:
            if len(mode) == 2:
                mode = globals()[('FB_%sx%s' % mode)]
            fb.open(mode)
        else:
            fb.open()

    def info(self):
        """
        Return some basic informations about the frambuffer.
        """
        return fb.info()

    def get_id(self):
        """
        Fake id function that does not return a windows id but returns a
        string that would identify this as framebuffer.
        """
        return 'fb0'

    def size(self):
        """
        Return the size of the framebuffer.
        """
        return fb.size()

    def __del__(self):
        fb.close()


class Framebuffer(_Framebuffer):
    """
    Frambuffer using an imlib2 image for drawing
    The 'mode' argument can either be a size (width, height) matching one of
    the specified framebuffer resolutions, a list for fbset or None. If set to
    None, the current framebuffer size will be used.
    """

    def __init__(self, mode=None):
        _Framebuffer.__init__(self, mode)
        import kaa.imlib2
        self.image = kaa.imlib2.new(fb.size())

    def set_image(self, image):
        """
        Set an imlib2 image to the frambuffer. The size of the image must match
        the current framebuffer resolution.
        """
        if (
         image.width, image.height) != fb.size():
            raise AttributeError('Invalid image size')
        self.image = image

    def blend(self, src, src_pos=(0, 0), dst_pos=(0, 0)):
        """
        Blend an imlib2 image to the framebuffer.
        """
        self.image.blend(src, src_pos=src_pos, dst_pos=dst_pos)

    def update(self):
        """
        Update the framebuffer.
        """
        fb.update(self.image._image)