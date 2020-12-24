# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\demos\chaos.py
# Compiled at: 2005-12-18 12:52:50
"""
A demonstration of chaos theory (namely sensitivity to initial
conditions) with a Lorenz system.

"""
import sys, pygame
sys.path.append('..')
import spyre, zoe_objects as zoeobj
pygame.init()
PARTICLES = 10

class LorenzParticle(zoeobj.Particle):
    """A Lorenz particle simply moves according to the Lorenz
    differential equations described above.
    """
    __module__ = __name__
    SIGMA = 10.0
    RHO = 28.0
    B = 8.0 / 3.0
    DELTA_T = 0.01
    trailLength = 100

    def __init__(self, start):
        zoeobj.Particle.__init__(self, start)
        self.t = 0.0

    def update(self):
        (x, y, z) = [ 10 * x for x in self.pos ]
        zoeobj.Particle.update(self)
        deltaX = self.SIGMA * (y - x) * self.DELTA_T
        deltaY = (self.RHO * x - y - x * z) * self.DELTA_T
        deltaZ = (-self.B * z + x * y) * self.DELTA_T
        x += deltaX
        y += deltaY
        z += deltaZ
        self.pos = [ 0.1 * x for x in (x, y, z) ]
        self.t += self.DELTA_T


class LorenzGroup(spyre.Group):
    """A Lorenz group creates a collection of particles that all have
    very nearly the same position, differing only by a very small
    amount."""
    __module__ = __name__
    BASE = 0.001
    VARIANCE = 1e-06

    def __init__(self, count):
        spyre.Group.__init__(self)
        for i in range(1, count + 1):
            xyz = self.BASE + i * self.VARIANCE / count
            self.append(LorenzParticle((xyz,) * 3))


def main():
    engine = spyre.Engine()
    engine.setup()
    engine.add(zoeobj.AxesObject(50.0))
    engine.add(LorenzGroup(PARTICLES))
    engine.add(zoeobj.FrameRateCounter(engine))
    engine.go()


if __name__ == '__main__':
    main()