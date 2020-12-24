# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\layer\scrolling.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 20120 bytes
__doc__ = "This module defines the :class:`ScrollableLayer` and \n:class:`ScrollingManager` classes.\n\nThis module helps to handle what will be visible on screen when the game world\ndoes not fit in the window area.\n\nIt models this concept: the game world is a big volume. We have a camera\nthat follows the actor moving parallel to one of the volume faces, without \nrotations. What the camera sees is what  will be seen on the app window. Also, \nthe camera's movements can be restricted in order not to show parts outside \nof the world. This technique is usually named *'scrolling'*.\n\nIt has support for parallax rendering, that is, faking perspective by using\nlayers that slide slower the farther they are.\n\nThe important concepts are:\n  - The coordinator, implemented as :class:`ScrollingManager` which enforces the\n    view limits imposed by the managed layers, accounts for layer's parallax.\n\n  - The managed layers, implemented each by a :class:`ScrollableLayer`, which as\n    a group holds all the entities in the world and each one can define what\n    area of the x-y plane should be shown on camera.\n\n  -The focus, tied to ScrollingManager ``fx`` and ``fy`` attributes, which \n    indicates that point (fx, fy) in world coordinates is the point of interest,\n    and should show at the center of the *screen view* if no restriction is\n    violated.\n"
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import warnings
import cocos.director as director
from .base_layers import Layer
import pyglet
from pyglet import gl

class ScrollableLayer(Layer):
    """ScrollableLayer"""

    def __init__(self, parallax=1):
        super(ScrollableLayer, self).__init__()
        self.parallax = parallax
        self.transform_anchor_x = 0
        self.transform_anchor_y = 0
        self.batch = pyglet.graphics.Batch()
        self.view_x = 0
        self.view_y = 0
        self.view_w = 0
        self.view_h = 0
        self.origin_x = self.origin_y = self.origin_z = 0

    def on_enter(self):
        director.push_handlers(self.on_cocos_resize)
        super(ScrollableLayer, self).on_enter()

    def on_exit(self):
        super(ScrollableLayer, self).on_exit()
        director.pop_handlers()

    def set_view(self, x, y, w, h, viewport_ox=0, viewport_oy=0):
        """Sets the position of the viewport for this layer.

        Arguments:
            x (float): The view x position
            y (float): The view y position
            w (float): The width of the view
            h (float): The height of the view
            viewport_ox (float) : The viewport x origin
            viewport_oy (float) : The viewport y origin
        """
        x *= self.parallax
        y *= self.parallax
        self.view_x, self.view_y = x, y
        self.view_w, self.view_h = w, h
        x -= self.origin_x
        y -= self.origin_y
        x -= viewport_ox
        y -= viewport_oy
        self.position = (-x, -y)

    def draw(self):
        super(ScrollableLayer, self).draw()
        gl.glPushMatrix()
        self.transform()
        self.batch.draw()
        gl.glPopMatrix()

    def set_dirty(self):
        """The viewport has changed in some way.
        """
        pass

    def on_cocos_resize(self, usable_width, usable_height):
        """Event handler for window resizing."""
        self.set_dirty()


class ScrollingManager(Layer):
    """ScrollingManager"""

    def __init__(self, viewport=None, do_not_scale=None):
        if do_not_scale is None:
            do_not_scale = not director.autoscale
        self.autoscale = not do_not_scale and director.autoscale
        self.viewport = viewport
        self.view_x, self.view_y = (0, 0)
        self.view_w, self.view_h = (1, 1)
        self.childs_ox = 0
        self.childs_oy = 0
        self.fx = self.fy = 0
        super(ScrollingManager, self).__init__()
        self.transform_anchor_x = 0
        self.transform_anchor_y = 0
        self._old_focus = None

    def on_enter(self):
        super(ScrollingManager, self).on_enter()
        director.push_handlers(self.on_cocos_resize)
        self.update_view_size()
        self.refresh_focus()

    def on_exit(self):
        director.pop_handlers()
        super(ScrollingManager, self).on_exit()

    def update_view_size(self):
        """Updates the view size based on the director usable width and height,
        and on the optional viewport.
        """
        if self.viewport is not None:
            self.view_w, self.view_h = self.viewport.width, self.viewport.height
            self.view_x, self.view_y = getattr(self.viewport, 'position', (0, 0))
            if not director.autoscale:
                self._scissor_flat = (
                 self.view_x, self.view_y,
                 self.view_w, self.view_h)
            else:
                w, h = director.get_window_size()
                sx = director._usable_width / w
                sy = director._usable_height / h
                self._scissor_flat = (int(self.view_x * sx), int(self.view_y * sy),
                 int(self.view_w * sx), int(self.view_h * sy))
        elif self.autoscale:
            self.view_w, self.view_h = director.get_window_size()
        else:
            self.view_w = director._usable_width
            self.view_h = director._usable_height

    def on_cocos_resize(self, usable_width, usable_height):
        """Event handler for Window resize."""
        self.update_view_size()
        self.refresh_focus()

    def refresh_focus(self):
        """Resets the focus at the focus point."""
        if self.children:
            self._old_focus = None
            self.set_focus(self.fx, self.fy)

    def _set_scale(self, scale):
        self._scale = 1.0 * scale
        self.refresh_focus()

    scale = property((lambda s: s._scale), _set_scale, doc='The scaling factor of the object.\n\n        :type: float\n        ')

    def add(self, child, z=0, name=None):
        """Add the child and then update the manager's focus / viewport.

        Args:
            child (CocosNode): The node to add. Normally it's a
                :class:`ScrollableLayer`.
            z (int) : z-order for this child.
            name (str) : The name of this child. [Optional]
        """
        super(ScrollingManager, self).add(child, z=z, name=name)
        self.set_focus((self.fx), (self.fy), force=True)

    def pixel_from_screen(self, x, y):
        """deprecated, was renamed as screen_to_world"""
        warnings.warn('Cocos Deprecation Warning: ScrollingManager.pixel_from_screen was renamed to Scrolling Manager.screen_to_world; the former will disappear in future cocos releases')
        return self.screen_to_world(x, y)

    def screen_to_world(self, x, y):
        """Translates screen coordinates to world coordinates.

        Account for viewport, layer and screen transformations.

        Arguments:
            x (int): x coordinate in screen space
            y (int): y coordinate in screen space

        Returns:
            tuple[int, int]: coordinates in world-space
        """
        if director.autoscale:
            x, y = director.get_virtual_coordinates(x, y)
        ww, wh = director.get_window_size()
        sx = x / self.view_w
        sy = y / self.view_h
        vx, vy = self.childs_ox, self.childs_oy
        w = int(self.view_w / self.scale)
        h = int(self.view_h / self.scale)
        return (
         int(vx + sx * w), int(vy + sy * h))

    def pixel_to_screen(self, x, y):
        """deprecated, was renamed as world_to_screen"""
        warnings.warn('Cocos Deprecation Warning: ScrollingManager.pixel_to_screen was renamed to Scrolling Manager.world_to_screen; the former will disappear in future cocos releases')
        return self.world_to_screen(x, y)

    def world_to_screen(self, x, y):
        """Translates world coordinates to screen coordinates.

        Account for viewport, layer and screen transformations.

        Arguments:
            x (int): x coordinate in world space
            y (int): y coordinate in world space

        Returns:
            tuple[int, int]: coordinates in screen space
        """
        screen_x = self.scale * (x - self.childs_ox)
        screen_y = self.scale * (y - self.childs_oy)
        return (
         int(screen_x), int(screen_y))

    def set_focus(self, fx, fy, force=False):
        """Makes the point (fx, fy) show as near the view's center as possible.

        Changes his children so that the point (fx, fy) in world coordinates
        will be seen as near the view center as possible, while at the
        same time not displaying out-of-bounds areas in the children.

        Args:
            fx (int): the focus point x coordinate
            fy (int): the focus point y coordinate
            force (bool): If True, forces the update of the focus, eventhough the
                focus point or the scale did not change. Defaults to False.
        """
        if not [l for z, l in self.children if hasattr(l, 'px_width')]:
            return self.force_focus(fx, fy)
            self.fx, self.fy = fx, fy
            a = (
             fx, fy, self.scale)
            if not force:
                if self._old_focus == a:
                    return
            else:
                self._old_focus = a
                x1 = []
                y1 = []
                x2 = []
                y2 = []
                for z, layer in self.children:
                    if not hasattr(layer, 'px_width'):
                        pass
                    else:
                        x1.append(layer.origin_x)
                        y1.append(layer.origin_y)
                        x2.append(layer.origin_x + layer.px_width)
                        y2.append(layer.origin_y + layer.px_height)

                b_min_x = min(x1)
                b_min_y = min(y1)
                b_max_x = max(x2)
                b_max_y = max(y2)
                w = self.view_w / self.scale
                h = self.view_h / self.scale
                w2, h2 = w / 2, h / 2
                if b_max_x - b_min_x <= w:
                    restricted_fx = (b_max_x + b_min_x) / 2
                elif fx - w2 < b_min_x:
                    restricted_fx = b_min_x + w2
                elif fx + w2 > b_max_x:
                    restricted_fx = b_max_x - w2
                else:
                    restricted_fx = fx
            if b_max_y - b_min_y <= h:
                restricted_fy = (b_max_y + b_min_y) / 2
        elif fy - h2 < b_min_y:
            restricted_fy = b_min_y + h2
        elif fy + h2 > b_max_y:
            restricted_fy = b_max_y - h2
        else:
            restricted_fy = fy
        self.restricted_fx = restricted_fx
        self.restricted_fy = restricted_fy
        x, y = restricted_fx - w2, restricted_fy - h2
        childs_scroll_x = x
        childs_scroll_y = y
        self.childs_ox = childs_scroll_x - self.view_x / self.scale
        self.childs_oy = childs_scroll_y - self.view_y / self.scale
        for z, layer in self.children:
            layer.set_view(childs_scroll_x, childs_scroll_y, w, h, self.view_x / self.scale, self.view_y / self.scale)

    def force_focus(self, fx, fy):
        """Force the manager to focus on a point, regardless of any managed layer
        visible boundaries.

        Args:
            fx (int): the focus point x coordinate
            fy (int): the focus point y coordinate
        """
        self.fx, self.fy = map(int, (fx, fy))
        self.fx, self.fy = fx, fy
        w = int(self.view_w / self.scale)
        h = int(self.view_h / self.scale)
        w2, h2 = w // 2, h // 2
        x, y = fx - w2, fy - h2
        childs_scroll_x = x
        childs_scroll_y = y
        self.childs_ox = childs_scroll_x - self.view_x / self.scale
        self.childs_oy = childs_scroll_y - self.view_y / self.scale
        for z, layer in self.children:
            layer.set_view(childs_scroll_x, childs_scroll_y, w, h, self.view_x / self.scale, self.view_y / self.scale)

    def set_state(self):
        """Sets OpenGL state for using scissor test."""
        self._scissor_enabled = gl.glIsEnabled(gl.GL_SCISSOR_TEST)
        self._old_scissor_flat = (gl.GLint * 4)()
        gl.glGetIntegerv(gl.GL_SCISSOR_BOX, self._old_scissor_flat)
        if not self._scissor_enabled:
            gl.glEnable(gl.GL_SCISSOR_TEST)
        (gl.glScissor)(*self._scissor_flat)

    def unset_state(self):
        """Unsets OpenGL state for using scissor test."""
        (gl.glScissor)(*self._old_scissor_flat)
        if not self._scissor_enabled:
            gl.glDisable(gl.GL_SCISSOR_TEST)

    def visit(self):
        if self.viewport is not None:
            self.set_state()
            super(ScrollingManager, self).visit()
            self.unset_state()
        else:
            super(ScrollingManager, self).visit()