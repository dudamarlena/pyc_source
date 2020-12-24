# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\demos\fountain.py
# Compiled at: 2005-12-14 21:43:43
"""
A sample of a fountain effect.
"""
import random, sys, pygame
sys.path.append('..')
import la, spyre, zoe_objects as zoeobj
pygame.init()
PARTICLES = 100

class FountainParticle(zoeobj.NewtonianParticle):
    """Each particle is pulled down by a gravitational force, and is
    reset when it hits the x-y plane."""
    __module__ = __name__
    G = -0.002 * la.Vector.K
    Z_MIN = 0.0
    trailLength = 5

    def update(self):
        self.impulse(self.G)
        zoeobj.NewtonianParticle.update(self)

    def ok(self):
        return self.pos[2] >= self.Z_MIN


class FountainSystem(zoeobj.System):
    """Manage the fountain particles, creating them at the origin with some
    random upward velocity."""
    __module__ = __name__
    V0_MAX = 0.1

    def new(self):
        theta = random.uniform(0, spyre.twoPi)
        phi = random.uniform(0, spyre.pi)
        vel = la.PolarVector(self.V0_MAX, theta, phi)
        return FountainParticle(la.Vector.ZERO, vel)


def main():
    engine = spyre.Engine()
    engine.add(zoeobj.AxesObject())
    engine.add(zoeobj.GridObject())
    engine.add(FountainSystem(PARTICLES))
    engine.add(zoeobj.FrameRateCounter(engine))
    engine.go()


if __name__ == '__main__':
    main()