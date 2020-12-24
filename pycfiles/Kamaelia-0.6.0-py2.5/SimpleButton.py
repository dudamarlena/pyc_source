# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/OpenGL/SimpleButton.py
# Compiled at: 2008-10-19 12:19:52
"""=======================
Simple Button component
=======================

A simple cuboid shaped button without caption. Implements responsive
button behavoir.

Could be used to subclass differently shaped buttons from. The colours
of the front/back and the side faces can be specified.

Example Usage
-------------
Two simple buttons which send messages to the console::

    Graphline(
        button1 = SimpleButton(size=(1,1,0.3), position=(-2,0,-10), msg="PINKY"),
        button2 = SimpleButton(size=(2,2,1), position=(5,0,-15), msg="BRAIN"),
        echo = ConsoleEchoer(),
        linkages = {
            ("button1", "outbox") : ("echo", "inbox"),
            ("button2", "outbox") : ("echo", "inbox")
        }
    ).run()
        

How does it work?
-----------------
This component is a subclass of OpenGLComponent (for OpenGLComponent
functionality see its documentation). It overrides __init__(), setup(),
draw() and handleEvents().

It draws a simple cuboid. It is activated on mouse button release over
the object and on key down if a key is assigned. On mouse button down it
is shrunk by a small amount until the button is released.

"""
import Axon, pygame
from pygame.locals import *
from OpenGL.GL import *
from Vector import Vector
from OpenGLComponent import OpenGLComponent

class SimpleButton(OpenGLComponent):
    """    SimpleButton(...) -> A new SimpleButton component.
    
    A simple cuboid shaped button without caption. Implements responsive
    button behavoir.

    Keyword arguments:
    
    - bgcolour      -- Background colour (default=(244,244,244))
    - sidecolour    -- Colour of side planes (default=(200,200,244))
    - key           -- Activation key, pygame identifier (optional)
    - msg           -- Message that gets sent to the outbox when the button is activated (default="CLICK")
    """

    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(SimpleButton, self).__init__(**argd)
        self.backgroundColour = argd.get('bgcolour', (244, 244, 244))
        self.sideColour = argd.get('sidecolour', (200, 200, 244))
        self.key = argd.get('key', None)
        self.eventMsg = argd.get('msg', 'CLICK')
        self.size = Vector(*argd.get('size', (1, 1, 1)))
        self.grabbed = 0
        return

    def setup(self):
        self.addListenEvents([pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN])

    def draw(self):
        hs = self.size / 2.0
        glBegin(GL_QUADS)
        glColor4f(self.sideColour[0] / 256.0, self.sideColour[1] / 256.0, self.sideColour[2] / 256.0, 0.5)
        glVertex3f(hs.x, hs.y, hs.z)
        glVertex3f(hs.x, -hs.y, hs.z)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glVertex3f(hs.x, hs.y, -hs.z)
        glVertex3f(-hs.x, hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glVertex3f(-hs.x, hs.y, -hs.z)
        glVertex3f(hs.x, hs.y, hs.z)
        glVertex3f(-hs.x, hs.y, hs.z)
        glVertex3f(-hs.x, hs.y, -hs.z)
        glVertex3f(hs.x, hs.y, -hs.z)
        glVertex3f(hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glColor4f(self.backgroundColour[0] / 256.0, self.backgroundColour[1] / 256.0, self.backgroundColour[2] / 256.0, 0.5)
        glVertex3f(hs.x, hs.y, -hs.z)
        glVertex3f(-hs.x, hs.y, -hs.z)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glVertex3f(hs.x, -hs.y, hs.z)
        glVertex3f(hs.x, hs.y, hs.z)
        glVertex3f(-hs.x, hs.y, hs.z)
        glEnd()

    def handleEvents(self):
        while self.dataReady('events'):
            activate = False
            event = self.recv('events')
            if event.type == pygame.KEYDOWN:
                if event.key == self.key:
                    activate = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.identifier in event.hitobjects:
                        self.grabbed = event.button
                        self.scaling = Vector(0.9, 0.9, 0.9)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.grabbed = 0
                        self.scaling = Vector(1, 1, 1)
                        if self.identifier in event.hitobjects:
                            activate = True
            elif activate:
                self.send(self.eventMsg, 'outbox')


__kamaelia_components__ = (SimpleButton,)
if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    Graphline(button1=SimpleButton(size=(1, 1, 0.3), position=(-2, 0, -10), msg='PINKY'), button2=SimpleButton(size=(2,
                                                                                                                     2,
                                                                                                                     1), position=(5,
                                                                                                                                   0,
                                                                                                                                   -15), msg='BRAIN'), echo=ConsoleEchoer(), linkages={('button1', 'outbox'): ('echo', 'inbox'), 
       ('button2', 'outbox'): ('echo', 'inbox')}).run()