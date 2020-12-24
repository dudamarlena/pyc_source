# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\mapcolliders.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 17203 bytes
"""Support for handling collisions between an actor and a container of objects"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'

class RectMapCollider(object):
    __doc__ = 'Helper to handle collisions between an actor and objects in a RectMapLayer\n\n    Arguments:\n        velocity_on_bump (str) : one of ``"bounce"``, ``"stick"``, ``"slide"``.\n            selects which of the predefined on_bump handlers will be used\n    Attributes:\n        on_bump_handler : method to change velocity when a collision was detected\n        bumped_x (bool) : True if collide_map detected collision in the x-axis\n        bumped_y (bool) : True if collide_map detected collision in the y-axis\n\n    The code that updates actor position and velocity would call\n    method :meth:`collide_map` to account for collisions\n\n    There are basically two ways to include this functionality into an\n    actor class\n\n        - as a component, essentially passing (mapcollider, maplayer) in\n          the actor\'s __init__\n        - mixin style, by using RectMapCollider or a subclass as a secondary\n          base class for actor.\n\n    Component way is more decoupled, Mixin style is more powerful because\n    the collision code will have access to the entire actor trough his \'self\'.\n\n    To have a working instance the behavior of velocity in a collision must be\n    defined, and that\'s the job of method `on_bump_handler`\n\n        - if one of the stock on_bump_<variant> suits the requirements, suffices\n            `mapcollider.on_bump_handler = mapcollider.on_bump_<desired variant>`\n          or passing a selector at instantiation time\n            `mapcollider = MapCollider(<desired variant>)`\n\n        - for custom behavior define on_bump_handler in a subclass and instantiate it.\n\n    '

    def __init__(self, velocity_on_bump=None):
        if velocity_on_bump is not None:
            self.on_bump_handler = getattr(self, 'on_bump_' + velocity_on_bump)

    def collide_bottom(self, obj):
        """placeholder, called when collision with obj's bottom side detected"""
        pass

    def collide_left(self, obj):
        """placeholder, called when collision with obj's left side detected"""
        pass

    def collide_right(self, obj):
        """placeholder, called when collision with obj's right side detected"""
        pass

    def collide_top(self, obj):
        """placeholder, called when collision with obj's top side detected"""
        pass

    def on_bump_bounce(self, vx, vy):
        """Bounces when a wall is touched.

        Example use case: bouncing projectiles.
        """
        if self.bumped_x:
            vx = -vx
        if self.bumped_y:
            vy = -vy
        return (
         vx, vy)

    def on_bump_stick(self, vx, vy):
        """Stops all movement when any wall is touched.

        Example use case: sticky bomb, hook weapon projectile.
        """
        if self.bumped_x or self.bumped_y:
            vx = vy = 0.0
        return (
         vx, vy)

    def on_bump_slide(self, vx, vy):
        """Blocks movement only in the axis that touched a wall.

        Example use case: player in a platformer game.
        """
        if self.bumped_x:
            vx = 0.0
        if self.bumped_y:
            vy = 0.0
        return (
         vx, vy)

    def on_bump_handler(self, vx, vy):
        """Returns velocity after all collisions considered by collide_map

        Arguments:
            vx (float) : velocity in x-axis before collision
            vy (float) : velocity in y-axis before collision

        Returns:
            (vx, vx) : velocity after all collisions considered in collide_map

        This is a placeholder, either define a custom one or replace with one
        of the stock on_bump_<bump_style> methods
        """
        raise ValueError(self.__class__.__name__ + '.on_bump_handler must be set to a real handler before calling.')
        return (
         vx, vy)

    def collide_map(self, maplayer, last, new, vx, vy):
        """Constrains a movement ``last`` -> ``new`` by considering collisions

        Arguments:
            maplayer (RectMapLayer) : layer with solid objects to collide with.
            last (Rect) : actor rect before step.
            new (Rect): tentative rect after the stepm will be adjusted.
            vx (float) : velocity in x-axis used to calculate 'last' -> 'new'
            vy (float) : velocity in y-axis used to calculate 'last' -> 'new'

        Returns:
            (vx, vy) (float, float) : the possibly modified (vx, vy).

        Assumes:
            'last' does not collide with any object.

            The dt involved in 'last' -> 'new' is small enough that no object
            can entirely fit between 'last' and 'new'.

        Side effects:
            ``new`` eventually modified to not be into forbidden area.
            For each collision with one object's side detected, the method
            ``self.collide_<side>(obj)`` is called.

        if rect ``new`` does not overlap any object in maplayer, the method
            - does not modify ``new``.
            - returns unchanged (vx, vy).
            - no method ``self.collide_<side>`` is called.
            - ``self.bumped_x`` and ``self.bumped_y`` both will be ``False``.

        if rect ``new`` does overlaps any object in maplayer, the method:
            - modifies ``new`` to be the nearest rect to the original ``new``
              rect that it is still outside any maplayer object.
            - returns a modified (vx, vy) as specified by self.on_bump_handler.
            - after return self.bumped_x  (resp self.bumped_y) will be True if
              an horizontal (resp vertical) collision happened.
            - if the movement from ``last`` to the original ``new`` was stopped
              by side <side> of object <obj>, then self.collide_<side>(obj) will be called.

        Implementation details

        Adjusts ``new`` in two passes against each object in maplayer.

        In pass one, ``new`` is collision tested against each object in maplayer:
            - if collides only in one axis, ``new`` is adjusted as close as possible but not overlapping object
            - if not overlapping, nothing is done
            - if collision detected on both axis, let second pass handle it

        In pass two, ``new`` is collision tested against the objects with double collisions in pass one:
            - if a collision is detected, adjust ``new`` as close as possible but not overlapping object,
              ie. use the smallest displacement on either X or Y axis. If they are both equal, move on
              both axis.
        """
        self.bumped_x = False
        self.bumped_y = False
        objects = (maplayer.get_in_region)(*new.bottomleft + new.topright)
        collide_later = set()
        for obj in objects:
            if not (obj is None or obj.tile is None):
                if not obj.intersects(new):
                    pass
                else:
                    dx_correction, dy_correction = self.detect_collision(obj, last, new)
                    if dx_correction == 0.0 or dy_correction == 0.0:
                        self.resolve_collision(obj, new, dx_correction, dy_correction)
                    else:
                        collide_later.add(obj)
            for obj in collide_later:
                if obj.intersects(new):
                    dx_correction, dy_correction = self.detect_collision(obj, last, new)
                    if abs(dx_correction) < abs(dy_correction):
                        dy_correction = 0.0
                    else:
                        if abs(dy_correction) < abs(dx_correction):
                            dx_correction = 0.0
                    self.resolve_collision(obj, new, dx_correction, dy_correction)
                vx, vy = self.on_bump_handler(vx, vy)
                return (
                 vx, vy)

    def detect_collision(self, obj, last, new):
        """returns minimal correction in each axis to not collide with obj

        Arguments:
            obj : object in a MapLayer
            last (Rect) : starting rect for the actor step
            new (Rect) : tentative actor's rect after step

        Decides if there is a collision with obj when moving ``last`` -> ``new``
        and then returns the minimal correctioin in each axis as to not collide.
        
        It can be overridden to be more selective about when a collision exists
        (see the matching method in :class:`RectMapWithPropsCollider` for example).
        """
        dx_correction = dy_correction = 0.0
        if last.bottom >= obj.top > new.bottom:
            dy_correction = obj.top - new.bottom
        else:
            if last.top <= obj.bottom < new.top:
                dy_correction = obj.bottom - new.top
            else:
                if last.right <= obj.left < new.right:
                    dx_correction = obj.left - new.right
                else:
                    pass
                if last.left >= obj.right > new.left:
                    dx_correction = obj.right - new.left
            return (
             dx_correction, dy_correction)

    def resolve_collision(self, obj, new, dx_correction, dy_correction):
        """Corrects ``new`` to just avoid collision with obj, does side effects.

        Arguments:
            obj (obj) : the object colliding with ``new``.
            new (Rect) : tentative actor position before considering
                collision with ``obj``.
            dx_correction (float) : smallest correction needed on
                ``new`` x position not to collide ``obj``.
            dy_correction (float) : smallest correction needed on
            ``new`` y position not to collide ``obj``.

        The correction is applied to ``new`` position.

        If a collision along the x-axis (respectively y-axis) was detected,
        the flag ``self.bumped_x`` (resp y) is set.

        If the movement towards the original ``new`` was stopped by side <side>
        of object <obj>, then ``self.collide_<side>(obj)`` will be called.
        """
        if dx_correction != 0.0:
            self.bumped_x = True
            new.left += dx_correction
            if dx_correction > 0.0:
                self.collide_left(obj)
            else:
                self.collide_right(obj)
        elif dy_correction != 0.0:
            self.bumped_y = True
            new.top += dy_correction
            if dy_correction > 0.0:
                self.collide_bottom(obj)
            else:
                self.collide_top(obj)


class RectMapWithPropsCollider(RectMapCollider):
    __doc__ = 'Helper to handle collisions between an actor and objects in a RectMapLayer\n\n    Same as RectMapCollider except that collision detection is more fine grained.\n    Collision happens only on objects sides with prop(<side>) set.\n\n    Look at :class:`RectMapCollider` for details\n    '

    def detect_collision(self, obj, last, new):
        """Returns minimal correction in each axis to not collide with obj

        Collision happens only on objects sides with prop <side> set.
        """
        g = obj.get
        dx_correction = dy_correction = 0.0
        if g('top'):
            if last.bottom >= obj.top > new.bottom:
                dy_correction = obj.top - new.bottom
            else:
                pass
        if g('bottom'):
            if last.top <= obj.bottom < new.top:
                dy_correction = obj.bottom - new.top
            elif g('left'):
                if last.right <= obj.left < new.right:
                    dx_correction = obj.left - new.right
                else:
                    pass
        elif g('right'):
            if last.left >= obj.right > new.left:
                dx_correction = obj.right - new.left
        return (
         dx_correction, dy_correction)


class TmxObjectMapCollider(RectMapCollider):
    __doc__ = 'Helper to handle collisions between an actor and objects in a TmxObjectLayer\n\n    Same as RectMapCollider except maplayer is expected to be a :class:`TmxObjectLayer`, so\n    the objects to collide are TmxObject instances.\n\n    Look at :class:`RectMapCollider` for details\n    '

    def collide_map(self, maplayer, last, new, vx, vy):
        """Constrains a movement ``last`` -> ``new`` by considering collisions

        Arguments:
            maplayer (RectMapLayer) : layer with solid objects to collide with.
            last (Rect) : actor rect before step.
            new (Rect): tentative rect after the stepm will be adjusted.
            vx (float) : velocity in x-axis used to calculate 'last' -> 'new'
            vy (float) : velocity in y-axis used to calculate 'last' -> 'new'

        Returns:
            vx, vy (float, float) : the possibly modified (vx, vy).

        See :meth:`RectMapCollider.collide_map` for side effects and details
        """
        self.bumped_x = False
        self.bumped_y = False
        objects = (maplayer.get_in_region)(*new.bottomleft + new.topright)
        collide_later = set()
        for obj in objects:
            if not obj.intersects(new):
                pass
            else:
                dx_correction, dy_correction = self.detect_collision(obj, last, new)
                if dx_correction == 0.0 or dy_correction == 0.0:
                    self.resolve_collision(obj, new, dx_correction, dy_correction)
                else:
                    collide_later.add(obj)
        else:
            for obj in collide_later:
                if obj.intersects(new):
                    dx_correction, dy_correction = self.detect_collision(obj, last, new)
                    if abs(dx_correction) < abs(dy_correction):
                        dy_correction = 0.0
                    else:
                        if abs(dy_correction) < abs(dx_correction):
                            dx_correction = 0.0
                    self.resolve_collision(obj, new, dx_correction, dy_correction)
                vx, vy = self.on_bump_handler(vx, vy)
                return (
                 vx, vy)


def make_collision_handler(collider, maplayer):
    """Returns ``f = collider.collide_map(maplayer, ...)``

    Returns:
        f : ``(last, new, vx, vy)`` -> ``(vx, vy)``

    Utility function to create a collision handler by combining

    Arguments:
       maplayer : tells the objects to collide with.
       collider : tells how velocity changes on collision and resolves
           actual collisions.
    """

    def collision_handler(last, new, vx, vy):
        return collider.collide_map(maplayer, last, new, vx, vy)

    return collision_handler