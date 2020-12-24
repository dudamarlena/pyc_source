# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\openvr\color_cube_actor.py
# Compiled at: 2017-04-23 15:45:16
# Size of source mod 2**32: 3734 bytes
from textwrap import dedent
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from openvr.glframework import shader_string

class ColorCubeActor(object):
    __doc__ = '\n    Draws a cube\n    \n       2________ 3\n       /|      /|\n     6/_|____7/ |\n      | |_____|_| \n      | /0    | /1\n      |/______|/\n      4       5\n    '

    def __init__(self):
        self.shader = 0
        self.vao = None

    def init_gl(self):
        vertex_shader = compileShader(shader_string("\n            // Adapted from @jherico's RiftDemo.py in pyovr\n            \n            layout(location = 0) uniform mat4 Projection = mat4(1);\n            layout(location = 4) uniform mat4 ModelView = mat4(1);\n            layout(location = 8) uniform float Size = 0.3;\n            \n            // Minimum Y value is zero, so cube sits on the floor in room scale\n            const vec3 UNIT_CUBE[8] = vec3[8](\n              vec3(-1.0, -0.0, -1.0), // 0: lower left rear\n              vec3(+1.0, -0.0, -1.0), // 1: lower right rear\n              vec3(-1.0, +2.0, -1.0), // 2: upper left rear\n              vec3(+1.0, +2.0, -1.0), // 3: upper right rear\n              vec3(-1.0, -0.0, +1.0), // 4: lower left front\n              vec3(+1.0, -0.0, +1.0), // 5: lower right front\n              vec3(-1.0, +2.0, +1.0), // 6: upper left front\n              vec3(+1.0, +2.0, +1.0)  // 7: upper right front\n            );\n            \n            const vec3 UNIT_CUBE_NORMALS[6] = vec3[6](\n              vec3(0.0, 0.0, -1.0),\n              vec3(0.0, 0.0, 1.0),\n              vec3(1.0, 0.0, 0.0),\n              vec3(-1.0, 0.0, 0.0),\n              vec3(0.0, 1.0, 0.0),\n              vec3(0.0, -1.0, 0.0)\n            );\n            \n            const int CUBE_INDICES[36] = int[36](\n              0, 1, 2, 2, 1, 3, // front\n              4, 6, 5, 6, 5, 7, // back\n              0, 2, 4, 4, 2, 6, // left\n              1, 3, 5, 5, 3, 7, // right\n              2, 6, 3, 6, 3, 7, // top\n              0, 1, 4, 4, 1, 5  // bottom\n            );\n            \n            out vec3 _color;\n            \n            void main() {\n              _color = vec3(1.0, 0.0, 0.0);\n              int vertexIndex = CUBE_INDICES[gl_VertexID];\n              int normalIndex = gl_VertexID / 6;\n              \n              _color = UNIT_CUBE_NORMALS[normalIndex];\n              if (any(lessThan(_color, vec3(0.0)))) {\n                  _color = vec3(1.0) + _color;\n              }\n            \n              gl_Position = Projection * ModelView * vec4(UNIT_CUBE[vertexIndex] * Size, 1.0);\n            }\n            "), GL_VERTEX_SHADER)
        fragment_shader = compileShader(shader_string('\n            in vec3 _color;\n            out vec4 FragColor;\n            \n            void main() {\n              FragColor = vec4(_color, 1.0);\n            }\n            '), GL_FRAGMENT_SHADER)
        self.shader = compileProgram(vertex_shader, fragment_shader)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        glEnable(GL_DEPTH_TEST)

    def display_gl(self, modelview, projection):
        glUseProgram(self.shader)
        glUniformMatrix4fv(0, 1, False, projection)
        glUniformMatrix4fv(4, 1, False, modelview)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 36)

    def dispose_gl(self):
        glDeleteProgram(self.shader)
        self.shader = 0
        if self.vao:
            glDeleteVertexArrays(1, (self.vao,))
        self.vao = 0