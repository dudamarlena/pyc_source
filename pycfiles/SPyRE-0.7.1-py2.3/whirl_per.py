# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\demos\whirl_per.py
# Compiled at: 2005-12-14 21:46:23
"""
A sample of a whirlpool effect using Newtonian gravity and drag.
uses frustum perspective
"""
import math, random, sys, pygame
sys.path.append('..')
import la, spyre, zoe_objects as zoeobj
pygame.init()
PARTICLES = 100

class WhirlParticle(zoeobj.NewtonianParticle):
    """Whirlpool articles respond to a gravitational influence located
    at the origin, and are effected by a small O(v) drag.  Particles
    that get too close or too far away are recycled."""
    __module__ = __name__
    GM_DELTA_T = 0.001
    R_SQUARED_MIN = 0.2 ** 2
    R_SQUARED_MAX = 5.0 ** 2
    B = 0.001
    trailLength = 10

    def update(self):
        r = la.Vector(*self.pos)
        v = la.Vector(*self.vel)
        deltavee = -self.GM_DELTA_T / r.normSquared() ** 1.5 * r - self.B * v
        self.impulse(deltavee)
        zoeobj.NewtonianParticle.update(self)

    def ok(self):
        normSquared = la.Vector(*self.pos).normSquared()
        return self.R_SQUARED_MIN <= normSquared <= self.R_SQUARED_MAX


class WhirlSystem(zoeobj.System):
    """Manage the particles.  Particles are created with an
    appropriate orbital velocity at a random distance range from the
    origin."""
    __module__ = __name__
    R0_MIN = 1.0
    R0_MAX = 5.0

    def new(self):
        theta = random.uniform(0.0, spyre.twoPi)
        r0 = random.uniform(self.R0_MIN, self.R0_MAX)
        v0 = math.sqrt(WhirlParticle.GM_DELTA_T / r0)
        posUnit = la.PolarVector(1.0, theta, 0.0)
        velUnit = la.Vector.K.cross(posUnit)
        return WhirlParticle(r0 * posUnit, v0 * velUnit)


def main():
    engine = spyre.Engine()
    engine.camera = spyre.MobileCameraFrustum(engine, 5.0)
    engine.add(zoeobj.AxesObject(1.0))
    engine.add(WhirlSystem(PARTICLES))
    engine.add(zoeobj.FrameRateCounter(engine))
    engine.go()


if __name__ == '__main__':
    main()