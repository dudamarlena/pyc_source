# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\test\test_shader.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2383 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'shader, quadric'
from pyglet.gl import *
import cocos
import cocos.director as director
from cocos.sprite import Sprite
import pyglet
from cocos import shader

class TestLayer(cocos.layer.Layer):

    def draw(self):
        x, y = director.get_window_size()
        x = x // 2
        y = y // 2
        d = 100
        cuadric.install()
        glColor4ub(255, 255, 255, 255)
        glBegin(GL_TRIANGLES)
        glTexCoord2f(0.5, 0)
        glVertex2f(x + d, y + d)
        glTexCoord2f(0, 0)
        glVertex2f(x, y + d)
        glTexCoord2f(1, 1)
        glVertex2f(x + d, y)
        glTexCoord2f(0.5, 0)
        glVertex2f(x - d, y - d)
        glTexCoord2f(0, 0)
        glVertex2f(x, y - d)
        glTexCoord2f(1, 1)
        glVertex2f(x - d, y)
        glTexCoord2f(0.5, 0)
        glVertex2f(x + d, y - d)
        glTexCoord2f(0, 0)
        glVertex2f(x, y - d)
        glTexCoord2f(1, 1)
        glVertex2f(x + d, y)
        glTexCoord2f(0.5, 0)
        glVertex2f(x - d, y + d)
        glTexCoord2f(0, 0)
        glVertex2f(x, y + d)
        glTexCoord2f(1, 1)
        glVertex2f(x - d, y)
        glTexCoord2f(0.5, 1)
        glVertex2f(x, y)
        glVertex2f(x, y + d)
        glVertex2f(x + d, y)
        glVertex2f(x, y)
        glVertex2f(x, y - d)
        glVertex2f(x + d, y)
        glVertex2f(x, y)
        glVertex2f(x, y + d)
        glVertex2f(x - d, y)
        glVertex2f(x, y)
        glVertex2f(x, y - d)
        glVertex2f(x - d, y)
        glEnd()
        cuadric.uninstall()


cuadric_t = '\nvoid main() {\n    vec2 pos = gl_TexCoord[0].st;\n    float res = pos.x*pos.x - pos.y;\n    if (res<0.0) {\n        gl_FragColor = vec4(1.0,1.0,1.0,1.0);\n    } else {\n        gl_FragColor = vec4(0.0,0.0,0.0,0.0);\n    }\n}\n'
cuadric = shader.ShaderProgram()
cuadric.setShader(shader.FragmentShader('cuadric_t', cuadric_t))

def main():
    director.init()
    test_layer = TestLayer()
    main_scene = cocos.scene.Scene(test_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()