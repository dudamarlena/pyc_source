# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\demos\dumbbell_mv_stereo_ed.py
# Compiled at: 2006-02-18 18:33:26
"""
Draws a dumbbell, (two spheres and a connecting cylinder) fixed in space, 
but with an orbiting light source.

@undocumented gl.*
@exclude gl.*
"""
import math, sys, atexit, stereoscopic, pygame, OpenGL.GL as ogl, OpenGL.GLU as oglu
sys.path.append('..')
import spyre, zoe_objects as zoeobj

class DumbBell(spyre.Object):
    """draws a dumbbell object """
    __module__ = __name__

    def __init__(self, height, radius, x=0, y=0, z=0):
        spyre.Object.__init__(self)
        self.height = height
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.quad = oglu.gluNewQuadric()

    def display(self):
        ogl.glColor4f(0.5, 0.5, 0.5, 1)
        ogl.glPushMatrix()
        ogl.glTranslate(self.x, self.y, self.z - self.height / 2.0)
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_AMBIENT, [0.1745, 0.0, 0.1, 0.0])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_DIFFUSE, [0.5, 0.5, 0.5, 0.1])
        ogl.glMaterialfv(ogl.GL_FRONT, ogl.GL_SPECULAR, [0.7, 0.6, 0.8, 0.0])
        ogl.glMaterialf(ogl.GL_FRONT, ogl.GL_SHININESS, 50)
        oglu.gluCylinder(self.quad, self.radius / 2.0, self.radius / 2.0, self.height, 60, 70)
        ogl.glTranslate(0, 0, self.height + self.radius / 2.0)
        oglu.gluSphere(self.quad, self.radius, 60, 60)
        ogl.glTranslate(0, 0, -self.height - self.radius)
        oglu.gluSphere(self.quad, self.radius, 60, 60)
        ogl.glPopMatrix()


def postMortem(engine):
    """ displays frame rate to stderr at end of run """
    print >> sys.stderr, 'frame %d rate %.2f' % (spyre.Object.runTurn, engine.runTimer.frameRate)


def main():
    """ main block """
    pygame.init()
    eng = spyre.EngineFullScreen()
    (eng.width, eng.height) = (800, 600)
    cam0 = spyre.MobileCameraOrtho(eng, 2.0)
    cam0.ortho(-3, 3, -3, 3, -10, 100)
    cam0.eye = (8, 0, 0)
    cam0.setViewport(0.2, 0.2, 0.8, 0.8)
    eng.addCamera(cam0)
    cam1 = spyre.MobileCameraOrtho(eng, 5.0)
    cam1.eye = (1.5, 1.5, 8)
    cam1.setViewport(0, 0, 0.4, 0.4)
    cam1.background = None
    eng.addCamera(cam1)
    cam2 = spyre.MobileCameraOrtho(eng, 5.0)
    cam2.eye = (-1.5, -1.5, -8)
    cam2.setViewport(0.6, 0.6, 1, 1)
    cam2.background = None
    eng.addCamera(cam2)
    eng.studio = spyre.StudioColorMat(eng)
    engine = stereoscopic.StereoEngineED(eng)
    light0 = spyre.Bulb([0.5, 0.6, 0.5, 1.0], [
     0.6, 0.7, 0.7, 1.0], [
     0.3, 0.3, 0.3, 1.0])
    orbiter = zoeobj.RotatingGroup(0.03, objects=[light0], ray=(1, 0, 0))
    engine.studio.addMobileLight(light0, orbiter, (0, 10, 10))
    engine.add(zoeobj.AxesObject())
    engine.add(zoeobj.GridObject())
    engine.add(DumbBell(2, 1))
    atexit.register(postMortem, engine)
    engine.go()
    return


if __name__ == '__main__':
    main()