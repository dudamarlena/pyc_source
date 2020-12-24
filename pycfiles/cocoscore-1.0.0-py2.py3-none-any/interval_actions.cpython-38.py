# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../..\cocos\actions\interval_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 21905 bytes
__doc__ = 'Interval Action\n\nInterval Actions\n================\n\nAn interval action is an action that takes place within a certain period of time.\nIt has an start time, and a finish time. The finish time is the parameter\n``duration`` plus the start time.\n\nThese `IntervalAction` have some interesting properties, like:\n\n  - They can run normally (default)\n  - They can run reversed with the `Reverse` action.\n  - They can run with the time altered with the `Accelerate`, `AccelDeccel` and\n    `Speed` actions.\n\nFor example, you can simulate a Ping Pong effect running the action normally and\nthen running it again in Reverse mode.\n\nExample::\n\n    ping_pong_action = action + Reverse(action)\n\n\nAvailable IntervalActions\n=========================\n\n  * `MoveTo`\n  * `MoveBy`\n  * `JumpTo`\n  * `JumpBy`\n  * `Bezier`\n  * `Blink`\n  * `RotateTo`\n  * `RotateBy`\n  * `ScaleTo`\n  * `ScaleBy`\n  * `FadeOut`\n  * `FadeIn`\n  * `FadeTo`\n  * `Delay`\n  * `RandomDelay`\n\n\nModifier actions\n================\n\n  * `Accelerate`\n  * `AccelDeccel`\n  * `Speed`\n\n\nExamples::\n\n    move = MoveBy((200,0), duration=5)  # Moves 200 pixels to the right in 5 seconds.\n\n    move = MoveTo((320,240), duration=5) # Moves to the pixel (320,240) in 5 seconds\n\n    jump = JumpBy((320,0), 100, 5, duration=5) # Jumps to the right 320 pixels\n                                                # doing 5 jumps of 100 pixels\n                                                # of height in 5 seconds\n\n    accel_move = Accelerate(move)               # accelerates action move\n'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import random, copy, math
from .base_actions import *
from cocos.euclid import *
__all__ = [
 'Lerp',
 'MoveTo', 'MoveBy',
 'Jump', 'JumpTo', 'JumpBy',
 'Bezier',
 'Rotate', 'RotateTo', 'RotateBy',
 'ScaleTo', 'ScaleBy',
 'Delay', 'RandomDelay',
 'FadeOut', 'FadeIn', 'FadeTo',
 'Blink',
 'Accelerate', 'AccelDeccel', 'Speed']

class Lerp(IntervalAction):
    """Lerp"""

    def init(self, attrib, start, end, duration):
        """Init method.

        :Parameters:
            `attrib` : string
                The name of the attrbiute where the value is stored
            `start`  : float
                The start value
            `end`    : float
                The end value
            `duration` : float
                Duration time in seconds
        """
        self.attrib = attrib
        self.duration = duration
        self.start_p = start
        self.end_p = end
        self.delta = end - start

    def update(self, t):
        setattr(self.target, self.attrib, self.start_p + self.delta * t)

    def __reversed__(self):
        return Lerp(self.attrib, self.end_p, self.start_p, self.duration)


class RotateBy(IntervalAction):
    """RotateBy"""

    def init(self, angle, duration):
        """Init method.

        :Parameters:
            `angle` : float
                Degrees that the sprite will be rotated.
                Positive degrees rotates the sprite clockwise.
            `duration` : float
                Duration time in seconds
        """
        self.angle = angle
        self.duration = duration

    def start(self):
        self.start_angle = self.target.rotation

    def update(self, t):
        self.target.rotation = (self.start_angle + self.angle * t) % 360

    def __reversed__(self):
        return RotateBy(-self.angle, self.duration)


Rotate = RotateBy

class RotateTo(IntervalAction):
    """RotateTo"""

    def init(self, angle, duration):
        """Init method.

        :Parameters:
            `angle` : float
                Destination angle in degrees.
            `duration` : float
                Duration time in seconds
        """
        self.angle = angle % 360
        self.duration = duration

    def start(self):
        ea = self.angle
        sa = self.start_angle = self.target.rotation % 360
        self.angle = ea % 360 - sa % 360
        if self.angle > 180:
            self.angle = -360 + self.angle
        if self.angle < -180:
            self.angle = 360 + self.angle

    def update(self, t):
        self.target.rotation = (self.start_angle + self.angle * t) % 360

    def __reversed__(self):
        return RotateTo(-self.angle, self.duration)


class Speed(IntervalAction):
    """Speed"""

    def init(self, other, speed):
        """Init method.

        :Parameters:
            `other` : IntervalAction
                The action that will be affected
            `speed` : float
                The speed change. 1 is no change.
                2 means twice as fast, takes half the time
                0.5 means half as fast, takes double the time
        """
        self.other = other
        self.speed = speed
        self.duration = other.duration / speed

    def start(self):
        self.other.target = self.target
        self.other.start()

    def update(self, t):
        self.other.update(t)

    def __reversed__(self):
        return Speed(Reverse(self.other), self.speed)


class Accelerate(IntervalAction):
    """Accelerate"""

    def init(self, other, rate=2):
        """Init method.

        :Parameters:
            `other` : IntervalAction
                The action that will be affected
            `rate` : float
                The acceleration rate. 1 is linear.
                the new t is t**rate
        """
        self.other = other
        self.rate = rate
        self.duration = other.duration

    def start(self):
        self.other.target = self.target
        self.other.start()

    def update(self, t):
        self.other.update(t ** self.rate)

    def __reversed__(self):
        return Accelerate(Reverse(self.other), 1.0 / self.rate)


class AccelDeccel(IntervalAction):
    """AccelDeccel"""

    def init(self, other):
        """Init method.

        :Parameters:
            `other` : IntervalAction
                The action that will be affected
        """
        self.other = other
        self.duration = other.duration

    def start(self):
        self.other.target = self.target
        self.other.start()

    def update(self, t):
        if t != 1.0:
            ft = (t - 0.5) * 12
            t = 1.0 / (1.0 + math.exp(-ft))
        self.other.update(t)

    def __reversed__(self):
        return AccelDeccel(Reverse(self.other))


class MoveTo(IntervalAction):
    """MoveTo"""

    def init(self, dst_coords, duration=5):
        """Init method.

        :Parameters:
            `dst_coords` : (x,y)
                Coordinates where the sprite will be placed at the end of the action
            `duration` : float
                Duration time in seconds
        """
        self.end_position = Point2(*dst_coords)
        self.duration = duration

    def start(self):
        self.start_position = self.target.position
        self.delta = self.end_position - self.start_position

    def update(self, t):
        self.target.position = self.start_position + self.delta * t


class MoveBy(MoveTo):
    """MoveBy"""

    def init(self, delta, duration=5):
        """Init method.

        :Parameters:
            `delta` : (x,y)
                Delta coordinates
            `duration` : float
                Duration time in seconds
        """
        self.delta = Point2(*delta)
        self.duration = duration

    def start(self):
        self.start_position = self.target.position
        self.end_position = self.start_position + self.delta

    def __reversed__(self):
        return MoveBy(-self.delta, self.duration)


class FadeOut(IntervalAction):
    """FadeOut"""

    def init(self, duration):
        """Init method.

        :Parameters:
            `duration` : float
                Seconds that it will take to fade
        """
        self.duration = duration

    def update(self, t):
        self.target.opacity = 255 * (1 - t)

    def __reversed__(self):
        return FadeIn(self.duration)


class FadeTo(IntervalAction):
    """FadeTo"""

    def init(self, alpha, duration):
        """Init method.

        :Parameters:
            `alpha` : float
                0-255 value of opacity
            `duration` : float
                Seconds that it will take to fade
        """
        self.alpha = alpha
        self.duration = duration

    def start(self):
        self.start_alpha = self.target.opacity

    def update(self, t):
        self.target.opacity = self.start_alpha + (self.alpha - self.start_alpha) * t


class FadeIn(FadeOut):
    """FadeIn"""

    def update(self, t):
        self.target.opacity = 255 * t

    def __reversed__(self):
        return FadeOut(self.duration)


class ScaleTo(IntervalAction):
    """ScaleTo"""

    def init(self, scale, duration=5):
        """Init method.

        :Parameters:
            `scale` : float
                scale factor
            `duration` : float
                Duration time in seconds
        """
        self.end_scale = scale
        self.duration = duration

    def start(self):
        self.start_scale = self.target.scale
        self.delta = self.end_scale - self.start_scale

    def update(self, t):
        self.target.scale = self.start_scale + self.delta * t


class ScaleBy(ScaleTo):
    """ScaleBy"""

    def start(self):
        self.start_scale = self.target.scale
        self.delta = self.start_scale * self.end_scale - self.start_scale

    def __reversed__(self):
        return ScaleBy(1.0 / self.end_scale, self.duration)


class Blink(IntervalAction):
    """Blink"""

    def init(self, times, duration):
        """Init method.

        :Parameters:
            `times` : integer
                Number of times to blink
            `duration` : float
                Duration time in seconds
        """
        self.times = times
        self.duration = duration

    def start(self):
        self.end_invisible = not self.target.visible

    def update(self, t):
        slice = 1.0 / self.times
        m = t % slice
        self.target.visible = self.end_invisible ^ (m < slice / 2.0)

    def __reversed__(self):
        return self


class Bezier(IntervalAction):
    """Bezier"""

    def init(self, bezier, duration=5, forward=True):
        """Init method

        :Parameters:
            `bezier` : bezier_configuration instance
                A bezier configuration
            `duration` : float
                Duration time in seconds
        """
        self.duration = duration
        self.bezier = bezier
        self.forward = forward

    def start(self):
        self.start_position = self.target.position

    def update(self, t):
        if self.forward:
            p = self.bezier.at(t)
        else:
            p = self.bezier.at(1 - t)
        self.target.position = self.start_position + Point2(*p)

    def __reversed__(self):
        return Bezier(self.bezier, self.duration, not self.forward)


class Jump(IntervalAction):
    """Jump"""

    def init(self, y=150, x=120, jumps=1, duration=5):
        """Init method

        :Parameters:
            `y` : integer
                Height of jumps
            `x` : integer
                horizontal movement relative to the startin position
            `jumps` : integer
                quantity of jumps
            `duration` : float
                Duration time in seconds
        """
        import warnings
        warnings.warn('Deprecated "Jump" action. Consider using JumpBy instead', DeprecationWarning)
        self.y = y
        self.x = x
        self.duration = duration
        self.jumps = jumps

    def start(self):
        self.start_position = self.target.position

    def update(self, t):
        y = int(self.y * abs(math.sin(t * math.pi * self.jumps)))
        x = self.x * t
        self.target.position = self.start_position + Point2(x, y)

    def __reversed__(self):
        return Jump(self.y, -self.x, self.jumps, self.duration)


class JumpBy(IntervalAction):
    """JumpBy"""

    def init(self, position=(0, 0), height=100, jumps=1, duration=5):
        """Init method

        :Parameters:
            `position` : integer x integer tuple
                horizontal and vertical movement relative to the
                starting position
            `height` : integer
                Height of jumps
            `jumps` : integer
                quantity of jumps
            `duration` : float
                Duration time in seconds
        """
        self.position = position
        self.height = height
        self.duration = duration
        self.jumps = jumps

    def start(self):
        self.start_position = self.target.position
        self.delta = Vector2(*self.position)

    def update(self, t):
        y = self.height * abs(math.sin(t * math.pi * self.jumps))
        y = int(y + self.delta[1] * t)
        x = self.delta[0] * t
        self.target.position = self.start_position + Point2(x, y)

    def __reversed__(self):
        return JumpBy((-self.position[0], -self.position[1]), self.height, self.jumps, self.duration)


class JumpTo(JumpBy):
    """JumpTo"""

    def start(self):
        self.start_position = self.target.position
        self.delta = Vector2(*self.position) - self.start_position


class Delay(IntervalAction):
    """Delay"""

    def init(self, delay):
        """Init method

        :Parameters:
            `delay` : float
                Seconds of delay
        """
        self.duration = delay

    def __reversed__(self):
        return self


class RandomDelay(Delay):
    """RandomDelay"""

    def init(self, low, hi):
        """Init method

        :Parameters:
            `low` : float
                Minimun seconds of delay
            `hi` : float
                Maximun seconds of delay
        """
        self.low = low
        self.hi = hi

    def __deepcopy__(self, memo):
        new = copy.copy(self)
        new.duration = self.low + random.random() * (self.hi - self.low)
        return new

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError('Can only multiply actions by ints')
        if other <= 1:
            return self
        return RandomDelay(self.low * other, self.hi * other)