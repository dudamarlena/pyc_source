# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/basicObjects2.py
# Compiled at: 2018-12-06 15:37:31
# Size of source mod 2**32: 6111 bytes
from typing import Union, List, Tuple, Callable, Optional
from PyreeEngine.engine import PyreeObject
from OpenGL.GL import *
from OpenGL.GL import shaders
from PyreeEngine.engine import DeferredGBufShader, ModelObject
from pathlib import Path
import numpy as np
from PyreeEngine.objloader import ObjLoader

class ObjModelObject(ModelObject):

    def __init__(self, pathToObj):
        super(ObjModelObject, self).__init__()
        self.vbo = None
        self.vao = None
        self.tricount = None
        self.shaderProgram = DeferredGBufShader.getprogram()
        self.textures = []
        if pathToObj is not None:
            self.loadFromObj(pathToObj)

    def loadFromObj(self, pathToObj: Path):
        vertlist = ObjLoader(pathToObj).verts
        verts = []
        for l in vertlist:
            verts += l

        verts = np.array(verts, np.float32)
        self.tricount = int(len(verts) / 8)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * verts.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8 * verts.itemsize, ctypes.c_void_p(3 * verts.itemsize))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * verts.itemsize, ctypes.c_void_p(5 * verts.itemsize))
        glEnableVertexAttribArray(2)

    def render(self, viewProjMatrix):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBindVertexArray(self.vao)
        glUseProgram(self.shaderProgram)
        self.bindTextures(self.textures)
        uniformLoc = glGetUniformLocation(self.shaderProgram, 'MVP')
        if not uniformLoc == -1:
            glUniformMatrix4fv(uniformLoc, 1, GL_TRUE, viewProjMatrix * self.getModelMatrix())
        glDrawArrays(GL_TRIANGLES, 0, self.tricount)

    def setTextures(self, textures: List[int]):
        self.textures = textures

    def bindTextures(self, textures: List[int]):
        glUseProgram(self.shaderProgram)
        if textures:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, textures[0])
            loc = glGetUniformLocation(self.shaderProgram, 'tex0')
            if not loc == -1:
                glUniform1i(loc, 0)
        if len(textures) > 1:
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, textures[1])
            loc = glGetUniformLocation(self.shaderProgram, 'tex1')
            if not loc == -1:
                glUniform1i(loc, 1)
        if len(textures) > 2:
            glActiveTexture(GL_TEXTURE2)
            glBindTexture(GL_TEXTURE_2D, textures[2])
            loc = glGetUniformLocation(self.shaderProgram, 'tex2')
            if not loc == -1:
                glUniform1i(loc, 2)


class FullscreenQuad(ModelObject):

    def __init__(self, shaderProgram=None):
        super(FullscreenQuad, self).__init__()
        self.vbo = None
        self.vao = None
        self.textures = []
        if shaderProgram is not None:
            self.shaderProgram = shaderProgram
        else:
            vertcode = '#version 450 core\n            layout (location = 0) in vec2 posIn;\n            void main()\n            {\n                gl_Position = vec4(posIn, 0, 1);\n            }'
            fragcode = '#version 450 core\n            uniform sampler2D tex0;\n            uniform sampler2D tex1;\n            uniform sampler2D tex2;\n            layout (location = 0) out vec4 colorOut;\n            void main()\n            {\n                colorOut = texelFetch(tex0, ivec2(gl_FragCoord.xy), 0);\n                colorOut = texture(tex0, vec2(gl_FragCoord.xy)/vec2(640, 480));\n            }'
            self.vertShader = shaders.compileShader(vertcode, GL_VERTEX_SHADER)
            self.fragShader = shaders.compileShader(fragcode, GL_FRAGMENT_SHADER)
            self.shaderProgram = shaders.compileProgram(self.vertShader, self.fragShader)
        verts = np.array([[-1, -1],
         [
          -1, 1],
         [
          1, -1],
         [
          1, 1]], np.float32)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, verts.nbytes, verts, GL_STATIC_DRAW)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

    def render(self, viewProjMatrix):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBindVertexArray(self.vao)
        self.bindTextures(self.textures)
        glUseProgram(self.shaderProgram)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    def setTextures(self, textures: List[int]):
        self.textures = textures

    def bindTextures(self, textures: List[int]):
        glUseProgram(self.shaderProgram)
        if textures:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, textures[0])
            loc = glGetUniformLocation(self.shaderProgram, 'tex0')
            if not loc == -1:
                glUniform1i(loc, 0)
        if len(textures) > 1:
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, textures[1])
            loc = glGetUniformLocation(self.shaderProgram, 'tex1')
            if not loc == -1:
                glUniform1i(loc, 1)
        if len(textures) > 2:
            glActiveTexture(GL_TEXTURE2)
            glBindTexture(GL_TEXTURE_2D, textures[2])
            loc = glGetUniformLocation(self.shaderProgram, 'tex2')
            if not loc == -1:
                glUniform1i(loc, 2)