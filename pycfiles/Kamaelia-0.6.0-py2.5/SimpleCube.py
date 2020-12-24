# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/OpenGL/SimpleCube.py
# Compiled at: 2008-10-19 12:19:52
"""=====================
Simple Cube component
=====================

A simple cube for the OpenGL display service.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

Example Usage
-------------
Three cubes in different positions with various rotation and sizes::

    Graphline(    
        CUBEC = SimpleCube(position=(0, 0,-12), rotation=(40,90,0), size=(1,1,1)).activate(),
        CUBER = SimpleCube(position=(4,0,-22), size=(2,2,2)).activate(),
        CUBEB = SimpleCube(position=(0,-4,-18), rotation=(0,180,20), size=(1,3,2)).activate(),
        linkages = {}
    ).run()

How does it work?
-----------------
SimpleButton is a subclass of OpenGLComponent (for OpenGLComponent
functionality see its documentation). It overrides draw().

In draw() a simple cube made of 6 quads with different colours is drawn.

"""
import Axon, pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Vector import Vector
from OpenGLComponent import *

class SimpleCube(OpenGLComponent):
    """    SimpleCube(...) -> new SimpleCube component.
    
    A simple cube for the OpenGL display service.
    """

    def draw(self):
        hs = self.size / 2.0
        glBegin(GL_QUADS)
        glColor4f(1.0, 0.75, 0.75, 0.5)
        glVertex3f(hs.x, hs.y, hs.z)
        glVertex3f(hs.x, -hs.y, hs.z)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glVertex3f(hs.x, hs.y, -hs.z)
        glColor4f(0.75, 1.0, 0.75, 0.5)
        glVertex3f(-hs.x, hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glVertex3f(-hs.x, hs.y, -hs.z)
        glColor4f(0.75, 0.75, 1.0, 0.5)
        glVertex3f(hs.x, hs.y, hs.z)
        glVertex3f(-hs.x, hs.y, hs.z)
        glVertex3f(-hs.x, hs.y, -hs.z)
        glVertex3f(hs.x, hs.y, -hs.z)
        glColor4f(1.0, 0.75, 1.0, 0.5)
        glVertex3f(hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glColor4f(0.75, 1.0, 1.0, 0.5)
        glVertex3f(hs.x, hs.y, -hs.z)
        glVertex3f(-hs.x, hs.y, -hs.z)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glColor4f(1.0, 1.0, 0.75, 0.5)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glVertex3f(hs.x, -hs.y, hs.z)
        glVertex3f(hs.x, hs.y, hs.z)
        glVertex3f(-hs.x, hs.y, hs.z)
        glEnd()


__kamaelia_components__ = (
 SimpleCube,)
if __name__ == '__main__':
    from Kamaelia.Util.Graphline import Graphline
    Graphline(CUBEC=SimpleCube(position=(0, 0, -12), rotation=(225, 45, 135), size=(1,
                                                                                    1,
                                                                                    1)).activate(), CUBER=SimpleCube(position=(4,
                                                                                                                               0,
                                                                                                                               -22), size=(2,
                                                                                                                                           2,
                                                                                                                                           2)).activate(), CUBEB=SimpleCube(position=(0,
                                                                                                                                                                                      -4,
                                                                                                                                                                                      -18), rotation=(0,
                                                                                                                                                                                                      180,
                                                                                                                                                                                                      20), size=(1,
                                                                                                                                                                                                                 3,
                                                                                                                                                                                                                 2)).activate(), linkages={}).run()