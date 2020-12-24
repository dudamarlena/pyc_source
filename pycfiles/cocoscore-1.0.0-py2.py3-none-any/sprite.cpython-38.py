# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\sprite.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 13735 bytes
__doc__ = '\nSprites allows to display an image in a rectangular area, which can be rotated,\nscaled and moved.\nThe placement in the scene follows the standard CocosNode rules.\nAlso, all stock actions will work with sprites.\n\nAnimating a sprite\n==================\n\nAnimation as in cartoon style animation, that is, replacing the image fast\nenough to give the illusion of movement, can be accomplished by:\n\n - using an animated .gif file as source for the image\n - passing a ``pyglet.image.Animation`` as image, which collects a number of images\n - have an array of images and let your code assign to the sprite image member\n\nChanging a sprite by way of actions\n===================================\n\nTo execute any action you need to create an action::\n\n    move = MoveBy((50, 0), 5)\n\nIn this case, ``move`` is an action that will move the sprite\n50 pixels to the right (``x`` coordinate) and  0 pixel in the ``y`` coordinate\nin 5 seconds.\n\nAnd now tell the sprite to execute it::\n\n    sprite.do(move)\n'
from __future__ import division, print_function, unicode_literals
from six import string_types
__docformat__ = 'restructuredtext'
import math, pyglet
from pyglet import gl
from cocos.batch import BatchableNode
from cocos.rect import Rect
from cocos import euclid
import math
__all__ = [
 'Sprite']

class Sprite(BatchableNode, pyglet.sprite.Sprite):
    """Sprite"""

    def __init__(self, image, position=(0, 0), rotation=0, scale=1, opacity=255, color=(255, 255, 255), anchor=None, **kwargs):
        if isinstance(image, string_types):
            image = pyglet.resource.image(image)
        else:
            self.transform_anchor_x = 0
            self.transform_anchor_y = 0
            self._image_anchor_x = 0
            self._image_anchor_y = 0
            self._scale_x = 1
            self._scale_y = 1
            (pyglet.sprite.Sprite.__init__)(self, image, **kwargs)
            BatchableNode.__init__(self)
            if anchor is None:
                if isinstance(self.image, pyglet.image.Animation):
                    anchor = (
                     image.frames[0].image.width // 2,
                     image.frames[0].image.height // 2)
                else:
                    anchor = (
                     image.width // 2, image.height // 2)
        self.image_anchor = anchor
        self.group = None
        self.children_group = None
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.scale_x = 1
        self.scale_y = 1
        self.opacity = opacity
        self.color = color

    def get_rect(self):
        """Get a :class:`cocos.rect.Rect` for this sprite.

        Note that this rect's position is most likely NOT the same
        as the Sprite's position - in fact by default the rect's
        center is the Sprite's position. If you move the rect around
        and wish to reflect this change in the Sprite, you will probably
        have to do something like (again with the default image anchor
        in the center)::

            rect = sprite.get_rect()
            rect.midbottom = (0, 100)
            sprite.position = rect.center

        Returns:
            :class:`cocos.rect.Rect`: The bounding box for this sprite.
        """
        x, y = self.position
        x -= self.image_anchor_x
        y -= self.image_anchor_y
        return Rect(x, y, self.width, self.height)

    def get_AABB(self):
        """
        Returns:
            :class:`cocos.rect.Rect`: Local-coordinates Axis Aligned Bounding Box.
        """
        v = self._vertex_list.vertices
        x = (v[0], v[2], v[4], v[6])
        y = (v[1], v[3], v[5], v[7])
        return Rect(min(x), min(y), max(x) - min(x), max(y) - min(y))

    @BatchableNode.rotation.setter
    def rotation(self, a):
        super(Sprite, Sprite).rotation.__set__(self, a)
        pyglet.sprite.Sprite.rotation.__set__(self, a)

    @BatchableNode.scale.setter
    def scale(self, s):
        super(Sprite, Sprite).scale.__set__(self, s)
        pyglet.sprite.Sprite.scale.__set__(self, s)

    @BatchableNode.scale_x.setter
    def scale_x(self, s):
        super(Sprite, Sprite).scale_x.__set__(self, s)
        self._update_position()

    @BatchableNode.scale_y.setter
    def scale_y(self, s):
        super(Sprite, Sprite).scale_y.__set__(self, s)
        self._update_position()

    @property
    def width(self):
        """Scaled width of the sprite.

        Read-only.  Invariant under rotation.

        :type: int
        """
        return int(self._texture.width * self._scale * self._scale_x)

    @property
    def height(self):
        """Scaled height of the sprite.

        Read-only.  Invariant under rotation.

        Returns: 
            int
        """
        return int(self._texture.height * self._scale * self._scale_y)

    @BatchableNode.position.setter
    def position(self, p):
        super(Sprite, Sprite).position.__set__(self, p)
        pyglet.sprite.Sprite.position.__set__(self, p)

    @BatchableNode.x.setter
    def x(self, x):
        super(Sprite, Sprite).x.__set__(self, x)
        pyglet.sprite.Sprite.x.__set__(self, x)

    @BatchableNode.y.setter
    def y(self, y):
        super(Sprite, Sprite).y.__set__(self, y)
        pyglet.sprite.Sprite.y.__set__(self, y)

    def contains(self, x, y):
        """Test if the point is in the area covered by the (untransformed) 
        :class:`Sprite` bounding box.
        
        Returns:
            bool
        """
        sx, sy = self.position
        ax, ay = self.image_anchor
        sx -= ax
        sy -= ay
        if x < sx or x > sx + self.width:
            return False
        if y < sy or y > sy + self.height:
            return False
        return True

    @property
    def image_anchor_x(self):
        """float: x coordinate from where the image will be positioned, 
        rotated and scaled in pixels.
        """
        return self._image_anchor_x

    @image_anchor_x.setter
    def image_anchor_x(self, value):
        self._image_anchor_x = value
        self._update_position()

    @property
    def image_anchor_y(self):
        """float: y coordinate from where the image will be positioned, 
        rotated and scaled in pixels.
        """
        return self._image_anchor_y

    @image_anchor_y.setter
    def image_anchor_y(self, value):
        self._image_anchor_y = value
        self._update_position()

    @property
    def image_anchor(self):
        """tuple[float]: Point from where the image will be positioned, 
        rotated and scaled in pixels.
        """
        return (
         self._image_anchor_x, self._image_anchor_y)

    @image_anchor.setter
    def image_anchor(self, value):
        self._image_anchor_x, self.image_anchor_y = value
        self._update_position()

    def draw(self):
        """
        When the sprite is not into a batch it will be drawn with this method.
        If in a batch, this method is not called, and the draw is done by
        the batch.
        """
        self._group.set_state()
        if self._vertex_list is not None:
            self._vertex_list.draw(gl.GL_QUADS)
        self._group.unset_state()

    def _update_position(self):
        """Updates the vertex list"""
        if not self._visible:
            self._vertex_list.vertices[:] = [
             0, 0, 0, 0, 0, 0, 0, 0]
            return
        img = self._texture
        if self.transform_anchor_x == self.transform_anchor_y == 0:
            if self._rotation:
                x1 = -self._image_anchor_x * self._scale * self._scale_x
                y1 = -self._image_anchor_y * self._scale * self._scale_y
                x2 = x1 + img.width * self._scale * self._scale_x
                y2 = y1 + img.height * self._scale * self._scale_y
                x = self._x
                y = self._y
                r = -math.radians(self._rotation)
                cr = math.cos(r)
                sr = math.sin(r)
                ax = int(x1 * cr - y1 * sr + x)
                ay = int(x1 * sr + y1 * cr + y)
                bx = int(x2 * cr - y1 * sr + x)
                by = int(x2 * sr + y1 * cr + y)
                cx = int(x2 * cr - y2 * sr + x)
                cy = int(x2 * sr + y2 * cr + y)
                dx = int(x1 * cr - y2 * sr + x)
                dy = int(x1 * sr + y2 * cr + y)
                self._vertex_list.vertices[:] = [
                 ax, ay, bx, by, cx, cy, dx, dy]
            elif not self._scale != 1.0:
                if self._scale_x != 1.0 or self._scale_y != 1.0:
                    x1 = int(self._x - self._image_anchor_x * self._scale * self._scale_x)
                    y1 = int(self._y - self._image_anchor_y * self._scale * self._scale_y)
                    x2 = int(x1 + img.width * self._scale * self._scale_x)
                    y2 = int(y1 + img.height * self._scale * self._scale_y)
                    self._vertex_list.vertices[:] = [x1, y1, x2, y1, x2, y2, x1, y2]
            else:
                x1 = int(self._x - self._image_anchor_x)
                y1 = int(self._y - self._image_anchor_y)
                x2 = x1 + img.width
                y2 = y1 + img.height
                self._vertex_list.vertices[:] = [x1, y1, x2, y1, x2, y2, x1, y2]
        else:
            x1 = int(-self._image_anchor_x)
            y1 = int(-self._image_anchor_y)
            x2 = x1 + img.width
            y2 = y1 + img.height
            m = self.get_local_transform()
            p1 = m * euclid.Point2(x1, y1)
            p2 = m * euclid.Point2(x2, y1)
            p3 = m * euclid.Point2(x2, y2)
            p4 = m * euclid.Point2(x1, y2)
            self._vertex_list.vertices[:] = [
             int(p1.x), int(p1.y), int(p2.x), int(p2.y),
             int(p3.x), int(p3.y), int(p4.x), int(p4.y)]


Sprite.supported_classes = Sprite