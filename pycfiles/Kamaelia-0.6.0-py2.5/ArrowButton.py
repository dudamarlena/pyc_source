# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/OpenGL/ArrowButton.py
# Compiled at: 2008-10-19 12:19:52
"""=============================
Simple Arrow Button component
=============================

A simple arrow shaped button without caption. Implements responsive
button behavoir.

ArrowButton is a subclass of SimpleButton. It only overrides the draw()
method, i.e. it only changes its appearance.

Example Usage
-------------
Two arrow buttons printing to the console::

    Graphline(
        button1 = ArrowButton(size=(1,1,0.3), position=(-2,0,-10), msg="PINKY"),
        button2 = ArrowButton(size=(2,2,1), position=(5,0,-15), rotation=(0,0,90), msg="BRAIN"),
        echo = ConsoleEchoer(),
        linkages = {
            ("button1", "outbox") : ("echo", "inbox"),
            ("button2", "outbox") : ("echo", "inbox")
        }
    ).run()

"""
import Axon, pygame
from pygame.locals import *
from OpenGL.GL import *
from Vector import Vector
from SimpleButton import SimpleButton

class ArrowButton(SimpleButton):
    """    ArrowButton(...) -> A new ArrowButton component.

    A simple arrow shaped button without caption. Implements responsive
    button behavoir.
    """

    def draw(self):
        hs = self.size / 2.0
        glBegin(GL_QUADS)
        glColor4f(self.sideColour[0] / 256.0, self.sideColour[1] / 256.0, self.sideColour[2] / 256.0, 0.5)
        glVertex3f(0, hs.y, hs.z)
        glVertex3f(hs.x, -hs.y, hs.z)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glVertex3f(0, hs.y, -hs.z)
        glVertex3f(0, hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glVertex3f(0, hs.y, -hs.z)
        glVertex3f(hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glEnd()
        glBegin(GL_TRIANGLES)
        glColor4f(self.backgroundColour[0] / 256.0, self.backgroundColour[1] / 256.0, self.backgroundColour[2] / 256.0, 0.5)
        glVertex3f(0, hs.y, -hs.z)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glVertex3f(hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glVertex3f(0, hs.y, hs.z)
        glEnd()


__kamaelia_components__ = (
 ArrowButton,)
if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    Graphline(button1=ArrowButton(size=(1, 1, 0.3), position=(-2, 0, -10), msg='PINKY'), button2=ArrowButton(size=(2,
                                                                                                                   2,
                                                                                                                   1), position=(5,
                                                                                                                                 0,
                                                                                                                                 -15), rotation=(0,
                                                                                                                                                 0,
                                                                                                                                                 90), msg='BRAIN'), echo=ConsoleEchoer(), linkages={('button1', 'outbox'): ('echo', 'inbox'), 
       ('button2', 'outbox'): ('echo', 'inbox')}).run()