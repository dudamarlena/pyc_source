# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\actions\move_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 7686 bytes
"""Actions for moving things around based on their velocity and
acceleration.

The simplest usage:

    sprite = cocos.sprite.Sprite('ship.png')
    sprite.velocity = (100, 100)
    sprite.do(Move())

This will move the sprite (100, 100) pixels per second indefinitely.

Typically the sprite would be controlled by the user, so something like::

 keys = <standard pyglet keyboard state handler>

 class MoveShip(Move):
    def step(self, dt):
        super(MoveShip, self).step(dt)
        self.target.dr = (keys[key.RIGHT] - keys[key.LEFT]) * 360
        rotation = math.pi * self.target.rotation / 180.0
        rotation_x = math.cos(-rotation)
        rotation_y = math.sin(-rotation)
        if keys[key.UP]:
            self.target.acceleration = (200 * rotation_x, 200 * rotation_y)

 ship.do(MoveShip())

"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
__all__ = [
 'Move', 'WrappedMove', 'BoundedMove', 'Driver']
import math
from .base_actions import Action

class Move(Action):
    __doc__ = 'Move the target based on parameters on the target.\n\n    For movement the parameters are::\n\n        target.position = (x, y)\n        target.velocity = (dx, dy)\n        target.acceleration = (ddx, ddy) = (0, 0)\n        target.gravity = 0\n\n    And rotation::\n\n        target.rotation\n        target.dr\n        target.ddr\n    '

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
    __doc__ = 'Move the target but wrap position when it hits certain bounds.\n\n    Wrap occurs outside of 0 < x < width and 0 < y < height taking into\n    account the dimenstions of the target.\n    '

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
        else:
            if x < 0 - w / 2:
                x += self.width + w
            elif y > self.height + h / 2:
                y -= self.height + h
            else:
                if y < 0 - h / 2:
                    y += self.height + h
            self.target.position = (
             x, y)


class BoundedMove(Move):
    __doc__ = 'Move the target but limit position when it hits certain bounds.\n\n    Position is bounded to 0 < x < width and 0 < y < height taking into\n    account the dimenstions of the target.\n    '

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
        else:
            if x < w / 2:
                x = w / 2
            elif y > self.height - h / 2:
                y = self.height - h / 2
            else:
                if y < h / 2:
                    y = h / 2
            self.target.position = (
             x, y)


class Driver(Action):
    __doc__ = "Drive a `CocosNode` object around like a car in x, y according to\n    a direction and speed.\n\n    Example::\n\n        # control the movement of the given sprite\n        sprite.do(Driver())\n\n        ...\n        sprite.rotation = 45\n        sprite.speed = 100\n        ...\n\n    The sprite MAY have these parameters (beyond the standard position\n    and rotation):\n\n        `speed` : float\n            Speed to move at in pixels per second in the direction of\n            the target's rotation.\n        `acceleration` : float\n            If specified will automatically be added to speed.\n            Specified in pixels per second per second.\n        `max_forward_speed` : float (default None)\n            Limits to apply to speed when updating with acceleration.\n        `max_reverse_speed` : float (default None)\n            Limits to apply to speed when updating with acceleration.\n    "

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