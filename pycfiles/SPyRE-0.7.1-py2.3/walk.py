# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\demos\walk.py
# Compiled at: 2005-12-14 21:45:53
"""
A sample of a number of particles engaging in a random walk.
"""
import random, sys, pygame
sys.path.append('..')
import la, spyre, zoe_objects as zoeobj
PARTICLES = 100

class WalkParticle(zoeobj.NewtonianParticle):
    """A particle gets successive random nudges applied to its
    velocity.  It is recycled when it wanders too far."""
    __module__ = __name__
    EPSILON = 0.01
    R_MAX_SQUARED = 10.0 ** 2
    trailLength = 10

    def update(self):
        epsilon = la.Vector(random.uniform(-self.EPSILON, self.EPSILON), random.uniform(-self.EPSILON, self.EPSILON), random.uniform(-self.EPSILON, self.EPSILON))
        self.impulse(epsilon)
        zoeobj.NewtonianParticle.update(self)

    def ok(self):
        return la.Vector(*self.pos).normSquared() <= self.R_MAX_SQUARED


class WalkSystem(zoeobj.System):
    """Manage the walk system.  All particles start out at rest, at
    the origin."""
    __module__ = __name__

    def new(self):
        return WalkParticle(la.Vector.ZERO, la.Vector.ZERO)


def main():
    engine = spyre.Engine()
    engine.add(zoeobj.AxesObject())
    engine.add(zoeobj.GridObject())
    engine.add(WalkSystem(100))
    engine.add(zoeobj.FrameRateCounter(engine))
    engine.go()


if __name__ == '__main__':
    main()