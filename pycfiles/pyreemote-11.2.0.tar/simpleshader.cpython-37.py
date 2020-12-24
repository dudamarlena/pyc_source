# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/simpleshader.py
# Compiled at: 2018-12-10 17:20:58
# Size of source mod 2**32: 2118 bytes
__doc__ = 'Simple fullscreen shader\n\nAllows to easily apply a fullscreen shader to the screen without big hassle.\nEnables multi-staged rendering by exposing Framebuffer content as textures.'
from OpenGL.GL import *
from PyreeEngine.layers import LayerContext
from PyreeEngine.framebuffers import RegularFramebuffer, DefaultFramebuffer
from PyreeEngine.util import Resolution
from PyreeEngine.shaders import HotloadingShader, DebugShader
from PyreeEngine.basicObjects import FSQuad
from PyreeEngine.camera import Camera
from typing import List, Union

class SimpleShader:

    def __init__(self, context: LayerContext, quadz: float=0):
        self.context = context
        self.context.addresolutioncallback(self.resolutionchangecallback)
        self.quadz = quadz
        self.framebuffer = RegularFramebuffer(self.context.resolution)
        self.shader = None
        self.fsquad = FSQuad(z=quadz)
        self.camera = Camera()
        self.updateshader(self.shader)

    def updateshader(self, newshader: HotloadingShader):
        self.shader = newshader
        if self.shader is not None:
            self.fsquad.shader = self.shader
        else:
            self.fsquad.shader = DebugShader()

    def resolutionchangecallback(self, newres: Resolution):
        self.framebuffer = RegularFramebuffer(self.context.resolution)

    def __del__(self):
        self.context.removeresolutionscallback(self.resolutionchangecallback)

    def tick(self):
        self.shader.tick()
        self.framebuffer.bindFramebuffer()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setuniform('time', self.context.time)
        self.setuniform('dt', self.context.dt)
        self.setuniform('frame', self.context.frame)
        self.fsquad.render(self.camera.viewMatrix)
        self.framebuffer.rendertoscreen()

    def setuniform(self, name: str, value: Union[(any, List[any])]):
        self.fsquad.uniforms[name] = value

    def clearuniforms(self):
        self.fsquad.uniforms = {}