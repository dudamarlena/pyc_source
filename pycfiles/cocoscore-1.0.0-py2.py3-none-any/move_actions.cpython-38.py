# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\actions\move_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 7686 bytes
__doc__ = "Actions for moving things around based on their velocity and\nacceleration.\n\nThe simplest usage:\n\n    sprite = cocos.sprite.Sprite('ship.png')\n    sprite.velocity = (100, 100)\n    sprite.do(Move())\n\nThis will move the sprite (100, 100) pixels per second indefinitely.\n\nTypically the sprite would be controlled by the user, so something like::\n\n keys = <standard pyglet keyboard state handler>\n\n class MoveShip(Move):\n    def step(self, dt):\n        super(MoveShip, self).step(dt)\n        self.target.dr = (keys[key.RIGHT] - keys[key.LEFT]) * 360\n        rotation = math.pi * self.target.rotation / 180.0\n        rotation_x = math.cos(-rotation)\n        rotation_y = math.sin(-rotation)\n        if keys[key.UP]:\n            self.target.acceleration = (200 * rotation_x, 200 * rotation_y)\n\n ship.do(MoveShip())\n\n"
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
__all__ = [
 'Move', 'WrappedMove', 'BoundedMove', 'Driver']
import math
from .base_actions import Action

class Move(Action):
    """Move"""

    def step(self, dt):
        x, y = self.target.position
        dx, dy = self.target.velocity
        ddx, ddy = getattr(self.target, 'acceleration', (0, 0))
        gravity = getattr(self.target, 'gravity', 0)
        dx += ddx * dt
        dy += (ddy + gravity) * dt
        self.target.velocity = (dx, dy)
        x += dx * dt
        y += dy * dt
        self.target.position = (x, y)
        dr = getattr(self.target, 'dr', 0)
        ddr = getattr(self.target, 'ddr', 0)
        if dr or ddr:
            dr = self.target.dr = dr + ddr * dt
        if dr:
            self.target.rotation += dr * dt


class WrappedMove(Move):
    """WrappedMove"""

    def init(self, width, height):
        """Init method.

        :Parameters:
            `width` : integer
                The width to wrap position at.
            `height` : integer
                The height to wrap position at.
        """
        self.width, self.height = width, height

    def step(self, dt):
        super(WrappedMove, self).step(dt)
        x, y = self.target.position
        w, h = self.target.width, self.target.height
        if x > self.width + w / 2:
            x -= self.width + w
        elif x < 0 - w / 2:
            x += self.width + w
        if y > self.height + h / 2:
            y -= self.height + h
        elif y < 0 - h / 2:
            y += self.height + h
        self.target.position = (
         x, y)


class BoundedMove(Move):
    """BoundedMove"""

    def init(self, width, height):
        """Init method.

        :Parameters:
            `width` : integer
                The width to bound position at.
            `height` : integer
                The height to bound position at.
        """
        self.width, self.height = width, height

    def step(self, dt):
        super(BoundedMove, self).step(dt)
        x, y = self.target.position
        w, h = self.target.width, self.target.height
        if x > self.width - w / 2:
            x = self.width - w / 2
        elif x < w / 2:
            x = w / 2
        if y > self.height - h / 2:
            y = self.height - h / 2
        elif y < h / 2:
            y = h / 2
        self.target.position = (
         x, y)


class Driver(Action):
    """Driver"""

    def step(self, dt):
        accel = getattr(self.target, 'acceleration', 0)
        speed = getattr(self.target, 'speed', 0)
        max_forward = getattr(self.target, 'max_forward_speed', None)
        max_reverse = getattr(self.target, 'max_reverse_speed', None)
        if accel:
            speed += dt * accel
            if max_forward is not None:
                if self.target.speed > max_forward:
                    speed = max_forward
            if max_reverse is not None:
                if self.target.speed < max_reverse:
                    speed = max_reverse
        r = math.radians(self.target.rotation)
        s = dt * speed
        x, y = self.target.position
        self.target.position = (x + math.sin(r) * s, y + math.cos(r) * s)
        self.target.speed = speed