# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/visuals/filters/picking.py
# Compiled at: 2016-11-03 01:40:19
import struct, weakref
from ..shaders import Function

class PickingFilter(object):
    """Filter used to color visuals by a picking ID. 
    
    Note that the ID color uses the alpha channel, so this may not be used
    with blending enabled.
    """

    def __init__(self, id_=None):
        self.shader = Function('\n            void picking_filter() {\n                if( $enabled == 0 )\n                    return;\n                if( gl_FragColor.a == 0.0 )\n                    discard;\n                gl_FragColor = $id_color;\n            }\n        ')
        self.id = id_
        self.enabled = False

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if id < 1:
            raise ValueError('Picking ID must be integer > 0.')
        id_color = struct.unpack('<4B', struct.pack('<I', id))
        self.shader['id_color'] = [ x / 255.0 for x in id_color ]
        self._id = id
        self._id_color = id_color

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, e):
        self._enabled = e
        self.shader['enabled'] = 1 if e is True else 0

    @property
    def color(self):
        """ The RGBA color that will be drawn to the framebuffer for visuals
        that use this filter.
        """
        return self._id_color

    def _attach(self, visual):
        self._visual = weakref.ref(visual)
        hook = self._visual()._get_hook('frag', 'post')
        hook.add(self.shader(), position=10)