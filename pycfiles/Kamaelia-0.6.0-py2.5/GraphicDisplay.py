# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/UI/GraphicDisplay.py
# Compiled at: 2008-10-19 12:19:52
__kamaelia_components__ = ()
try:
    from Kamaelia.UI.Pygame.Display import PygameDisplay
    have_pygame = True
except ImportError:
    have_pygame = False

try:
    from Kamaelia.UI.OpenGL.Display import OpenGLDisplay
    have_opengl = True
except ImportError:
    have_opengl = False