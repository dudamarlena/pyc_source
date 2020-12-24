# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\cocos\shader.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 10958 bytes
from __future__ import division, print_function, unicode_literals
import six
from . import compat
from ctypes import byref, c_char, c_char_p, c_float, c_int, cast, create_string_buffer, POINTER
from pyglet import gl

class GLSLException(Exception):
    pass


def glsl_log(handle):
    if handle == 0:
        return ''
    log_len = c_int(0)
    gl.glGetObjectParameterivARB(handle, gl.GL_OBJECT_INFO_LOG_LENGTH_ARB, byref(log_len))
    if log_len.value == 0:
        return ''
    log = create_string_buffer(log_len.value)
    chars_written = c_int(0)
    gl.glGetInfoLogARB(handle, log_len.value, byref(chars_written), log)
    return log.value


class Shader(object):
    s_tag = 0

    def __init__(self, name, prog):
        prog = compat.asciibytes(prog)
        self.name = name
        self.prog = prog
        self.shader = 0
        self.compiling = False
        self.tag = -1
        self.dependencies = []

    def __del__(self):
        self.destroy()

    def _source(self):
        if self.tag == Shader.s_tag:
            return []
        self.tag = Shader.s_tag
        r = []
        for d in self.dependencies:
            r.extend(d._source())
        else:
            r.append(self.prog)
            return r

    def _compile(self):
        if self.shader:
            return
        else:
            if self.compiling:
                return
            self.compiling = True
            self.shader = gl.glCreateShaderObjectARB(self.shaderType())
            if self.shader == 0:
                raise GLSLException('faled to create shader object')
            prog = c_char_p(self.prog)
            length = c_int(-1)
            gl.glShaderSourceARB(self.shader, 1, cast(byref(prog), POINTER(POINTER(c_char))), byref(length))
            gl.glCompileShaderARB(self.shader)
            self.compiling = False
            compile_status = c_int(0)
            gl.glGetObjectParameterivARB(self.shader, gl.GL_OBJECT_COMPILE_STATUS_ARB, byref(compile_status))
            err = compile_status.value or glsl_log(self.shader)
            gl.glDeleteObjectARB(self.shader)
            self.shader = 0
            raise GLSLException('failed to compile shader', err)

    def _attachTo(self, program):
        if self.tag == Shader.s_tag:
            return
        self.tag = Shader.s_tag
        for d in self.dependencies:
            d._attachTo(program)
        else:
            if self.isCompiled():
                gl.glAttachObjectARB(program, self.shader)

    def addDependency(self, shader):
        self.dependencies.append(shader)
        return self

    def destroy(self):
        if self.shader != 0:
            gl.glDeleteObjectARB(self.shader)

    def shaderType(self):
        raise NotImplementedError()

    def isCompiled(self):
        return self.shader != 0

    def attachTo(self, program):
        Shader.s_tag = Shader.s_tag + 1
        self._attachTo(program)

    def attachFlat(self, program):
        if self.isCompiled():
            gl.glAttachObjectARB(program, self.shader)

    def compileFlat(self):
        if self.isCompiled():
            return
        else:
            self.shader = gl.glCreateShaderObjectARB(self.shaderType())
            if self.shader == 0:
                raise GLSLException('faled to create shader object')
            all_source = [(b'\n').join(self._source())]
            prog = (c_char_p * len(all_source))(*all_source)
            length = c_int * len(all_source)(-1)
            gl.glShaderSourceARB(self.shader, len(all_source), cast(prog, POINTER(POINTER(c_char))), length)
            gl.glCompileShaderARB(self.shader)
            compile_status = c_int(0)
            gl.glGetObjectParameterivARB(self.shader, gl.GL_OBJECT_COMPILE_STATUS_ARB, byref(compile_status))
            err = compile_status.value or glsl_log(self.shader)
            gl.glDeleteObjectARB(self.shader)
            self.shader = 0
            raise GLSLException('failed to compile shader', err)

    def compile(self):
        if self.isCompiled():
            return
        for d in self.dependencies:
            d.compile()
        else:
            self._compile()


class VertexShader(Shader):

    def shaderType(self):
        return gl.GL_VERTEX_SHADER_ARB


class FragmentShader(Shader):

    def shaderType(self):
        return gl.GL_FRAGMENT_SHADER_ARB


class ShaderProgram(object):

    @classmethod
    def simple_program(cls, name, vertex_code, fragment_code):
        """Intended to cut boilerplate when doing simple shaders

           name : string with program name
           vertex_code : None or string with the vertex shader code
           fragment_code : None or string with the fragment shader code
        """
        shader_p = cls()
        if vertex_code:
            shader_p.setShader(VertexShader(name + '_vp', vertex_code))
        if fragment_code:
            shader_p.setShader(FragmentShader(name + '_fp', fragment_code))
        shader_p.prog()
        return shader_p

    def __init__(self, vertex_shader=None, fragment_shader=None):
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        self.program = 0

    def __del__(self):
        self.destroy()

    def destroy(self):
        if self.program != 0:
            gl.glDeleteObjectARB(self.program)

    def setShader(self, shader):
        if isinstance(shader, FragmentShader):
            self.fragment_shader = shader
        if isinstance(shader, VertexShader):
            self.vertex_shader = shader
        if self.program != 0:
            gl.glDeleteObjectARB(self.program)

    def link(self):
        if self.vertex_shader is not None:
            self.vertex_shader.compileFlat()
        if self.fragment_shader is not None:
            self.fragment_shader.compileFlat()
        self.program = gl.glCreateProgramObjectARB()
        if self.program == 0:
            raise GLSLException('failed to create program object')
        if self.vertex_shader is not None:
            self.vertex_shader.attachFlat(self.program)
        if self.fragment_shader is not None:
            self.fragment_shader.attachFlat(self.program)
        gl.glLinkProgramARB(self.program)
        link_status = c_int(0)
        gl.glGetObjectParameterivARB(self.program, gl.GL_OBJECT_LINK_STATUS_ARB, byref(link_status))
        if link_status.value == 0:
            err = glsl_log(self.program)
            gl.glDeleteObjectARB(self.program)
            self.program = 0
            raise GLSLException('failed to link shader', err)
        self.__class__._uloc_ = {}
        self.__class__._vloc_ = {}
        return self.program

    def prog(self):
        if self.program:
            return self.program
        return self.link()

    def install(self):
        p = self.prog()
        if p != 0:
            gl.glUseProgramObjectARB(p)

    def uninstall(self):
        gl.glUseProgramObjectARB(0)

    def uniformLoc--- This code section failed: ---

 L. 286         0  LOAD_GLOBAL              compat
                2  LOAD_METHOD              asciibytes
                4  LOAD_FAST                'var'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               'var'

 L. 287        10  SETUP_FINALLY        26  'to 26'

 L. 288        12  LOAD_FAST                'self'
               14  LOAD_ATTR                __class__
               16  LOAD_ATTR                _uloc_
               18  LOAD_FAST                'var'
               20  BINARY_SUBSCR    
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    10  '10'

 L. 289        26  POP_TOP          
               28  POP_TOP          
               30  POP_TOP          

 L. 290        32  LOAD_FAST                'self'
               34  LOAD_ATTR                program
               36  LOAD_CONST               0
               38  COMPARE_OP               ==
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L. 291        42  LOAD_FAST                'self'
               44  LOAD_METHOD              link
               46  CALL_METHOD_0         0  ''
               48  POP_TOP          
             50_0  COME_FROM            40  '40'

 L. 292        50  LOAD_GLOBAL              gl
               52  LOAD_METHOD              glGetUniformLocationARB
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                program
               58  LOAD_FAST                'var'
               60  CALL_METHOD_2         2  ''
               62  DUP_TOP          
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                __class__
               68  LOAD_ATTR                _uloc_
               70  LOAD_FAST                'var'
               72  STORE_SUBSCR     
               74  STORE_FAST               'v'

 L. 293        76  LOAD_FAST                'v'
               78  ROT_FOUR         
               80  POP_EXCEPT       
               82  RETURN_VALUE     
               84  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 48

    def uset1F(self, var, x):
        gl.glUniform1fARB(self.uniformLoc(var), x)

    def uset2F(self, var, x, y):
        gl.glUniform2fARB(self.uniformLoc(var), x, y)

    def uset3F(self, var, x, y, z):
        gl.glUniform3fARB(self.uniformLoc(var), x, y, z)

    def uset4F(self, var, x, y, z, w):
        gl.glUniform4fARB(self.uniformLoc(var), x, y, z, w)

    def uset1I(self, var, x):
        gl.glUniform1iARB(self.uniformLoc(var), x)

    def uset2I(self, var, x, y):
        gl.glUniform2iARB(self.uniformLoc(var), x, y)

    def uset3I(self, var, x, y, z):
        gl.glUniform3iARB(self.uniformLoc(var), x, y, z)

    def usetM4F(self, var, matrix, transpose=False):
        gl.glUniformMatrix4fvARB(self.uniformLoc(var), 1, transpose, (c_float * 16)(*matrix))

    def usetTex(self, var, unit, target, tx):
        """
        var : name of variable to write
        unit : texture unit
        target : target for glBindTexture
        tx : texture ID
        """
        gl.glUniform1iARB(self.uniformLoc(var), unit)
        gl.glActiveTexture(gl.GL_TEXTURE0 + unit)
        gl.glBindTexture(target, tx)


__all__ = [
 'VertexShader', 'FragmentShader', 'ShaderProgram', 'GLSLException']