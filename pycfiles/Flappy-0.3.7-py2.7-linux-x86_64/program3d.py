# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/display3d/program3d.py
# Compiled at: 2014-03-13 10:09:15
from flappy import _gl as gl

class Program3D(object):

    def __init__(self):
        self.gl_program = gl.createProgram()
        self.gl_vshader = gl.createShader(gl.VERTEX_SHADER)
        self.gl_fshader = gl.createShader(gl.FRAGMENT_SHADER)

    def __del__(self):
        gl.deleteProgram(self.gl_program)

    def upload(self, vertex_shader_src, fragment_shader_src):
        gl.shaderSource(self.gl_vshader, vertex_shader_src)
        gl.compileShader(self.gl_vshader)
        if gl.getShaderParameter(self.gl_vshader, gl.COMPILE_STATUS) == 0:
            raise RuntimeError('Error compiling vertex shader')
        gl.shaderSource(self.gl_fshader, fragment_shader_src)
        gl.compileShader(self.gl_fshader)
        if gl.getShaderParameter(self.gl_fshader, gl.COMPILE_STATUS) == 0:
            raise RuntimeError('Error compiling fragment shader')
        gl.attachShader(self.gl_program, self.gl_vshader)
        gl.attachShader(self.gl_program, self.gl_fshader)
        gl.linkProgram(self.gl_program)
        if gl.getProgramParameter(self.gl_program, gl.LINK_STATUS) == 0:
            raise RuntimeError('Error linking program')