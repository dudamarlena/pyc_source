# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\demos\follow.py
# Compiled at: 2005-12-18 22:36:37
"""
A sample of swarming behavior, with a pedestrian interface to move the 
camera around the scene.
"""
import math, sys, atexit, random, pygame, OpenGL.GL as ogl, OpenGL.GLU as oglu
sys.path.append('..')
import la, spyre, zoe_objects as zoeobj
pygame.init()
PARTICLES = 25

class ChaseParticle(zoeobj.NewtonianParticle):
    """The chase particle is one that the swarming particles follow."""
    __module__ = __name__
    OMEGA = 0.01 * la.Vector.K
    particleColor = (
     1.0, 1.0, 0.0)
    trailColor = (0.5, 0.5, 0.0)
    trailLength = 100

    def update(self):
        r = la.Vector(*self.pos)
        self.vel = self.OMEGA.cross(r)
        zoeobj.NewtonianParticle.update(self)


class SwarmParticle(zoeobj.NewtonianParticle):
    """The swarm particle is mainstay of the simulation.  If the swarm
    particle is within a certain distance of the chase particle, it
    will attempt to match its velocity.  If not, it will alter its
    velocity to approach the chase particle.  Both the acceleration
    and speed of the particle is bounded above, and a random nudging
    effect is applied to result in a random element."""
    __module__ = __name__
    THRESHHOLD_SQUARED = 1.0 ** 2
    MAX_DELTAVEE = 0.01
    MAX_SPEED = 0.05
    EPSILON = 0.02
    Chase = None
    trailLength = 10

    def update(self):
        s = la.Vector(*SwarmParticle.Chase.pos)
        r = la.Vector(*self.pos)
        if (s - r).normSquared() > self.THRESHHOLD_SQUARED:
            ideal = s - r
        else:
            ideal = la.Vector(*SwarmParticle.Chase.vel)
        deltavee = (ideal - la.Vector(*self.vel)).bound(self.MAX_DELTAVEE)
        if self.EPSILON > 0.0:
            nudge = la.Vector(random.uniform(-self.EPSILON, self.EPSILON), random.uniform(-self.EPSILON, self.EPSILON), random.uniform(-self.EPSILON, self.EPSILON))
            deltavee += nudge
        self.impulse(deltavee)
        self.vel = la.Vector(*self.vel).bound(self.MAX_SPEED)
        zoeobj.NewtonianParticle.update(self)


class SwarmSystem(zoeobj.System):
    """Manage the particles.  Create new ones within a certain range
    of the origid, and within a certain angle of the x-y plane."""
    __module__ = __name__
    RHO_MAX = 10.0
    PHI_MAX = -spyre.pi / 12

    def new(self):
        rho = random.uniform(0.0, self.RHO_MAX)
        theta = random.uniform(0, spyre.twoPi)
        phi = random.uniform(-self.PHI_MAX, self.PHI_MAX)
        return SwarmParticle(la.PolarVector(rho, theta, phi), la.Vector.ZERO)


def main():
    engine = spyre.Engine()
    engine.camera = spyre.RovingCameraOrtho(engine, (2, 5, 2), (0, 0, 1.5))
    engine.camera.zoomIn()
    engine.interface = spyre.PedestrianInterface(engine)
    engine.studio = spyre.StudioColorMat(engine)
    engine.studio.lightsOut()
    engine.studio.depthCueing(True, ogl.GL_LINEAR, 0, 5, 20)
    engine.add(zoeobj.AxesObject())
    engine.add(zoeobj.GridObject())
    chase = ChaseParticle(la.Vector(3.0, 0.0, 0.0))
    engine.add(chase)
    SwarmParticle.Chase = chase
    engine.add(SwarmSystem(PARTICLES))
    engine.add(zoeobj.FrameRateCounter(engine))
    engine.go()


if __name__ == '__main__':
    main()