# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cube\display.py
# Compiled at: 2007-04-06 01:30:31
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from pygame.locals import *

def screenshot(width, height, filename=None):
    """Take a screen shot and save it to the given filename."""
    try:
        import Image
    except:
        print 'Screenshot capability requires the Python Image Library (PIL).'
        return

    data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    img = Image.fromstring('RGB', (width, height), data)
    if filename:
        img.save(filename)


def init():
    """Initialize the graphics framework.  This starts up pygame and creates the
    main window."""
    pygame.init()
    pygame.key.set_repeat(500, 30)
    pygame.display.set_caption('Cube Graphics')


def initviewport(left, top, width, height, linewidth, pointsize):
    """Initialize the OpenGL context with the given settings."""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(left, top, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width - left) / float(height - top), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glLineWidth(float(linewidth))
    glPointSize(pointsize)


def resize(width, height, fullscreen, linewidth, pointsize):
    """Resize the viewport to the given size and configure the new viewport with the given width, height, linewidth, and pointsize and use fullscreen mode according to the fullscreen parameter."""
    res = pygame.display.get_surface()
    if res is not None:
        mode = res.get_flags()
        if bool(mode & pygame.FULLSCREEN) ^ fullscreen:
            caption = pygame.display.get_caption()
            if mode & pygame.FULLSCREEN:
                pygame.display.set_mode((width, height), mode ^ pygame.OPENGL)
            pygame.display.quit()
            pygame.display.init()
            if mode & pygame.FULLSCREEN:
                pygame.display.set_mode((width, height), mode ^ pygame.OPENGL ^ pygame.FULLSCREEN)
            pygame.display.set_caption(*caption)
    else:
        mode = OPENGL | DOUBLEBUF
    if fullscreen:
        mode = mode | pygame.FULLSCREEN
        if mode & pygame.RESIZABLE:
            mode = mode ^ pygame.RESIZABLE
    else:
        if mode & pygame.FULLSCREEN:
            mode = mode ^ pygame.FULLSCREEN
        mode = mode | pygame.RESIZABLE
    res = pygame.display.set_mode((width, height), mode)
    (left, top, twidth, theight) = res.get_rect()
    pygame.key.set_mods(0)
    initviewport(left, top, twidth, theight, linewidth, pointsize)
    if fullscreen:
        pygame.mouse.set_visible(0)
    else:
        pygame.mouse.set_visible(1)
    return


def updatelinewidth(linewidth):
    """Sets the opengl line width."""
    glLineWidth(float(linewidth))


def updatepointsize(pointsize):
    """Sets the opengl point size."""
    glPointSize(float(pointsize))


def toggle_fullscreen():
    """Toggles fullscreen mode, saving state and rebuilding the context as
    necessary.  Returns the screen resolution as a tuple."""
    if pygame.display.get_init():
        screen = pygame.display.get_surface()
        caption = pygame.display.get_caption()
        w, h = screen.get_width(), screen.get_height()
        flags = screen.get_flags()
        bits = screen.get_bitsize()
        pygame.display.quit()
    pygame.display.init()
    screen = pygame.display.set_mode((w, h), flags ^ FULLSCREEN, bits)
    pygame.display.set_caption(*caption)
    pygame.key.set_mods(0)
    return screen


def clear():
    """Clears the display.  This can be used before rendering each frame."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def flip():
    """Flips the display when in double-buffer mode.  This can be used after
    rendering a frame in order to show it on the screen."""
    pygame.display.flip()