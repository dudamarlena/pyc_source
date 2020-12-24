# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/OpenGL/Label.py
# Compiled at: 2008-10-19 12:19:52
"""===================
OpenGL Label Widget
===================

A Label widget for the OpenGL display service.

This component is a subclass of OpenGLComponent and therefore uses the
OpenGL display service.

Example Usage
-------------
4 Labels with various sizes, colours, captions and positions::

    Graphline(
        Label1 = Label(caption="That", size=(2,2,1), sidecolour=(0,200,0), position=(-3,0,-10)),
        Label2 = Label(caption="Boy", bgcolour=(200,100,0), position=(3,0,-10)),
        Label3 = Label(caption="Needs", margin=15, position=(-1,0,-10), rotation=(30,0,10)),
        Label4 = Label(caption="Therapy!", fontsize=20, size=(0.3,0.3,1), position=(1,0,-10)),
        ECHO = ConsoleEchoer(),
        linkages = {
            ("Label1", "outbox") : ("ECHO", "inbox"),
            ("Label2", "outbox") : ("ECHO", "inbox"),
            ("Label3", "outbox") : ("ECHO", "inbox"),
            ("Label4", "outbox") : ("ECHO", "inbox"),            
        }
    ).run()
    
How does it work?
-----------------
This component is a subclass of OpenGLComponent. It overrides
__init__(), setup(), draw(), handleEvents() and frame().

In setup() only buildCaption() gets called where the set caption is
rendered on a pygame surface. This surface is then set as OpenGL
texture.

In draw() a flat cuboid is drawn (if size is not specified) with the
caption texture on both the front and the back surface.

"""
import Axon, pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Vector import Vector
from OpenGLComponent import *
from math import *

class Label(OpenGLComponent):
    """
    Label(...) -> A new Label component.
    
    A Label widget for the OpenGL display service.

    Keyword arguments:
    
    - caption      -- Label caption (default="Label")
    - bgcolour     -- Colour of surfaces behind caption (default=(200,200,200))
    - fgcolour     -- Colour of the caption text (default=(0,0,0)
    - sidecolour   -- Colour of side planes (default=(200,200,244))
    - margin       -- Margin size in pixels (default=8)
    - fontsize     -- Font size for caption text (default=50)
    - pixelscaling -- Factor to convert pixels to units in 3d, ignored if size is specified (default=100)
    - thickness    -- Thickness of Label widget, ignored if size is specified (default=0.3)
        
    """

    def __init__(self, **argd):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(Label, self).__init__(**argd)
        self.caption = argd.get('caption', 'Label')
        self.backgroundColour = argd.get('bgcolour', (200, 200, 244))
        self.foregroundColour = argd.get('fgcolour', (0, 0, 0))
        self.sideColour = argd.get('sidecolour', (244, 244, 244))
        self.margin = argd.get('margin', 8)
        self.fontsize = argd.get('fontsize', 50)
        self.pixelscaling = argd.get('pixelscaling', 100)
        self.thickness = argd.get('thickness', 0.3)

    def setup(self):
        """ Build caption."""
        self.buildCaption()

    def draw(self):
        """ Draw label cuboid."""
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
        glEnd()
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        glBegin(GL_QUADS)
        glTexCoord2f(self.tex_w, 1.0 - self.tex_h)
        glVertex3f(hs.x, hs.y, -hs.z)
        glTexCoord2f(0.0, 1.0 - self.tex_h)
        glVertex3f(-hs.x, hs.y, -hs.z)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-hs.x, -hs.y, -hs.z)
        glTexCoord2f(self.tex_w, 1.0)
        glVertex3f(hs.x, -hs.y, -hs.z)
        glTexCoord2f(0.0, 1.0 - self.tex_h)
        glVertex3f(-hs.x, -hs.y, hs.z)
        glTexCoord2f(self.tex_w, 1.0 - self.tex_h)
        glVertex3f(hs.x, -hs.y, hs.z)
        glTexCoord2f(self.tex_w, 1.0)
        glVertex3f(hs.x, hs.y, hs.z)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-hs.x, hs.y, hs.z)
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def buildCaption(self):
        """Pre-render the text to go on the label."""
        pygame.font.init()
        font = pygame.font.Font(None, self.fontsize)
        self.image = font.render(self.caption, True, self.foregroundColour)
        if self.size != Vector(0, 0, 0):
            texsize = (
             self.size.x * self.pixelscaling, self.size.y * self.pixelscaling)
        else:
            texsize = (
             self.image.get_width() + 2 * self.margin, self.image.get_height() + 2 * self.margin)
            self.size = Vector(texsize[0] / float(self.pixelscaling), texsize[1] / float(self.pixelscaling), self.thickness)
        pow2size = (
         int(2 ** ceil(log(texsize[0] + 2 * self.margin, 2))), int(2 ** ceil(log(texsize[1] + 2 * self.margin, 2))))
        textureSurface = pygame.Surface(pow2size)
        textureSurface.fill(self.backgroundColour)
        self.tex_w = float(texsize[0]) / pow2size[0]
        self.tex_h = float(texsize[1]) / pow2size[1]
        dest = (
         max((texsize[0] - self.image.get_width()) / 2, 0), max((texsize[1] - self.image.get_height()) / 2, 0))
        textureSurface.blit(self.image, dest)
        textureSurface = textureSurface.convert_alpha()
        textureData = pygame.image.tostring(textureSurface, 'RGBX', 1)
        self.texID = glGenTextures(1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureSurface.get_width(), textureSurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glDisable(GL_TEXTURE_2D)
        return


__kamaelia_components__ = (
 Label,)
if __name__ == '__main__':
    from Kamaelia.Util.Console import ConsoleEchoer
    from Kamaelia.Chassis.Graphline import Graphline
    Graphline(Label1=Label(caption='That', size=(2, 2, 1), sidecolour=(0, 200, 0), position=(-3,
                                                                                             0,
                                                                                             -10)), Label2=Label(caption='Boy', bgcolour=(200,
                                                                                                                                          100,
                                                                                                                                          0), position=(3,
                                                                                                                                                        0,
                                                                                                                                                        -10)), Label3=Label(caption='Needs', margin=15, position=(-1,
                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                  -10), rotation=(30,
                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                  10)), Label4=Label(caption='Therapy!', fontsize=20, size=(1.3,
                                                                                                                                                                                                                                                                                            0.3,
                                                                                                                                                                                                                                                                                            1), position=(1,
                                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                                          -10)), ECHO=ConsoleEchoer(), linkages={('Label1', 'outbox'): ('ECHO', 'inbox'), 
       ('Label2', 'outbox'): ('ECHO', 'inbox'), 
       ('Label3', 'outbox'): ('ECHO', 'inbox'), 
       ('Label4', 'outbox'): ('ECHO', 'inbox')}).run()