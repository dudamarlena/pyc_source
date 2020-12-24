# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/OpenGL/SkyGrassBackground.py
# Compiled at: 2008-10-19 12:19:52
"""======================
Sky & Grass background
======================

A very simple component showing a plane with the upper half coloured light blue and the lower half green. Can be used for a background.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

Example Usage
-------------
Only a background::

    SkyGrassBackground(size=(5000,5000,0), position=(0,0,-100)).activate()
    Axon.Scheduler.scheduler.run.runThreads()

"""
import Axon, pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGLComponent import *

class SkyGrassBackground(OpenGLComponent):
    """    SkyGrassBackground(...) -> A new SkyGrassBackground component.
    
    A very simple component showing a plane with the upper half coloured
    light blue and the lower half green. Can be used for a background.
    """

    def setup(self):
        self.w = self.size.x / 2.0
        self.h = self.size.y / 2.0

    def draw(self):
        glBegin(GL_QUADS)
        glColor4f(0.85, 0.85, 1.0, 1.0)
        glVertex3f(-self.w, self.h, 0)
        glVertex3f(self.w, self.h, 0)
        glVertex3f(self.w, 0.0, 0)
        glVertex3f(-self.w, 0.0, 0)
        glColor4f(0.75, 1.0, 0.75, 1.0)
        glVertex3f(-self.w, 0.0, 0)
        glVertex3f(self.w, 0.0, 0)
        glVertex3f(self.w, -self.h, 0)
        glVertex3f(-self.w, -self.h, 0)
        glEnd()


__kamaelia_components__ = (
 SkyGrassBackground,)
if __name__ == '__main__':
    SkyGrassBackground(size=(5000, 5000, 0), position=(0, 0, -100)).activate()
    Axon.Scheduler.scheduler.run.runThreads()