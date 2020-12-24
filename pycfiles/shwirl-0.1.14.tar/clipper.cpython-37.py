# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/filters/clipper.py
# Compiled at: 2018-10-01 14:58:41
# Size of source mod 2**32: 2051 bytes
from ..shaders import Function
from ..transforms import NullTransform
from ...geometry import Rect
clip_frag = '\nvoid clip() {\n    vec4 pos = $fb_to_clip(gl_FragCoord);\n    if( pos.x < $view.x || pos.x > $view.y || \n        pos.y < $view.z || pos.y > $view.w ) {\n        discard;\n    }\n}\n'

class Clipper(object):
    __doc__ = 'Clips visual output to a rectangular region.\n    '

    def __init__(self, bounds=(0, 0, 1, 1), transform=None):
        self.clip_shader = Function(clip_frag)
        self.clip_expr = self.clip_shader()
        self.bounds = bounds
        if transform is None:
            transform = NullTransform()
        self._transform = None
        self.transform = transform

    @property
    def bounds(self):
        """The clipping boundaries.
        
        This must be a tuple (x, y, w, h) in a clipping coordinate system
        that is defined by the `transform` property.
        """
        return self._bounds

    @bounds.setter
    def bounds(self, b):
        self._bounds = Rect(b).normalized()
        b = self._bounds
        self.clip_shader['view'] = (b.left, b.right, b.bottom, b.top)

    @property
    def transform(self):
        """The transform that maps from framebuffer coordinates to clipping
        coordinates.
        """
        return self._transform

    @transform.setter
    def transform(self, tr):
        if tr is self._transform:
            return
        self._transform = tr
        self.clip_shader['fb_to_clip'] = tr

    def _attach(self, visual):
        try:
            hook = visual._get_hook('frag', 'pre')
        except KeyError:
            raise NotImplementedError('Visual %s does not support clipping' % visual)

        hook.add((self.clip_expr), position=1)

    def _detach(self, visual):
        visual._get_hook('frag', 'pre').remove(self.clip_expr)