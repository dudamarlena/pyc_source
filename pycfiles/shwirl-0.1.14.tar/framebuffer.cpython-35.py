# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/gloo/framebuffer.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 9066 bytes
from .globject import GLObject
from .texture import Texture2D
from .wrappers import _check_valid, read_pixels
from .context import get_current_canvas
from ..ext.six import string_types

class RenderBuffer(GLObject):
    __doc__ = " Base class for render buffer object\n    \n    A render buffer can be in color, depth or stencil format. If this\n    format is not specified, it is set when attached to the FrameBuffer.\n    \n    Parameters\n    ----------\n    shape : tuple\n        The shape of the render buffer.\n    format : {None, 'color', 'depth', 'stencil'}\n        The format of the render buffer. See resize.\n    resizeable : bool\n        Indicates whether texture can be resized\n    "
    _GLIR_TYPE = 'RenderBuffer'

    def __init__(self, shape=None, format=None, resizeable=True):
        GLObject.__init__(self)
        self._format = None
        self._resizeable = True
        self.resize(shape, format)
        self._resizeable = bool(resizeable)

    @property
    def shape(self):
        """RenderBuffer shape """
        return self._shape

    @property
    def format(self):
        """ RenderBuffer format """
        return self._format

    def resize(self, shape, format=None):
        """ Set the render-buffer size and format

        Parameters
        ----------
        shape : tuple of integers
            New shape in yx order. A render buffer is always 2D. For
            symmetry with the texture class, a 3-element tuple can also
            be given, in which case the last dimension is ignored.
        format : {None, 'color', 'depth', 'stencil'}
            The buffer format. If None, the current format is maintained. 
            If that is also None, the format will be set upon attaching
            it to a framebuffer. One can also specify the explicit enum:
            GL_RGB565, GL_RGBA4, GL_RGB5_A1, GL_DEPTH_COMPONENT16, or
            GL_STENCIL_INDEX8
        """
        if not self._resizeable:
            raise RuntimeError('RenderBuffer is not resizeable')
        if not (isinstance(shape, tuple) and len(shape) in (2, 3)):
            raise ValueError('RenderBuffer shape must be a 2/3 element tuple')
        if format is None:
            format = self._format
        else:
            if isinstance(format, int):
                pass
            else:
                if isinstance(format, string_types):
                    if format not in ('color', 'depth', 'stencil'):
                        raise ValueError('RenderBuffer format must be "color", "depth" or "stencil", not %r' % format)
                else:
                    raise ValueError('Invalid RenderBuffer format: %r' % format)
        self._shape = tuple(shape[:2])
        self._format = format
        if self._format is not None:
            self._glir.command('SIZE', self._id, self._shape, self._format)


class FrameBuffer(GLObject):
    __doc__ = ' Frame buffer object\n    \n    Parameters\n    ----------\n    \n    color : RenderBuffer (optional)\n        The color buffer to attach to this frame buffer\n    depth : RenderBuffer (optional)\n        The depth buffer to attach to this frame buffer\n    stencil : RenderBuffer (optional)\n        The stencil buffer to attach to this frame buffer\n    '
    _GLIR_TYPE = 'FrameBuffer'

    def __init__(self, color=None, depth=None, stencil=None):
        GLObject.__init__(self)
        self._color_buffer = None
        self._depth_buffer = None
        self._stencil_buffer = None
        if color is not None:
            self.color_buffer = color
        if depth is not None:
            self.depth_buffer = depth
        if stencil is not None:
            self.stencil_buffer = stencil

    def activate(self):
        """ Activate/use this frame buffer.
        """
        self._glir.command('FRAMEBUFFER', self._id, True)
        canvas = get_current_canvas()
        if canvas is not None:
            canvas.context.glir.associate(self.glir)

    def deactivate(self):
        """ Stop using this frame buffer, the previous framebuffer will be
        made active.
        """
        self._glir.command('FRAMEBUFFER', self._id, False)

    def __enter__(self):
        self.activate()
        return self

    def __exit__(self, t, val, trace):
        self.deactivate()

    def _set_buffer(self, buffer, format):
        formats = ('color', 'depth', 'stencil')
        assert format in formats
        if isinstance(buffer, RenderBuffer):
            if buffer.format is None:
                buffer.resize(buffer.shape, format)
        elif buffer.format in formats and buffer.format != format:
            raise ValueError('Cannot attach a %s buffer as %s buffer.' % (
             buffer.format, format))
        if buffer is None:
            setattr(self, '_%s_buffer' % format, None)
            self._glir.command('ATTACH', self._id, format, 0)
        else:
            if isinstance(buffer, (Texture2D, RenderBuffer)):
                self.glir.associate(buffer.glir)
                setattr(self, '_%s_buffer' % format, buffer)
                self._glir.command('ATTACH', self._id, format, buffer.id)
            else:
                raise TypeError('Buffer must be a RenderBuffer, Texture2D or None. (got %s)' % type(buffer))

    @property
    def color_buffer(self):
        """Color buffer attachment"""
        return self._color_buffer

    @color_buffer.setter
    def color_buffer(self, buffer):
        self._set_buffer(buffer, 'color')

    @property
    def depth_buffer(self):
        """Depth buffer attachment"""
        return self._depth_buffer

    @depth_buffer.setter
    def depth_buffer(self, buffer):
        self._set_buffer(buffer, 'depth')

    @property
    def stencil_buffer(self):
        """Stencil buffer attachment"""
        return self._stencil_buffer

    @stencil_buffer.setter
    def stencil_buffer(self, buffer):
        self._set_buffer(buffer, 'stencil')

    @property
    def shape(self):
        """ The shape of the Texture/RenderBuffer attached to this FrameBuffer
        """
        if self.color_buffer is not None:
            return self.color_buffer.shape[:2]
        if self.depth_buffer is not None:
            return self.depth_buffer.shape[:2]
        if self.stencil_buffer is not None:
            return self.stencil_buffer.shape[:2]
        raise RuntimeError('FrameBuffer without buffers has undefined shape')

    def resize(self, shape):
        """ Resize all attached buffers with the given shape

        Parameters
        ----------
        shape : tuple of two integers
            New buffer shape (h, w), to be applied to all currently
            attached buffers. For buffers that are a texture, the number
            of color channels is preserved.
        """
        if not (isinstance(shape, tuple) and len(shape) == 2):
            raise ValueError('RenderBuffer shape must be a 2-element tuple')
        for buf in (self.color_buffer, self.depth_buffer, self.stencil_buffer):
            if buf is None:
                pass
            else:
                shape_ = shape
                if isinstance(buf, Texture2D):
                    shape_ = shape + (self.color_buffer.shape[(-1)],)
                buf.resize(shape_, buf.format)

    def read(self, mode='color', alpha=True):
        """ Return array of pixel values in an attached buffer
        
        Parameters
        ----------
        mode : str
            The buffer type to read. May be 'color', 'depth', or 'stencil'.
        alpha : bool
            If True, returns RGBA array. Otherwise, returns RGB.
        
        Returns
        -------
        buffer : array
            3D array of pixels in np.uint8 format. 
            The array shape is (h, w, 3) or (h, w, 4), with the top-left 
            corner of the framebuffer at index [0, 0] in the returned array.
        
        """
        _check_valid('mode', mode, ['color', 'depth', 'stencil'])
        buffer = getattr(self, mode + '_buffer')
        h, w = buffer.shape[:2]
        return read_pixels((0, 0, w, h), alpha=alpha)