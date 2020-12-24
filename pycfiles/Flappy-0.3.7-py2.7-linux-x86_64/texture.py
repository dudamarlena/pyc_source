# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/display3d/texture.py
# Compiled at: 2014-03-13 10:09:15
from flappy import _gl as gl

class Texture(object):

    def __init__(self, width, height):
        self.gl_texture = gl.createTexture()
        self.width = width
        self.height = height
        gl.bindTexture(gl.TEXTURE_2D, self.gl_texture)
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, width, height, 0, gl.RGBA, gl.UNSIGNED_BYTE, 0)