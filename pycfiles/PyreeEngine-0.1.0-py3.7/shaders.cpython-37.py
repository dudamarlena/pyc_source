# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyreeEngine/shaders.py
# Compiled at: 2018-12-10 16:01:01
# Size of source mod 2**32: 6042 bytes
"""Handy shader classes"""
from OpenGL.GL import *
from OpenGL.GL import shaders
import traceback, sys
from pathlib import Path
import inotify_simple

class Shader:

    def __init__(self):
        self.shaderprogram = None

    def getshaderprogram(self) -> shaders.ShaderProgram:
        return self.shaderprogram


class DebugShader(Shader):
    vertexCode = '#version 450 core\n    layout (location = 0) in vec3 posIn;\n    layout (location = 1) in vec2 uvIn;\n    layout (location = 2) in vec3 normIn;\n\n    layout (location = 0) out vec3 posOut;\n    layout (location = 1) out vec2 uvOut;\n    layout (location = 2) out vec3 normOut;\n\n    uniform mat4 MVP;\n\n    void main()\n    {\n        gl_Position = MVP * vec4(posIn, 1);\n        posOut = (MVP * vec4(posIn, 1)).xyz;\n        uvOut = uvIn;\n        normOut = normIn;\n    }\n    '
    fragCode = '#version 450 core\n    layout (location = 0) in vec3 posIn;\n    layout (location = 1) in vec2 uvIn;\n    layout (location = 2) in vec3 normIn;\n\n    layout (location = 0) out vec4 colorOut;\n    void main()\n    {\n        colorOut = vec4(uvIn, 0, 1);\n    }\n    '
    vertShader = None
    fragShader = None
    program = None

    def getshaderprogram(self):
        if DebugShader.program is None:
            DebugShader.vertShader = shaders.compileShader(DebugShader.vertexCode, GL_VERTEX_SHADER)
            DebugShader.fragShader = shaders.compileShader(DebugShader.fragCode, GL_FRAGMENT_SHADER)
            DebugShader.program = shaders.compileProgram(DebugShader.vertShader, DebugShader.fragShader)
        return DebugShader.program


class FullscreenTexture(Shader):
    vertexCode = '#version 450 core\n        layout (location = 0) in vec3 posIn;\n        layout (location = 1) in vec2 uvIn;\n        layout (location = 2) in vec3 normIn;\n\n        layout (location = 0) out vec3 posOut;\n        layout (location = 1) out vec2 uvOut;\n        layout (location = 2) out vec3 normOut;\n\n        uniform mat4 MVP;\n\n        void main()\n        {\n            gl_Position = MVP * vec4(posIn, 1);\n            posOut = (MVP * vec4(posIn, 1)).xyz;\n            uvOut = uvIn;\n            normOut = normIn;\n        }\n        '
    fragCode = '#version 450 core\n        layout (location = 0) in vec3 posIn;\n        layout (location = 1) in vec2 uvIn;\n        layout (location = 2) in vec3 normIn;\n        \n        layout(binding=0) uniform sampler2D tex1;\n        \n        layout (location = 0) out vec4 colorOut;\n        void main()\n        {\n            colorOut = texture(tex1, vec2(uvIn.x, uvIn.y)).rgba;\n            colorOut.a = 1.;\n        }\n        '
    vertShader = None
    fragShader = None
    program = None

    def getshaderprogram(self):
        if FullscreenTexture.program is None:
            FullscreenTexture.vertShader = shaders.compileShader(FullscreenTexture.vertexCode, GL_VERTEX_SHADER)
            FullscreenTexture.fragShader = shaders.compileShader(FullscreenTexture.fragCode, GL_FRAGMENT_SHADER)
            FullscreenTexture.program = shaders.compileProgram(FullscreenTexture.vertShader, FullscreenTexture.fragShader)
        return FullscreenTexture.program


class HotloadingShader(Shader):

    def __init__(self, vertexpath, fragmentpath, geometrypath=None):
        super(HotloadingShader, self).__init__()
        self.shaderprogram = DebugShader().getshaderprogram()
        self.vertShader = None
        self.fragShader = None
        self.geomShader = None
        fl = inotify_simple.flags.CREATE | inotify_simple.flags.MODIFY | inotify_simple.flags.MOVED_TO
        self.inotify = inotify_simple.INotify()
        self.vertexPath = vertexpath
        self.vertWatch = self.inotify.add_watch(self.vertexPath.parent, fl)
        self.fragmentPath = fragmentpath
        self.fragWatch = self.inotify.add_watch(self.fragmentPath.parent, fl)
        self.geometryPath = geometrypath
        if geometrypath is not None:
            self.geomWatch = self.inotify.add_watch(self.geometryPath.parent, fl)
        self.regenShader()

    def regenShader(self):
        try:
            if self.vertexPath.exists():
                with self.vertexPath.open() as (f):
                    self.vertShader = shaders.compileShader(f.read(), GL_VERTEX_SHADER)
            else:
                print("HOTLOADSHADER ERROR: vertex file doesn't exist")
                return
                if self.fragmentPath.exists():
                    with self.fragmentPath.open() as (f):
                        self.fragShader = shaders.compileShader(f.read(), GL_FRAGMENT_SHADER)
                else:
                    print("HOTLOADSHADER ERROR: fragment file doesn't exist")
                    return
                    if self.geometryPath is not None:
                        if self.geometryPath.exists():
                            with self.geometryPath.open() as (f):
                                self.vertShader = shaders.compileShader(f.read(), GL_FRAGMENT_SHADER)
                        else:
                            print("HOTLOADSHADER ERROR: geometry file doesn't exist")
                            return
                    else:
                        if self.shaderprogram is not None:
                            pass
                        if self.geometryPath is None:
                            self.shaderprogram = shaders.compileProgram(self.vertShader, self.fragShader)
                        else:
                            self.shaderprogram = shaders.compileProgram(self.vertShader, self.fragShader, self.geomShader)
        except Exception as exc:
            try:
                print((traceback.format_exc()), file=(sys.stderr))
                print(exc, file=(sys.stderr))
            finally:
                exc = None
                del exc

    def tick(self):
        events = self.inotify.read(0)
        for event in events:
            if not (event.name == self.vertexPath.name or event.name == self.fragmentPath.name or self.geometryPath) is not None or self.geometryPath.name == self.geometryPath.name:
                self.regenShader()

    def __del__(self):
        if self.shaderprogram:
            pass