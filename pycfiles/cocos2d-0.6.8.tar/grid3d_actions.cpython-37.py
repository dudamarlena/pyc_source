# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\actions\grid3d_actions.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 18026 bytes
"""Implementation of Grid3DAction actions
"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import math, random
import cocos.director as director
from cocos.euclid import *
from .basegrid_actions import *
rr = random.randrange
__all__ = [
 'Waves3D',
 'FlipX3D',
 'FlipY3D',
 'Lens3D',
 'Shaky3D',
 'Ripple3D',
 'Liquid',
 'Waves',
 'Twirl']

class Waves3D(Grid3DAction):
    __doc__ = 'Simulates waves using the math.sin() function in the z-axis\n    The x and y coordinates remains unmodified.\n\n    Example::\n\n       scene.do(Waves3D(waves=5, amplitude=40, grid=(16,16), duration=10))\n    '

    def init(self, waves=4, amplitude=20, *args, **kw):
        """
        :Parameters:
            `waves` : int
                Number of waves (2 * pi) that the action will perform. Default is 4
            `amplitude` : int
                Wave amplitude (height). Default is 20
        """
        (super(Waves3D, self).init)(*args, **kw)
        self.waves = waves
        self.amplitude_rate = 1.0
        self.amplitude = amplitude

    def update(self, t):
        for i in range(0, self.grid.x + 1):
            for j in range(0, self.grid.y + 1):
                x, y, z = self.get_original_vertex(i, j)
                z += math.sin(t * math.pi * self.waves * 2 + (y + x) * 0.01) * self.amplitude * self.amplitude_rate
                self.set_vertex(i, j, (x, y, z))


class FlipX3D(Grid3DAction):
    __doc__ = 'FlipX3D flips the screen using the Y-axis as a pivot.'

    def init(self, grid=(1, 1), *args, **kw):
        if grid != (1, 1):
            raise GridException('Invalid grid size.')
        (super(FlipX3D, self).init)(args, grid=grid, **kw)

    def update(self, t):
        angle = math.pi * t
        mz = math.sin(angle)
        angle = angle / 2.0
        mx = math.cos(angle)
        x0, y, z = self.get_original_vertex(1, 1)
        x1, y, z = self.get_original_vertex(0, 0)
        if x0 > x1:
            a = (0, 0)
            b = (0, 1)
            c = (1, 0)
            d = (1, 1)
            x = x0
        else:
            c = (0, 0)
            d = (0, 1)
            a = (1, 0)
            b = (1, 1)
            x = x1
        diff_x = x - x * mx
        diff_z = abs(x * mz // 4.0)
        x, y, z = (self.get_original_vertex)(*a)
        self.set_vertex(a[0], a[1], (diff_x, y, z + diff_z))
        x, y, z = (self.get_original_vertex)(*b)
        self.set_vertex(b[0], b[1], (diff_x, y, z + diff_z))
        x, y, z = (self.get_original_vertex)(*c)
        self.set_vertex(c[0], c[1], (x - diff_x, y, z - diff_z))
        x, y, z = (self.get_original_vertex)(*d)
        self.set_vertex(d[0], d[1], (x - diff_x, y, z - diff_z))


class FlipY3D(Grid3DAction):
    __doc__ = 'FlipY3D flips the screen using the X-axis as a pivot.'

    def init(self, grid=(1, 1), *args, **kw):
        if grid != (1, 1):
            raise GridException('Invalid grid size.')
        (super(FlipY3D, self).init)(args, grid=grid, **kw)

    def update(self, t):
        angle = math.pi * t
        mz = math.sin(angle)
        angle = angle / 2.0
        my = math.cos(angle)
        x, y0, z = self.get_original_vertex(1, 1)
        x, y1, z = self.get_original_vertex(0, 0)
        if y0 > y1:
            a = (0, 0)
            b = (0, 1)
            c = (1, 0)
            d = (1, 1)
            y = y0
        else:
            b = (0, 0)
            a = (0, 1)
            d = (1, 0)
            c = (1, 1)
            y = y1
        diff_y = y - y * my
        diff_z = abs(y * mz // 4.0)
        x, y, z = (self.get_original_vertex)(*a)
        self.set_vertex(a[0], a[1], (x, diff_y, z + diff_z))
        x, y, z = (self.get_original_vertex)(*b)
        self.set_vertex(b[0], b[1], (x, y - diff_y, z - diff_z))
        x, y, z = (self.get_original_vertex)(*c)
        self.set_vertex(c[0], c[1], (x, diff_y, z + diff_z))
        x, y, z = (self.get_original_vertex)(*d)
        self.set_vertex(d[0], d[1], (x, y - diff_y, z - diff_z))


class Lens3D(Grid3DAction):
    __doc__ = 'Lens simulates a Lens / Magnifying glass effect.\n    It modifies the z-coordinate while the x and y remains unmodified.\n\n    Example::\n\n       scene.do(Lens3D(center=(320,240), radius=150, grid=(16,16), duration=10))\n    '

    def init(self, center=(-1, -1), radius=160, lens_effect=0.7, *args, **kw):
        """
        :Parameters:
            `center` : (int,int)
                Center of the lens. Default: (win_size_width /2, win_size_height /2 )
            `radius` : int
                Radius of the lens.
            `lens_effect` : float
                How strong is the lens effect. Default: 0.7. 0 is no effect at all, 1 is a very strong lens effect.
        """
        (super(Lens3D, self).init)(*args, **kw)
        x, y = director.get_window_size()
        if center == (-1, -1):
            center = (
             x // 2, y // 2)
        self.position = Point2(center[0] + 1, center[1] + 1)
        self.radius = radius
        self.lens_effect = lens_effect
        self._last_position = (-1000, -1000)

    def update(self, t):
        if self.position != self._last_position:
            for i in range(0, self.grid.x + 1):
                for j in range(0, self.grid.y + 1):
                    x, y, z = self.get_original_vertex(i, j)
                    p = Point2(x, y)
                    vect = self.position - p
                    r = abs(vect)
                    if r < self.radius:
                        r = self.radius - r
                        pre_log = r / self.radius
                        if pre_log == 0:
                            pre_log = 0.001
                        l = math.log(pre_log) * self.lens_effect
                        new_r = math.exp(l) * self.radius
                        vect.normalize()
                        new_vect = vect * new_r
                        z += abs(new_vect) * self.lens_effect
                    self.set_vertex(i, j, (x, y, z))

            self._last_position = self.position


class Ripple3D(Grid3DAction):
    __doc__ = 'Simulates a ripple (radial wave) effect.\n    The amplitude of the wave will decrease when it goes away from the center of the ripple.\n    It modifies the z-coordinate while the x and y remains unmodified.\n\n    Example::\n\n       scene.do(Ripple3D(center=(320,240), radius=240, waves=15, amplitude=60, duration=20, grid=(32,24)))\n    '

    def init(self, center=(-1, -1), radius=240, waves=15, amplitude=60, *args, **kw):
        """
        :Parameters:
            `center` : (int,int)
                Center of the ripple. Default: (win_size_width /2, win_size_height /2)
            `radius` : int
                Radius of the ripple. Default: 240
            `waves` : int
                Number of waves (2 * pi) that the action will perform. Default: 15
            `amplitude` : int
                Wave amplitude (height). Default is 60
        """
        (super(Ripple3D, self).init)(*args, **kw)
        x, y = director.get_window_size()
        if center == (-1, -1):
            center = (
             x // 2, y // 2)
        self.position = Point2(center[0] + 1, center[1] + 1)
        self.radius = radius
        self.waves = waves
        self.amplitude_rate = 1.0
        self.amplitude = amplitude

    def update(self, t):
        for i in range(0, self.grid.x + 1):
            for j in range(0, self.grid.y + 1):
                x, y, z = self.get_original_vertex(i, j)
                p = Point2(x, y)
                vect = self.position - p
                r = abs(vect)
                if r < self.radius:
                    r = self.radius - r
                    rate = pow(r / self.radius, 2)
                    z += math.sin(t * math.pi * self.waves * 2 + r * 0.1) * self.amplitude * self.amplitude_rate * rate
                self.set_vertex(i, j, (x, y, z))


class Shaky3D(Grid3DAction):
    __doc__ = 'Shaky simulates an earthquake by modifying randomly the x, y and z coordinates of each vertex.\n\n    Example::\n\n       scene.do(Shaky3D(randrange=6, grid=(4,4), duration=10))\n    '

    def init(self, randrange=6, *args, **kw):
        """
        :Parameters:
            `randrange` : int
                Number that will be used in random.randrange(-randrange, randrange) to do the effect
        """
        (super(Shaky3D, self).init)(*args, **kw)
        self.randrange = randrange

    def update(self, t):
        for i in range(0, self.grid.x + 1):
            for j in range(0, self.grid.y + 1):
                x, y, z = self.get_original_vertex(i, j)
                x += rr(-self.randrange, self.randrange + 1)
                y += rr(-self.randrange, self.randrange + 1)
                z += rr(-self.randrange, self.randrange + 1)
                self.set_vertex(i, j, (x, y, z))


class Liquid(Grid3DAction):
    __doc__ = 'Simulates a liquid effect using the math.sin() function modifying the x and y coordinates.\n    The z coordinate remains unmodified.\n\n    Example::\n\n       scene.do(Liquid(waves=5, amplitude=40, grid=(16,16), duration=10))\n    '

    def init(self, waves=4, amplitude=20, *args, **kw):
        """
        :Parameters:
            `waves` : int
                Number of waves (2 * pi) that the action will perform. Default is 4
            `amplitude` : int
                Wave amplitude (height). Default is 20
        """
        (super(Liquid, self).init)(*args, **kw)
        self.waves = waves
        self.amplitude = amplitude
        self.amplitude_rate = 1.0

    def update(self, t):
        for i in range(1, self.grid.x):
            for j in range(1, self.grid.y):
                x, y, z = self.get_original_vertex(i, j)
                xpos = x + math.sin(t * math.pi * self.waves * 2 + x * 0.01) * self.amplitude * self.amplitude_rate
                ypos = y + math.sin(t * math.pi * self.waves * 2 + y * 0.01) * self.amplitude * self.amplitude_rate
                self.set_vertex(i, j, (xpos, ypos, z))


class Waves(Grid3DAction):
    __doc__ = 'Simulates waves using the math.sin() function both in the vertical and horizontal axis.\n    The z coordinate is not modified.\n\n    Example::\n\n        scene.do(Waves(waves=4, amplitude=20, hsin=False, vsin=True, grid=(16,16), duration=10))\n    '

    def init(self, waves=4, amplitude=20, hsin=True, vsin=True, *args, **kw):
        """Initializes the Waves actions

        :Parameters:
            `waves` : int
                Number of waves (2 * pi) that the action will perform. Default is 4
            `amplitude` : int
                Wave amplitude (height). Default is 20
            `hsin` : bool
                whether or not in will perform horizontal waves. Default is True
            `vsin` : bool
                whether or not in will perform vertical waves. Default is True
        """
        (super(Waves, self).init)(*args, **kw)
        self.hsin = hsin
        self.vsin = vsin
        self.waves = waves
        self.amplitude = amplitude
        self.amplitude_rate = 1.0

    def update(self, t):
        for i in range(0, self.grid.x + 1):
            for j in range(0, self.grid.y + 1):
                x, y, z = self.get_original_vertex(i, j)
                if self.vsin:
                    xpos = x + math.sin(t * math.pi * self.waves * 2 + y * 0.01) * self.amplitude * self.amplitude_rate
                else:
                    xpos = x
                if self.hsin:
                    ypos = y + math.sin(t * math.pi * self.waves * 2 + x * 0.01) * self.amplitude * self.amplitude_rate
                else:
                    ypos = y
                self.set_vertex(i, j, (xpos, ypos, z))


class Twirl(Grid3DAction):
    __doc__ = 'Simulates a twirl effect modifying the x and y coordinates.\n    The z coordinate is not modified.\n\n    Example::\n\n       scene.do(Twirl(center=(320,240), twirls=5, amplitude=1, grid=(16,12), duration=10))\n    '

    def init(self, center=(-1, -1), twirls=4, amplitude=1, *args, **kw):
        """
        :Parameters:
            `twirls` : int
                Number of twirls (2 * pi) that the action will perform. Default is 4
            `amplitude` : flaot
                Twirl amplitude. Default is 1
            `center` : (int,int)
                Center of the twirl in x,y coordinates. Default: center of the screen
        """
        (super(Twirl, self).init)(*args, **kw)
        x, y = director.get_window_size()
        if center == (-1, -1):
            center = (
             x // 2, y // 2)
        self.position = Point2(center[0] + 1, center[1] + 1)
        self.twirls = twirls
        self.amplitude = amplitude
        self.amplitude_rate = 1.0

    def update(self, t):
        cx = self.position.x
        cy = self.position.y
        for i in range(0, self.grid.x + 1):
            for j in range(0, self.grid.y + 1):
                x, y, z = self.get_original_vertex(i, j)
                r = math.sqrt((i - self.grid.x / 2.0) ** 2 + (j - self.grid.y / 2.0) ** 2)
                amplitude = 0.1 * self.amplitude * self.amplitude_rate
                a = r * math.cos(math.pi / 2.0 + t * math.pi * self.twirls * 2) * amplitude
                dx = math.sin(a) * (y - cy) + math.cos(a) * (x - cx)
                dy = math.cos(a) * (y - cy) - math.sin(a) * (x - cx)
                self.set_vertex(i, j, (cx + dx, cy + dy, z))