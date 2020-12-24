# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\shader.py
# Compiled at: 2020-03-29 13:19:23
# Size of source mod 2**32: 20253 bytes
__doc__ = 'Utilities for dealing with Shaders in OpenGL 3.3+.\n'
from ctypes import *
from collections import namedtuple
import weakref
from typing import List, Tuple, Iterable, Dict
from pyglet import gl

class ShaderException(Exception):
    pass


_uniform_getters = {gl.GLint: gl.glGetUniformiv, 
 gl.GLfloat: gl.glGetUniformfv}
_uniform_setters = {gl.GL_INT: (gl.GLint, gl.glUniform1iv, 1, 1), 
 gl.GL_INT_VEC2: (gl.GLint, gl.glUniform2iv, 2, 1), 
 gl.GL_INT_VEC3: (gl.GLint, gl.glUniform3iv, 3, 1), 
 gl.GL_INT_VEC4: (gl.GLint, gl.glUniform4iv, 4, 1), 
 gl.GL_FLOAT: (gl.GLfloat, gl.glUniform1fv, 1, 1), 
 gl.GL_FLOAT_VEC2: (gl.GLfloat, gl.glUniform2fv, 2, 1), 
 gl.GL_FLOAT_VEC3: (gl.GLfloat, gl.glUniform3fv, 3, 1), 
 gl.GL_FLOAT_VEC4: (gl.GLfloat, gl.glUniform4fv, 4, 1), 
 gl.GL_SAMPLER_2D: (gl.GLint, gl.glUniform1iv, 1, 1), 
 gl.GL_FLOAT_MAT2: (gl.GLfloat, gl.glUniformMatrix2fv, 4, 1), 
 gl.GL_FLOAT_MAT3: (gl.GLfloat, gl.glUniformMatrix3fv, 9, 1), 
 gl.GL_FLOAT_MAT4: (gl.GLfloat, gl.glUniformMatrix4fv, 16, 1)}

def _create_getter_func(program_id, location, gl_getter, c_array, length):
    if length == 1:

        def getter_func():
            gl_getter(program_id, location, c_array)
            return c_array[0]

    else:

        def getter_func():
            gl_getter(program_id, location, c_array)
            return c_array[:]

    return getter_func


def _create_setter_func(location, gl_setter, c_array, length, count, ptr, is_matrix):
    if is_matrix:

        def setter_func(value):
            c_array[:] = value
            gl_setter(location, count, gl.GL_FALSE, ptr)

    elif length == 1 and count == 1:

        def setter_func(value):
            c_array[0] = value
            gl_setter(location, count, ptr)

    elif length > 1 and count == 1:

        def setter_func(values):
            c_array[:] = values
            gl_setter(location, count, ptr)

    else:
        raise NotImplementedError('Uniform type not yet supported.')
    return setter_func


Uniform = namedtuple('Uniform', 'getter, setter')
ShaderCode = str
Shader = Tuple[(ShaderCode, gl.GLuint)]

class Program:
    """Program"""

    def __init__(self, *shaders: Shader):
        self.prog_id = prog_id = gl.glCreateProgram()
        shaders_id = []
        for shader_code, shader_type in shaders:
            shader = compile_shader(shader_code, shader_type)
            gl.glAttachShader(self.prog_id, shader)
            shaders_id.append(shader)

        gl.glLinkProgram(self.prog_id)
        for shader in shaders_id:
            gl.glDeleteShader(shader)

        self._uniforms = {}
        self._introspect_uniforms()
        weakref.finalize(self, Program._delete, shaders_id, prog_id)

    @staticmethod
    def _delete(shaders_id, prog_id):
        if gl.current_context is None:
            return
        for shader_id in shaders_id:
            gl.glDetachShader(prog_id, shader_id)

        gl.glDeleteProgram(prog_id)

    def release(self):
        if self.prog_id != 0:
            gl.glDeleteProgram(self.prog_id)
            self.prog_id = 0

    def __getitem__(self, item):
        try:
            uniform = self._uniforms[item]
        except KeyError:
            raise ShaderException(f"Uniform with the name `{item}` was not found.")

        return uniform.getter()

    def __setitem__(self, key, value):
        try:
            uniform = self._uniforms[key]
        except KeyError:
            raise ShaderException(f"Uniform with the name `{key}` was not found.")

        uniform.setter(value)

    def __enter__(self):
        gl.glUseProgram(self.prog_id)

    def __exit__(self, exception_type, exception_value, traceback):
        gl.glUseProgram(0)

    def get_num_active(self, variable_type: gl.GLenum) -> int:
        """Get the number of active variables of the passed GL type.

        variable_type can be GL_ACTIVE_ATTRIBUTES, GL_ACTIVE_UNIFORMS, etc.
        """
        num_active = gl.GLint(0)
        gl.glGetProgramiv(self.prog_id, variable_type, byref(num_active))
        return num_active.value

    def _introspect_uniforms(self):
        for index in range(self.get_num_active(gl.GL_ACTIVE_UNIFORMS)):
            uniform_name, u_type, u_size = self.query_uniform(index)
            loc = gl.glGetUniformLocation(self.prog_id, uniform_name.encode('utf-8'))
            if loc == -1:
                continue
            try:
                gl_type, gl_setter, length, count = _uniform_setters[u_type]
            except KeyError:
                raise ShaderException(f"Unsupported Uniform type {u_type}")

            gl_getter = _uniform_getters[gl_type]
            is_matrix = u_type in (gl.GL_FLOAT_MAT2, gl.GL_FLOAT_MAT3, gl.GL_FLOAT_MAT4)
            c_array = (gl_type * length)()
            ptr = cast(c_array, POINTER(gl_type))
            getter = _create_getter_func(self.prog_id, loc, gl_getter, c_array, length)
            setter = _create_setter_func(loc, gl_setter, c_array, length, count, ptr, is_matrix)
            self._uniforms[uniform_name] = Uniform(getter, setter)

    def query_uniform(self, index: int) -> Tuple[(str, int, int)]:
        """Retrieve Uniform information at given location.

        Returns the name, the type as a GLenum (GL_FLOAT, ...) and the size. Size is
        greater than 1 only for Uniform arrays, like an array of floats or an array
        of Matrices.
        """
        usize = gl.GLint()
        utype = gl.GLenum()
        buf_size = 192
        uname = create_string_buffer(buf_size)
        gl.glGetActiveUniform(self.prog_id, index, buf_size, None, usize, utype, uname)
        return (
         uname.value.decode(), utype.value, usize.value)


def program(vertex_shader: str, fragment_shader: str) -> Program:
    """Create a new program given the vertex_shader and fragment shader code.
    """
    return Program((
     vertex_shader, gl.GL_VERTEX_SHADER), (
     fragment_shader, gl.GL_FRAGMENT_SHADER))


def compile_shader(source: str, shader_type: gl.GLenum) -> gl.GLuint:
    """Compile the shader code of the given type.

    `shader_type` could be GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, ...

    Returns the shader id as a GLuint
    """
    shader = gl.glCreateShader(shader_type)
    source_bytes = source.encode('utf-8')
    strings = byref(cast(c_char_p(source_bytes), POINTER(c_char)))
    lengths = pointer(c_int(len(source_bytes)))
    gl.glShaderSource(shader, 1, strings, lengths)
    gl.glCompileShader(shader)
    result = c_int()
    gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS, byref(result))
    if result.value == gl.GL_FALSE:
        msg = create_string_buffer(512)
        length = c_int()
        gl.glGetShaderInfoLog(shader, 512, byref(length), msg)
        raise ShaderException(f"Shader compile failure ({result.value}): {msg.value.decode('utf-8')}")
    return shader


class Buffer:
    """Buffer"""
    usages = {'static':gl.GL_STATIC_DRAW, 
     'dynamic':gl.GL_DYNAMIC_DRAW, 
     'stream':gl.GL_STREAM_DRAW}

    def __init__(self, data: bytes, usage: str='static'):
        self.buffer_id = buffer_id = gl.GLuint()
        self.size = len(data)
        gl.glGenBuffers(1, byref(self.buffer_id))
        if self.buffer_id.value == 0:
            raise ShaderException('Cannot create Buffer object.')
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer_id)
        self.usage = Buffer.usages[usage]
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.size, data, self.usage)
        weakref.finalize(self, Buffer.release, buffer_id)

    @classmethod
    def create_with_size(cls, size: int, usage: str='static'):
        """Create an empty Buffer storage of the given size."""
        empty_buffer = Buffer('', usage=usage)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, empty_buffer.buffer_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, size, None, Buffer.usages[usage])
        empty_buffer.size = size
        return empty_buffer

    @staticmethod
    def release(buffer_id):
        if gl.current_context is None:
            return
        if buffer_id.value != 0:
            gl.glDeleteBuffers(1, byref(buffer_id))
            buffer_id.value = 0

    def write(self, data: bytes, offset: int=0):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer_id)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, gl.GLintptr(offset), len(data), data)

    def orphan(self):
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.size, None, self.usage)

    def _read(self, size):
        """ Debug method to read data from the buffer. """
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.buffer_id)
        ptr = gl.glMapBufferRange(gl.GL_ARRAY_BUFFER, gl.GLintptr(0), size, gl.GL_MAP_READ_BIT)
        print(f"Reading back from buffer:\n{string_at(ptr, size=size)}")
        gl.glUnmapBuffer(gl.GL_ARRAY_BUFFER)


def buffer(data: bytes, usage: str='static') -> Buffer:
    """Create a new OpenGL Buffer object.
    """
    return Buffer(data, usage)


class BufferDescription:
    """BufferDescription"""
    GL_TYPES_ENUM = {'B':gl.GL_UNSIGNED_BYTE, 
     'f':gl.GL_FLOAT, 
     'i':gl.GL_INT}
    GL_TYPES = {'B':gl.GLubyte, 
     'f':gl.GLfloat, 
     'i':gl.GLint}

    def __init__(self, buff: Buffer, formats: str, attributes: Iterable[str], normalized: Iterable[str]=None, instanced: bool=False):
        self.buffer = buff
        self.attributes = list(attributes)
        self.normalized = set() if normalized is None else set(normalized)
        self.instanced = instanced
        if self.normalized > set(self.attributes):
            raise ShaderException('Normalized attribute not found in attributes.')
        formats_list = formats.split(' ')
        if len(formats_list) != len(self.attributes):
            raise ShaderException(f"Different lengths of formats ({len(formats_list)}) and attributes ({len(self.attributes)})")
        self.formats = []
        for i, fmt in enumerate(formats_list):
            sizechar, type_ = fmt
            if not sizechar not in '1234':
                if type_ not in 'fiB':
                    raise ShaderException('Wrong format {fmt}.')
                size = int(sizechar)
                gl_type_enum = BufferDescription.GL_TYPES_ENUM[type_]
                gl_type = BufferDescription.GL_TYPES[type_]
                attribsize = size * sizeof(gl_type)
                self.formats.append((size, attribsize, gl_type_enum))


class VertexArray:
    """VertexArray"""

    def __init__(self, prog: Program, content: Iterable[BufferDescription], index_buffer: Buffer=None):
        self.program = prog.prog_id
        self.vao = vao = gl.GLuint()
        self.num_vertices = -1
        self.ibo = index_buffer
        gl.glGenVertexArrays(1, byref(self.vao))
        gl.glBindVertexArray(self.vao)
        for buffer_desc in content:
            self._enable_attrib(buffer_desc)

        if self.ibo is not None:
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo.buffer_id)
        weakref.finalize(self, VertexArray.release, vao)

    @staticmethod
    def release(vao):
        if gl.current_context is None:
            return
        if vao.value != 0:
            gl.glDeleteVertexArrays(1, byref(vao))
            vao.value = 0

    def __enter__(self):
        gl.glBindVertexArray(self.vao)
        gl.glUseProgram(self.program)

    def __exit__(self, exception_type, exception_value, traceback):
        gl.glUseProgram(0)

    def _enable_attrib(self, buf_desc: BufferDescription):
        buff = buf_desc.buffer
        stride = sum((attribsize for _, attribsize, _ in buf_desc.formats))
        if buf_desc.instanced:
            if self.num_vertices == -1:
                raise ShaderException('The first vertex attribute cannot be a per instance attribute.')
        else:
            self.num_vertices = max(self.num_vertices, buff.size // stride)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buff.buffer_id)
        offset = 0
        for (size, attribsize, gl_type_enum), attrib in zip(buf_desc.formats, buf_desc.attributes):
            loc = gl.glGetAttribLocation(self.program, attrib.encode('utf-8'))
            if loc == -1:
                raise ShaderException(f"Attribute {attrib} not found in shader program")
            normalized = gl.GL_TRUE if attrib in buf_desc.normalized else gl.GL_FALSE
            gl.glVertexAttribPointer(loc, size, gl_type_enum, normalized, stride, c_void_p(offset))
            if buf_desc.instanced:
                gl.glVertexAttribDivisor(loc, 1)
            offset += attribsize
            gl.glEnableVertexAttribArray(loc)

    def render(self, mode: gl.GLuint, instances: int=1):
        if self.ibo is not None:
            count = self.ibo.size // 4
            gl.glDrawElementsInstanced(mode, count, gl.GL_UNSIGNED_INT, None, instances)
        else:
            gl.glDrawArraysInstanced(mode, 0, self.num_vertices, instances)


def vertex_array(prog: gl.GLuint, content, index_buffer=None):
    """Create a new Vertex Array.
    """
    return VertexArray(prog, content, index_buffer)


class Texture:

    def __init__(self, size: Tuple[(int, int)], component: int, data):
        self.width, self.height = size
        sized_format = (gl.GL_R8, gl.GL_RG8, gl.GL_RGB8, gl.GL_RGBA8)[(component - 1)]
        self.format = (gl.GL_R, gl.GL_RG, gl.GL_RGB, gl.GL_RGBA)[(component - 1)]
        gl.glActiveTexture(gl.GL_TEXTURE0 + 0)
        self.texture_id = texture_id = gl.GLuint()
        gl.glGenTextures(1, byref(self.texture_id))
        if self.texture_id.value == 0:
            raise ShaderException('Cannot create Texture.')
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)
        gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        try:
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, sized_format, self.width, self.height, 0, self.format, gl.GL_UNSIGNED_BYTE, data)
        except gl.GLException:
            raise gl.GLException(f"Unable to create texture. {gl.GL_MAX_TEXTURE_SIZE} {size}")

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        weakref.finalize(self, Texture.release, texture_id)

    @staticmethod
    def release(texture_id):
        if gl.current_context is None:
            return
        if texture_id.value != 0:
            gl.glDeleteTextures(1, byref(texture_id))

    def use(self, texture_unit: int=0):
        gl.glActiveTexture(gl.GL_TEXTURE0 + texture_unit)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)


def texture(size: Tuple[(int, int)], component: int, data) -> Texture:
    return Texture(size, component, data)