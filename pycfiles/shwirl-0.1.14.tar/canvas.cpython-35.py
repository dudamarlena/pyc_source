# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/scene/canvas.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 21169 bytes
from __future__ import division
import weakref, numpy as np
from .. import gloo
from .. import app
from .visuals import VisualNode
from ..visuals.transforms import TransformSystem
from ..color import Color
from ..util import logger, Frozen
from ..util.profiler import Profiler
from .subscene import SubScene
from .events import SceneMouseEvent
from .widgets import Widget

class SceneCanvas(app.Canvas, Frozen):
    __doc__ = "A Canvas that automatically draws the contents of a scene\n\n    Parameters\n    ----------\n    title : str\n        The widget title\n    size : (width, height)\n        The size of the window.\n    position : (x, y)\n        The position of the window in screen coordinates.\n    show : bool\n        Whether to show the widget immediately. Default False.\n    autoswap : bool\n        Whether to swap the buffers automatically after a draw event.\n        Default True. If True, the ``swap_buffers`` Canvas method will\n        be called last (by default) by the ``canvas.draw`` event handler.\n    app : Application | str\n        Give vispy Application instance to use as a backend.\n        (vispy.app is used by default.) If str, then an application\n        using the chosen backend (e.g., 'pyglet') will be created.\n        Note the canvas application can be accessed at ``canvas.app``.\n    create_native : bool\n        Whether to create the widget immediately. Default True.\n    vsync : bool\n        Enable vertical synchronization.\n    resizable : bool\n        Allow the window to be resized.\n    decorate : bool\n        Decorate the window. Default True.\n    fullscreen : bool | int\n        If False, windowed mode is used (default). If True, the default\n        monitor is used. If int, the given monitor number is used.\n    config : dict\n        A dict with OpenGL configuration options, which is combined\n        with the default configuration options and used to initialize\n        the context. See ``canvas.context.config`` for possible\n        options.\n    shared : Canvas | GLContext | None\n        An existing canvas or context to share OpenGL objects with.\n    keys : str | dict | None\n        Default key mapping to use. If 'interactive', escape and F11 will\n        close the canvas and toggle full-screen mode, respectively.\n        If dict, maps keys to functions. If dict values are strings,\n        they are assumed to be ``Canvas`` methods, otherwise they should\n        be callable.\n    parent : widget-object\n        The parent widget if this makes sense for the used backend.\n    dpi : float | None\n        Resolution in dots-per-inch to use for the canvas. If dpi is None,\n        then the value will be determined by querying the global config first,\n        and then the operating system.\n    always_on_top : bool\n        If True, try to create the window in always-on-top mode.\n    px_scale : int > 0\n        A scale factor to apply between logical and physical pixels in addition\n        to the actual scale factor determined by the backend. This option\n        allows the scale factor to be adjusted for testing.\n    bgcolor : Color\n        The background color to use.\n\n    See also\n    --------\n    vispy.app.Canvas\n\n    Notes\n    -----\n    Receives the following events:\n\n        * initialize\n        * resize\n        * draw\n        * mouse_press\n        * mouse_release\n        * mouse_double_click\n        * mouse_move\n        * mouse_wheel\n        * key_press\n        * key_release\n        * stylus\n        * touch\n        * close\n\n    The ordering of the mouse_double_click, mouse_press, and mouse_release\n    events are not guaranteed to be consistent between backends. Only certain\n    backends natively support double-clicking (currently Qt and WX); on other\n    backends, they are detected manually with a fixed time delay.\n    This can cause problems with accessibility, as increasing the OS detection\n    time or using a dedicated double-click button will not be respected.\n    "

    def __init__(self, title='VisPy canvas', size=(800, 600), position=None, show=False, autoswap=True, app=None, create_native=True, vsync=False, resizable=True, decorate=True, fullscreen=False, config=None, shared=None, keys=None, parent=None, dpi=None, always_on_top=False, px_scale=1, bgcolor='black'):
        self._scene = None
        self._central_widget = None
        self._draw_order = weakref.WeakKeyDictionary()
        self._drawing = False
        self._fb_stack = []
        self._vp_stack = []
        self._mouse_handler = None
        self.transforms = TransformSystem(canvas=self)
        self._bgcolor = Color(bgcolor).rgba
        self._send_hover_events = False
        super(SceneCanvas, self).__init__(title, size, position, show, autoswap, app, create_native, vsync, resizable, decorate, fullscreen, config, shared, keys, parent, dpi, always_on_top, px_scale)
        self.events.mouse_press.connect(self._process_mouse_event)
        self.events.mouse_move.connect(self._process_mouse_event)
        self.events.mouse_release.connect(self._process_mouse_event)
        self.events.mouse_wheel.connect(self._process_mouse_event)
        self.scene = SubScene()
        self.freeze()

    @property
    def scene(self):
        """ The SubScene object that represents the root node of the
        scene graph to be displayed.
        """
        return self._scene

    @scene.setter
    def scene(self, node):
        oldscene = self._scene
        self._scene = node
        if oldscene is not None:
            oldscene._set_canvas(None)
            oldscene.events.children_change.disconnect(self._update_scenegraph)
        if node is not None:
            node._set_canvas(self)
            node.events.children_change.connect(self._update_scenegraph)

    @property
    def central_widget(self):
        """ Returns the default widget that occupies the entire area of the
        canvas. 
        """
        if self._central_widget is None:
            self._central_widget = Widget(size=self.size, parent=self.scene)
        return self._central_widget

    @property
    def bgcolor(self):
        return Color(self._bgcolor)

    @bgcolor.setter
    def bgcolor(self, color):
        self._bgcolor = Color(color).rgba
        if hasattr(self, '_backend'):
            self.update()

    def update(self, node=None):
        """Update the scene

        Parameters
        ----------
        node : instance of Node
            Not used.
        """
        if self._drawing:
            return
        app.Canvas.update(self)

    def on_draw(self, event):
        """Draw handler

        Parameters
        ----------
        event : instance of Event
            The draw event.
        """
        if self._scene is None:
            return
        logger.debug('Canvas draw')
        self._draw_scene()

    def render(self, region=None, size=None, bgcolor=None):
        """Render the scene to an offscreen buffer and return the image array.
        
        Parameters
        ----------
        region : tuple | None
            Specifies the region of the canvas to render. Format is 
            (x, y, w, h). By default, the entire canvas is rendered.
        size : tuple | None
            Specifies the size of the image array to return. If no size is 
            given, then the size of the *region* is used, multiplied by the 
            pixel scaling factor of the canvas (see `pixel_scale`). This
            argument allows the scene to be rendered at resolutions different
            from the native canvas resolution.
        bgcolor : instance of Color | None
            The background color to use.

        Returns
        -------
        image : array
            Numpy array of type ubyte and shape (h, w, 4). Index [0, 0] is the 
            upper-left corner of the rendered region.
        
        """
        self.set_current()
        offset = (0, 0) if region is None else region[:2]
        csize = self.size if region is None else region[2:]
        s = self.pixel_scale
        size = tuple([x * s for x in csize]) if size is None else size
        fbo = gloo.FrameBuffer(color=gloo.RenderBuffer(size[::-1]), depth=gloo.RenderBuffer(size[::-1]))
        self.push_fbo(fbo, offset, csize)
        try:
            self._draw_scene(bgcolor=bgcolor)
            return fbo.read()
        finally:
            self.pop_fbo()

    def _draw_scene(self, bgcolor=None):
        if bgcolor is None:
            bgcolor = self._bgcolor
        self.context.clear(color=bgcolor, depth=True)
        self.draw_visual(self.scene)

    def draw_visual(self, visual, event=None):
        """ Draw a visual and its children to the canvas or currently active
        framebuffer.
        
        Parameters
        ----------
        visual : Visual
            The visual to draw
        event : None or DrawEvent
            Optionally specifies the original canvas draw event that initiated
            this draw.
        """
        prof = Profiler()
        self.set_current()
        try:
            self._drawing = True
            if visual not in self._draw_order:
                self._draw_order[visual] = self._generate_draw_order()
            order = self._draw_order[visual]
            stack = []
            invisible_node = None
            for node, start in order:
                if start:
                    stack.append(node)
                    if invisible_node is None:
                        if not node.visible:
                            invisible_node = node
                        elif hasattr(node, 'draw'):
                            node.draw()
                            prof.mark(str(node))
                        else:
                            if node is invisible_node:
                                invisible_node = None
                            stack.pop()

        finally:
            self._drawing = False

    def _generate_draw_order(self, node=None):
        """Return a list giving the order to draw visuals.
        
        Each node appears twice in the list--(node, True) appears before the
        node's children are drawn, and (node, False) appears after.
        """
        if node is None:
            node = self._scene
        order = [
         (
          node, True)]
        children = node.children
        children.sort(key=lambda ch: ch.order)
        for ch in children:
            order.extend(self._generate_draw_order(ch))

        order.append((node, False))
        return order

    def _update_scenegraph(self, event):
        """Called when topology of scenegraph has changed.
        """
        self._draw_order.clear()
        self.update()

    def _process_mouse_event(self, event):
        prof = Profiler()
        deliver_types = ['mouse_press', 'mouse_wheel']
        if self._send_hover_events:
            deliver_types += ['mouse_move']
        picked = self._mouse_handler
        if picked is None and event.type in deliver_types:
            picked = self.visual_at(event.pos)
        if picked is None:
            return
        scene_event = SceneMouseEvent(event=event, visual=picked)
        if picked == self._mouse_handler:
            if event.type == 'mouse_release':
                self._mouse_handler = None
            getattr(picked.events, event.type)(scene_event)
        else:
            while picked is not None:
                getattr(picked.events, event.type)(scene_event)
                if scene_event.handled:
                    if event.type == 'mouse_press':
                        self._mouse_handler = picked
                    break
                if event.type in deliver_types:
                    picked = picked.parent
                    scene_event.visual = picked
                else:
                    picked = None

        event.handled = scene_event.handled

    def visual_at(self, pos):
        """Return the visual at a given position

        Parameters
        ----------
        pos : tuple
            The position in logical coordinates to query.

        Returns
        -------
        visual : instance of Visual | None
            The visual at the position, if it exists.
        """
        tr = self.transforms.get_transform('canvas', 'framebuffer')
        fbpos = tr.map(pos)[:2]
        try:
            id_ = self._render_picking(region=(fbpos[0], fbpos[1],
             1, 1))
            vis = VisualNode._visual_ids.get(id_[(0, 0)], None)
        except RuntimeError:
            return self._visual_bounds_at(pos)

        return vis

    def _visual_bounds_at(self, pos, node=None):
        """Find a visual whose bounding rect encompasses *pos*.
        """
        if node is None:
            node = self.scene
        for ch in node.children:
            hit = self._visual_bounds_at(pos, ch)
            if hit is not None:
                return hit

        if not isinstance(node, VisualNode) or not node.visible or not node.interactive:
            return
        bounds = [node.bounds(axis=i) for i in range(2)]
        if None in bounds:
            return
        tr = self.scene.node_transform(node).inverse
        corners = np.array([
         [
          bounds[0][0], bounds[1][0]],
         [
          bounds[0][0], bounds[1][1]],
         [
          bounds[0][1], bounds[1][0]],
         [
          bounds[0][1], bounds[1][1]]])
        bounds = tr.map(corners)
        xhit = bounds[:, 0].min() < pos[0] < bounds[:, 0].max()
        yhit = bounds[:, 1].min() < pos[1] < bounds[:, 1].max()
        if xhit and yhit:
            return node

    def visuals_at(self, pos, radius=10):
        """Return a list of visuals within *radius* pixels of *pos*.
        
        Visuals are sorted by their proximity to *pos*.
        
        Parameters
        ----------
        pos : tuple
            (x, y) position at which to find visuals.
        radius : int
            Distance away from *pos* to search for visuals.
        """
        tr = self.transforms.get_transform('canvas', 'framebuffer')
        pos = tr.map(pos)[:2]
        id = self._render_picking(region=(pos[0] - radius, pos[1] - radius,
         radius * 2 + 1, radius * 2 + 1))
        ids = []
        seen = set()
        for i in range(radius):
            subr = id[radius - i:radius + i + 1, radius - i:radius + i + 1]
            subr_ids = set(list(np.unique(subr)))
            ids.extend(list(subr_ids - seen))
            seen |= subr_ids

        visuals = [VisualNode._visual_ids.get(x, None) for x in ids]
        return [v for v in visuals if v is not None]

    def _render_picking(self, **kwargs):
        """Render the scene in picking mode, returning a 2D array of visual 
        IDs.
        """
        try:
            self._scene.picking = True
            img = self.render(bgcolor=(0, 0, 0, 0), **kwargs)
        finally:
            self._scene.picking = False

        img = img.astype('int32') * [1, 256, 65536, 16777216]
        id_ = img.sum(axis=2).astype('int32')
        return id_

    def on_resize(self, event):
        """Resize handler

        Parameters
        ----------
        event : instance of Event
            The resize event.
        """
        self._update_transforms()
        if self._central_widget is not None:
            self._central_widget.size = self.size
        if len(self._vp_stack) == 0:
            self.context.set_viewport(0, 0, *self.physical_size)

    def on_close(self, event):
        """Close event handler

        Parameters
        ----------
        event : instance of Event
            The event.
        """
        self.events.mouse_press.disconnect(self._process_mouse_event)
        self.events.mouse_move.disconnect(self._process_mouse_event)
        self.events.mouse_release.disconnect(self._process_mouse_event)
        self.events.mouse_wheel.disconnect(self._process_mouse_event)

    def push_viewport(self, viewport):
        """ Push a viewport (x, y, w, h) on the stack. Values must be integers
        relative to the active framebuffer.

        Parameters
        ----------
        viewport : tuple
            The viewport as (x, y, w, h).
        """
        vp = list(viewport)
        if vp[2] < 0:
            vp[0] += vp[2]
            vp[2] *= -1
        if vp[3] < 0:
            vp[1] += vp[3]
            vp[3] *= -1
        self._vp_stack.append(vp)
        try:
            self.context.set_viewport(*vp)
        except:
            self._vp_stack.pop()
            raise

        self._update_transforms()

    def pop_viewport(self):
        """ Pop a viewport from the stack.
        """
        vp = self._vp_stack.pop()
        if len(self._vp_stack) > 0:
            self.context.set_viewport(*self._vp_stack[(-1)])
        else:
            self.context.set_viewport(0, 0, *self.physical_size)
        self._update_transforms()
        return vp

    def push_fbo(self, fbo, offset, csize):
        """ Push an FBO on the stack.
        
        This activates the framebuffer and causes subsequent rendering to be
        written to the framebuffer rather than the canvas's back buffer. This
        will also set the canvas viewport to cover the boundaries of the 
        framebuffer.

        Parameters
        ----------
        fbo : instance of FrameBuffer
            The framebuffer object .
        offset : tuple
            The location of the fbo origin relative to the canvas's framebuffer
            origin.
        csize : tuple
            The size of the region in the canvas's framebuffer that should be 
            covered by this framebuffer object.
        """
        self._fb_stack.append((fbo, offset, csize))
        try:
            fbo.activate()
            h, w = fbo.color_buffer.shape[:2]
            self.push_viewport((0, 0, w, h))
        except Exception:
            self._fb_stack.pop()
            raise

        self._update_transforms()

    def pop_fbo(self):
        """ Pop an FBO from the stack.
        """
        fbo = self._fb_stack.pop()
        fbo[0].deactivate()
        self.pop_viewport()
        if len(self._fb_stack) > 0:
            old_fbo = self._fb_stack[(-1)]
            old_fbo[0].activate()
        self._update_transforms()
        return fbo

    def _current_framebuffer(self):
        """ Return (fbo, origin, canvas_size) for the current
        FBO on the stack, or for the canvas if there is no FBO.
        """
        if len(self._fb_stack) == 0:
            return (None, (0, 0), self.size)
        else:
            return self._fb_stack[(-1)]

    def _update_transforms(self):
        """Update the canvas's TransformSystem to correct for the current 
        canvas size, framebuffer, and viewport.
        """
        if len(self._fb_stack) == 0:
            fb_size = fb_rect = None
        else:
            fb, origin, fb_size = self._fb_stack[(-1)]
            fb_rect = origin + fb_size
        if len(self._vp_stack) == 0:
            viewport = None
        else:
            viewport = self._vp_stack[(-1)]
        self.transforms.configure(viewport=viewport, fbo_size=fb_size, fbo_rect=fb_rect)