# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/transforms/transform_system.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 13033 bytes
from __future__ import division
from .linear import STTransform, NullTransform
from .chain import ChainTransform
from ._util import TransformCache
from ...util.event import EventEmitter

class TransformSystem(object):
    __doc__ = " TransformSystem encapsulates information about the coordinate\n    systems needed to draw a Visual.\n\n    Visual rendering operates in six coordinate systems:\n\n    * **Visual** - arbitrary local coordinate frame of the visual. Vertex\n      buffers used by the visual are usually specified in this coordinate\n      system.\n\n    * **Scene** - This is an isometric coordinate system used mainly for \n      lighting calculations.\n\n    * **Document** - This coordinate system has units of _logical_ pixels, and\n      should usually represent the pixel coordinates of the canvas being drawn\n      to. Visuals use this coordinate system to make measurements for font\n      size, line width, and in general anything that is specified in physical\n      units (px, pt, mm, in, etc.). In most circumstances, this is exactly the\n      same as the canvas coordinate system.\n\n    * **Canvas** - This coordinate system represents the logical pixel\n      coordinates of the canvas. It has its origin in the top-left corner of\n      the canvas, and is typically the coordinate system that mouse and touch \n      events are reported in. Note that, by convention, _logical_ pixels\n      are not necessarily the same size as the _physical_ pixels in the\n      framebuffer that is being rendered to.\n\n    * **Framebuffer** - The buffer coordinate system has units of _physical_ \n      pixels, and should usually represent the coordinates of the current \n      framebuffer (on the canvas or an FBO) being rendered to. Visuals use this\n      coordinate system primarily for antialiasing calculations. It is also the\n      coorinate system used by glFragCoord. In most cases,\n      this will have the same scale as the document and canvas coordinate \n      systems because the active framebuffer is the\n      back buffer of the canvas, and the canvas will have _logical_ and\n      _physical_ pixels of the same size. However, the scale may be different\n      in the case of high-resolution displays, or when rendering to an \n      off-screen framebuffer with different scaling or boundaries than the\n      canvas.\n\n    * **Render** - This coordinate system is the obligatory system for\n      vertices returned by a vertex shader. It has coordinates (-1, -1) to\n      (1, 1) across the current glViewport. In OpenGL terminology, this is\n      called clip coordinates.\n\n    Parameters\n    ----------\n\n    canvas : Canvas\n        The canvas being drawn to.\n    dpi : float\n        The dot-per-inch resolution of the document coordinate system. By\n        default this is set to the resolution of the canvas.\n\n    Notes\n    -----\n\n    By default, TransformSystems are configured such that the document\n    coordinate system matches the logical pixels of the canvas,\n\n    Examples\n    --------\n    Use by Visuals\n    ~~~~~~~~~~~~~~\n\n    1. To convert local vertex coordinates to normalized device coordinates in\n    the vertex shader, we first need a vertex shader that supports configurable\n    transformations::\n\n        vec4 a_position;\n        void main() {\n            gl_Position = $transform(a_position);\n        }\n\n    Next, we supply the complete chain of transforms when drawing the visual:\n\n        def draw(tr_sys):\n            tr = tr_sys.get_full_transform()\n            self.program['transform'] = tr.shader_map()\n            self.program['a_position'] = self.vertex_buffer\n            self.program.draw('triangles')\n\n    2. Draw a line whose width is given in mm. To start, we need normal vectors\n    for each vertex, which tell us the direction the vertex should move in\n    order to set the line width::\n\n        vec4 a_position;\n        vec4 a_normal;\n        float u_line_width;\n        float u_dpi;\n        void main() {\n            // map vertex position and normal vector to the document cs\n            vec4 doc_pos = $visual_to_doc(a_position);\n            vec4 doc_normal = $visual_to_doc(a_position + a_normal) - doc_pos;\n\n            // Use DPI to convert mm line width to logical pixels\n            float px_width = (u_line_width / 25.4) * dpi;\n\n            // expand by line width\n            doc_pos += normalize(doc_normal) * px_width;\n\n            // finally, map the remainder of the way to normalized device\n            // coordinates.\n            gl_Position = $doc_to_render(a_position);\n        }\n\n    In this case, we need to access\n    the transforms independently, so ``get_full_transform()`` is not useful\n    here::\n\n        def draw(tr_sys):\n            # Send two parts of the full transform separately\n            self.program['visual_to_doc'] = tr_sys.visual_to_doc.shader_map()\n            doc_to_render = (tr_sys.framebuffer_transform *\n                             tr_sys.document_transform)\n            self.program['visual_to_doc'] = doc_to_render.shader_map()\n\n            self.program['u_line_width'] = self.line_width\n            self.program['u_dpi'] = tr_sys.dpi\n            self.program['a_position'] = self.vertex_buffer\n            self.program['a_normal'] = self.normal_buffer\n            self.program.draw('triangles')\n\n    3. Draw a triangle with antialiasing at the edge.\n\n    4. Using inverse transforms in the fragment shader\n    "

    def __init__(self, canvas=None, dpi=None):
        self.changed = EventEmitter(source=self, type='transform_changed')
        self._canvas = None
        self._fbo_bounds = None
        self.canvas = canvas
        self._cache = TransformCache()
        self._dpi = dpi
        self._visual_transform = ChainTransform([NullTransform()])
        self._scene_transform = ChainTransform([NullTransform()])
        self._document_transform = ChainTransform([NullTransform()])
        self._canvas_transform = ChainTransform([STTransform(),
         STTransform()])
        self._framebuffer_transform = ChainTransform([STTransform()])
        for tr in (self._visual_transform, self._scene_transform,
         self._document_transform, self._canvas_transform,
         self._framebuffer_transform):
            tr.changed.connect(self.changed)

    def configure(self, viewport=None, fbo_size=None, fbo_rect=None, canvas=None):
        """Automatically configure the TransformSystem:

        * canvas_transform maps from the Canvas logical pixel
          coordinate system to the framebuffer coordinate system, taking into 
          account the logical/physical pixel scale factor, current FBO 
          position, and y-axis inversion.
        * framebuffer_transform maps from the current GL viewport on the
          framebuffer coordinate system to clip coordinates (-1 to 1). 
          
          
        Parameters
        ==========
        viewport : tuple or None
            The GL viewport rectangle (x, y, w, h). If None, then it
            is assumed to cover the entire canvas.
        fbo_size : tuple or None
            The size of the active FBO. If None, then it is assumed to have the
            same size as the canvas's framebuffer.
        fbo_rect : tuple or None
            The position and size (x, y, w, h) of the FBO in the coordinate
            system of the canvas's framebuffer. If None, then the bounds are
            assumed to cover the entire active framebuffer.
        canvas : Canvas instance
            Optionally set the canvas for this TransformSystem. See the 
            `canvas` property.
        """
        if canvas is not None:
            self.canvas = canvas
        canvas = self._canvas
        if canvas is None:
            raise RuntimeError('No canvas assigned to this TransformSystem.')
        map_from = [
         (0, 0), canvas.size]
        map_to = [(0, canvas.physical_size[1]), (canvas.physical_size[0], 0)]
        self._canvas_transform.transforms[1].set_mapping(map_from, map_to)
        if fbo_rect is None:
            self._canvas_transform.transforms[0].scale = (1, 1, 1)
            self._canvas_transform.transforms[0].translate = (0, 0, 0)
        else:
            map_from = [
             (
              fbo_rect[0], fbo_rect[1]),
             (
              fbo_rect[0] + fbo_rect[2], fbo_rect[1] + fbo_rect[3])]
            map_to = [(0, 0), fbo_size]
            self._canvas_transform.transforms[0].set_mapping(map_from, map_to)
        if viewport is None:
            if fbo_size is None:
                map_from = [(0, 0), canvas.physical_size]
            else:
                map_from = [
                 (0, 0), fbo_size]
        else:
            map_from = [
             viewport[:2],
             (
              viewport[0] + viewport[2], viewport[1] + viewport[3])]
        map_to = [
         (-1, -1), (1, 1)]
        self._framebuffer_transform.transforms[0].set_mapping(map_from, map_to)

    @property
    def canvas(self):
        """ The Canvas being drawn to.
        """
        return self._canvas

    @canvas.setter
    def canvas(self, canvas):
        self._canvas = canvas

    @property
    def dpi(self):
        """ Physical resolution of the document coordinate system (dots per
        inch).
        """
        if self._dpi is None:
            if self._canvas is None:
                return
            else:
                return self.canvas.dpi
        else:
            return self._dpi

    @dpi.setter
    def dpi(self, dpi):
        assert dpi > 0
        self._dpi = dpi

    @property
    def visual_transform(self):
        """ Transform mapping from visual local coordinate frame to scene
        coordinate frame.
        """
        return self._visual_transform

    @visual_transform.setter
    def visual_transform(self, tr):
        self._visual_transform.transforms = tr

    @property
    def scene_transform(self):
        """ Transform mapping from scene coordinate frame to document
        coordinate frame.
        """
        return self._scene_transform

    @scene_transform.setter
    def scene_transform(self, tr):
        self._scene_transform.transforms = tr

    @property
    def document_transform(self):
        """ Transform mapping from document coordinate frame to the framebuffer
        (physical pixel) coordinate frame.
        """
        return self._document_transform

    @document_transform.setter
    def document_transform(self, tr):
        self._document_transform.transforms = tr

    @property
    def canvas_transform(self):
        """ Transform mapping from canvas coordinate frame to framebuffer
        coordinate frame.
        """
        return self._canvas_transform

    @canvas_transform.setter
    def canvas_transform(self, tr):
        self._canvas_transform.transforms = tr

    @property
    def framebuffer_transform(self):
        """ Transform mapping from pixel coordinate frame to rendering
        coordinate frame.
        """
        return self._framebuffer_transform

    @framebuffer_transform.setter
    def framebuffer_transform(self, tr):
        self._framebuffer_transform.transforms = tr

    def get_transform(self, map_from='visual', map_to='render'):
        """Return a transform mapping between any two coordinate systems.
        
        Parameters
        ----------
        map_from : str
            The starting coordinate system to map from. Must be one of: visual,
            scene, document, canvas, framebuffer, or render.
        map_to : str
            The ending coordinate system to map to. Must be one of: visual,
            scene, document, canvas, framebuffer, or render.
        """
        tr = [
         'visual', 'scene', 'document', 'canvas', 'framebuffer', 'render']
        ifrom = tr.index(map_from)
        ito = tr.index(map_to)
        if ifrom < ito:
            trs = [getattr(self, '_' + t + '_transform') for t in tr[ifrom:ito]][::-1]
        else:
            trs = [getattr(self, '_' + t + '_transform').inverse for t in tr[ito:ifrom]]
        return self._cache.get(trs)

    @property
    def pixel_scale(self):
        tr = self._canvas_transform
        return (tr.map((1, 0)) - tr.map((0, 0)))[0]