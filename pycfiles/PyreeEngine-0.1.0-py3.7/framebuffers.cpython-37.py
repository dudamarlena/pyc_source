# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/framebuffers.py
# Compiled at: 2018-12-10 16:07:25
# Size of source mod 2**32: 2773 bytes
"""Framebuffer classes"""
from OpenGL.GL import *
from PyreeEngine.util import Resolution
from PyreeEngine.basicObjects import FSQuad
from PyreeEngine.shaders import FullscreenTexture
from PyreeEngine.camera import Camera

class Framebuffer:

    def __init__(self):
        self.fbo = None

    def bindFramebuffer(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)


class DefaultFramebuffer:
    __doc__ = 'Default OpenGL framebuffer object required for rendering to screen'

    def __init__(self):
        self.fbo = 0

    def bindFramebuffer(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)


class RegularFramebuffer(Framebuffer):
    __doc__ = 'Framebuffer with 2d Texture and depth attachment'
    fsquad = None
    fsquad: FSQuad
    fstextureshader = None
    fstextureshader: FullscreenTexture
    fscamera = None
    fscamera: Camera

    def __init__(self, resolution):
        super(RegularFramebuffer, self).__init__()
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, resolution.width, resolution.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture, 0)
        self.depthBuf = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depthBuf)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, resolution.width, resolution.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depthBuf)
        self.initrendertoscreen()

    def __del__(self):
        glDeleteFramebuffers([self.fbo])
        glDeleteTextures([self.texture])

    def initrendertoscreen(self):
        """Sets up the objects required to render framebuffer contents to default framebuffer"""
        if RegularFramebuffer.fsquad is None:
            RegularFramebuffer.fsquad = FSQuad()
        if RegularFramebuffer.fstextureshader is None:
            RegularFramebuffer.fstextureshader = FullscreenTexture()
            RegularFramebuffer.fsquad.shader = RegularFramebuffer.fstextureshader
        if RegularFramebuffer.fscamera is None:
            RegularFramebuffer.fscamera = Camera()

    def rendertoscreen(self):
        """Renders the framebuffer to default framebuffer (Aka the screen)"""
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        RegularFramebuffer.fsquad.textures = [self.texture]
        RegularFramebuffer.fsquad.render(RegularFramebuffer.fscamera.viewMatrix)