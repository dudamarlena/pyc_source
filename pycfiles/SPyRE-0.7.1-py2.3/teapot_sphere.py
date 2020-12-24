# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\demos\teapot_sphere.py
# Compiled at: 2006-02-18 18:29:49
"""
A teapot and a sphere, demos lighting/shading peculiarity
"""
import math, atexit, sys, pygame
from pygame.locals import *
from pygame import display
import OpenGL.GL as ogl, OpenGL.GLU as oglu
sys.path.append('..')
import spyre, zoe_objects as zoe
from shapes_objects import *

class Sphere(spyre.Object):
    """draws a sphere """
    __module__ = __name__

    def __init__(self, radius, x=0, y=0, z=0):
        spyre.Object.__init__(self)
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.quad = oglu.gluNewQuadric()

    def display(self):
        ogl.glColor4f(0.7, 0.7, 0.7, 1)
        ogl.glPushMatrix()
        ogl.glTranslate(self.x, self.y, self.z)
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_AMBIENT, [0.2, 0.0, 0.1, 0.0])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_DIFFUSE, [0.5, 0.5, 0.5, 0.1])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_SPECULAR, [0.7, 0.6, 0.8, 0.0])
        ogl.glMaterialf(ogl.GL_FRONT, ogl.GL_SHININESS, 50)
        oglu.gluSphere(self.quad, self.radius, 60, 60)
        ogl.glPopMatrix()


class Teapot(spyre.Object):
    """ wrapper that adds color to Teapot obj """
    __module__ = __name__

    def __init__(self, size):
        spyre.Object.__init__(self)
        self.size = size
        self.geo = shapeTeapot(size)

    def display(self):
        ogl.glColor4f(1, 1, 1, 1)
        ogl.glPushMatrix()
        self.geo.display()
        ogl.glPopMatrix()


def postMortem(engine):
    """ displays frame rate to stderr at end of run """
    print >> sys.stderr, 'frame %d rate %.2f' % (spyre.Object.runTurn, engine.runTimer.frameRate)


def main():
    pygame.init()
    engine = spyre.Engine()
    engine.studio = spyre.StudioColorMat(engine)
    engine.studio.depthCueing(True, ogl.GL_LINEAR, None, 2, 10)
    light0 = spyre.Bulb([0.5, 0.6, 0.5, 1.0], [
     0.6, 0.7, 0.7, 1.0], [
     0.3, 0.3, 0.3, 1.0])
    engine.studio.addFixedLight(light0, (0, 5, 10))
    engine.add(zoe.AxesObject())
    engine.add(zoe.GridObject())
    engine.add(Teapot(1))
    engine.add(Sphere(1, 0, 3, 0))
    engine.add(zoe.FrameRateCounter(engine))
    atexit.register(postMortem, engine)
    engine.go()
    return


if __name__ == '__main__':
    main()