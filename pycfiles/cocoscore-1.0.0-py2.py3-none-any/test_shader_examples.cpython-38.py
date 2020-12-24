# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_shader_examples.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 11708 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'shader, uniform'
import time
from pyglet.gl import *
import cocos
import cocos.director as director
from cocos.sprite import Sprite
import pyglet
from pyglet.window import key
from cocos import shader

def load_texture(fname):
    pic = pyglet.image.load(fname, file=(pyglet.resource.file(fname)))
    texture = pic.get_texture()
    return texture


class TestLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, textures, available_programs, base_color):
        super(TestLayer, self).__init__()
        self.textures = textures
        self.texture_selector = 0
        self.texture = textures[self.texture_selector]
        self.available_programs = available_programs
        self.program_selector = 0
        self.shader_program = available_programs[self.program_selector]
        self.base_color = base_color
        self.color = base_color
        self.schedule(self.update)

    def on_enter(self):
        super(TestLayer, self).on_enter()
        self.start_time = time.time()

    def draw(self):
        x, y = director.get_window_size()
        x = x // 2
        y = y // 2
        d = 100
        if self.shader_program:
            self.shader_program.set_state(self)
        else:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture.id)
        glPushMatrix()
        self.transform()
        glBegin(GL_TRIANGLES)
        glColor4ub(0, 255, 0, 255)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(x + d, y + d)
        glColor4ub(255, 255, 255, 255)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x - d, y + d)
        glColor4ub(255, 255, 255, 255)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(x + d, y - d)
        glColor4ub(255, 255, 255, 255)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(x - d, y + d)
        glColor4ub(0, 0, 255, 255)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(x - d, y - d)
        glColor4ub(255, 255, 255, 255)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(x + d, y - d)
        glEnd()
        glPopMatrix()
        if self.shader_program:
            self.shader_program.unset_state()
        else:
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)

    def update(self, dt):
        multiplier = 0.5 + 0.5 * ((time.time() - self.start_time) % 2.0 / 2.0)
        self.blackness = 1.0 - multiplier
        self.color = tuple([c * multiplier for c in self.base_color])

    def on_key_press(self, k, m):
        if k in (key.LEFT, key.RIGHT):
            if k == key.LEFT:
                self.program_selector -= 1
            elif k == key.RIGHT:
                self.program_selector += 1
            self.program_selector = self.program_selector % len(self.available_programs)
            self.shader_program = self.available_programs[self.program_selector]
            print('program:', self.shader_program)
        if k in (key.DOWN, key.UP):
            if k == key.DOWN:
                self.texture_selector -= 1
            elif k == key.UP:
                self.texture_selector += 1
            self.texture_selector = self.texture_selector % len(self.textures)
            self.texture = self.textures[self.texture_selector]


class ProgramUntexturedFixedHardcodedColor(shader.ShaderProgram):
    """ProgramUntexturedFixedHardcodedColor"""
    vertex_code = None
    fragment_code = '\n    void main() {\n        gl_FragColor = vec4(1.0, 1.0, 0.0, 1.0);\n    }\n    '

    @classmethod
    def create(cls):
        return cls.simple_program('yellow', cls.vertex_code, cls.fragment_code)

    def set_state(self, provider):
        self.install()

    def unset_state(self):
        self.uninstall()


class ProgramUntexturedProgramableColor(shader.ShaderProgram):
    """ProgramUntexturedProgramableColor"""
    vertex_code = None
    fragment_code = '\n    uniform vec4 color;\n\n    void main() {\n        gl_FragColor = color;\n    }\n    '

    @classmethod
    def create(cls):
        return cls.simple_program('prog_color', cls.vertex_code, cls.fragment_code)

    def set_state(self, provider):
        self.install()
        (self.uset4F)(*('color', ), *provider.color)

    def unset_state(self):
        self.uninstall()


class ProgramUntexturedInterpolatedColor(shader.ShaderProgram):
    """ProgramUntexturedInterpolatedColor"""
    vertex_code = '\n    void main()\n    {\n        gl_FrontColor = gl_Color;\n        gl_Position = ftransform();\n    }\n    '
    fragment_code = '\n    void main()\n    {\n        gl_FragColor = gl_Color;\n    }\n    '

    @classmethod
    def create(cls):
        return cls.simple_program('gradient', cls.vertex_code, cls.fragment_code)

    def set_state(self, provider):
        self.install()

    def unset_state(self):
        self.uninstall()


class ProgramTexturedNoTint(shader.ShaderProgram):
    """ProgramTexturedNoTint"""
    vertex_code = '\n    void main()\n    {\n        gl_TexCoord[0] = gl_MultiTexCoord0;\n        gl_Position = ftransform();\n    }\n    '
    fragment_code = '\n    uniform sampler2D tex;\n\n    void main()\n    {\n        vec4 texel_color = texture2D(tex, gl_TexCoord[0].st);\n        gl_FragColor = texel_color;\n    }\n    '

    @classmethod
    def create(cls):
        return cls.simple_program('texture_only', cls.vertex_code, cls.fragment_code)

    def set_state(self, provider):
        self.install()
        self.usetTex('tex', 0, GL_TEXTURE_2D, provider.texture.id)

    def unset_state(self):
        self.uninstall()


class ProgramTexturedTinted(shader.ShaderProgram):
    """ProgramTexturedTinted"""
    vertex_code = '\n    void main()\n    {\n        gl_FrontColor = gl_Color;\n        gl_TexCoord[0] = gl_MultiTexCoord0;\n        gl_Position = ftransform();\n    }\n    '
    fragment_code = '\n    uniform sampler2D tex;\n\n    void main()\n    {\n        vec4 texel_color = texture2D(tex, gl_TexCoord[0].st);\n        gl_FragColor = texel_color * gl_Color;\n    }\n    '

    @classmethod
    def create(cls):
        return cls.simple_program('texture_tinted', cls.vertex_code, cls.fragment_code)

    def set_state(self, provider):
        self.install()
        self.usetTex('tex', 0, GL_TEXTURE_2D, provider.texture.id)

    def unset_state(self):
        self.uninstall()


class ProgramTexturedTintedProgramableDarkness(shader.ShaderProgram):
    """ProgramTexturedTintedProgramableDarkness"""
    vertex_code = '\n    void main()\n    {\n        gl_FrontColor = gl_Color;\n        gl_TexCoord[0] = gl_MultiTexCoord0;\n        gl_Position = ftransform();\n    }\n    '
    fragment_code = '\n    uniform sampler2D tex;\n    uniform float blackness;\n\n    void main()\n    {\n        vec4 texel = texture2D(tex, gl_TexCoord[0].st);\n        texel *= gl_Color;\n        texel = vec4(texel.rgb * (1.0 - blackness), texel.a);\n        gl_FragColor = texel;\n    }\n    '

    @classmethod
    def create(cls):
        return cls.simple_program('texture_tinted_darkened', cls.vertex_code, cls.fragment_code)

    def set_state(self, provider):
        self.install()
        self.usetTex('tex', 0, GL_TEXTURE_2D, provider.texture.id)
        self.uset1F('blackness', provider.blackness)

    def unset_state(self):
        self.uninstall()


def get_available_programs():
    return [
     None,
     ProgramUntexturedFixedHardcodedColor.create(),
     ProgramUntexturedProgramableColor.create(),
     ProgramUntexturedInterpolatedColor.create(),
     ProgramTexturedNoTint.create(),
     ProgramTexturedTinted.create(),
     ProgramTexturedTintedProgramableDarkness.create()]


description = '\nShows the efect of different example shaders.\nUse arrow keys - Left, Right change shaders, Up, Down textures.\n'

def main():
    print(description)
    director.init()
    textures = [
     load_texture('grossinis_sister1.png'),
     load_texture('fire.png')]
    available_programs = get_available_programs()
    test_layer = TestLayer(textures, available_programs, (1.0, 0.0, 1.0, 1.0))
    main_scene = cocos.scene.Scene(cocos.layer.ColorLayer(255, 214, 173, 255), test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()