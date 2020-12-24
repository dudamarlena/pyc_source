# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/convert360/projector.py
# Compiled at: 2017-09-19 05:57:09
# Size of source mod 2**32: 7266 bytes
import numpy as np
from OpenGL import GL
from OpenGL import GLU
from OpenGL import GLUT
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

def tex_from_array(img_data):
    img_data_array = np.asarray(img_data)
    sx, sy = img_data_array.shape[:2]
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, sy, sx, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, img_data_array)


PLAIN_VERTEX_SHADER = '\n#version 120\nattribute vec3 position;\nattribute vec2 texCoord;\nvarying vec2 texCoordOut;\nvoid main()\n{\n    gl_Position = vec4(position, 1.0);\n    texCoordOut = texCoord;\n} '
CUBEMAP_FRAGMENT_SHADER = '\n#version 120\n#define M_PI 3.141592653589\n\nvarying vec2 texCoordOut;\nuniform sampler2D BaseImage;\nuniform bool connected;\n\nvec2 flatToSpherical(vec3 flatCoord, float r)\n{\n  return vec2(\n      atan(flatCoord.y, flatCoord.x),\n      acos(flatCoord.z / r));\n}\n\nmat3 constructCompleteRotation(vec3 a)\n{\n  return mat3(\n      cos(a.x) * cos(a.z) - sin(a.x) * cos(a.y) * sin(a.z),\n      -cos(a.x) * sin(a.z) - sin(a.x) * cos(a.y) * cos(a.z),\n      sin(a.x) * sin(a.y),\n      sin(a.x) * cos(a.z) + cos(a.x) * cos(a.y) * sin(a.z),\n      -sin(a.x) * sin(a.z) + cos(a.x) * cos(a.y) * cos(a.z),\n      -cos(a.x) * sin(a.y),\n      sin(a.y) * sin(a.z),\n      sin(a.y) * cos(a.z),\n      cos(a.y));\n}\n\nint get_face(vec2 uv){\n  int x = int(floor(uv.x * 3.0));\n  int y = 1 - int(floor(uv.y * 2.0));\n  return y * 3 + x;\n}\n\nvoid main() {\n  vec2 uv = texCoordOut / 2.0 + 0.5;\n  vec2 faceCoord = uv * 2.0 - 1.0;\n  int face = get_face(uv);\n  vec3 latSphereCoord;\n  vec3 rot;\n\n  if(connected){\n    if(face == 0){\n        rot = vec3(-M_PI / 2.0, 0, 0);\n    }else if(face == 1){\n        rot = vec3(0, 0, 0);\n    }else if(face == 2){\n        rot = vec3(M_PI / 2.0, 0, 0);\n    }else if(face == 3){\n        rot = vec3(0.0, -M_PI / 2.0, M_PI / 2.0);\n    }else if(face == 4){\n        rot = vec3(0.0, -M_PI / 2.0, M_PI);\n    }else if(face == 5){\n        rot = vec3(0.0, -M_PI / 2.0, M_PI * 3.0 / 2.0);\n    }\n  }else{\n    if(face == 0){\n        rot = vec3(-M_PI / 2.0, 0, 0);\n    }else if(face == 1){\n        rot = vec3(M_PI / 2.0, 0, 0);\n    }else if(face == 2){\n        rot = vec3(M_PI / 2.0, M_PI / 2.0, M_PI / 2.0);\n    }else if(face == 3){\n        rot = vec3(M_PI / 2.0, -M_PI / 2.0, M_PI / 2.0);\n    }else if(face == 4){\n        rot = vec3(M_PI, 0, 0);\n    }else if(face == 5){\n        rot = vec3(0, 0, 0);\n    }\n  }\n\n  latSphereCoord = vec3(1.0,\n                        faceCoord.x * 3.0 + 2.0 - float(mod(face, 3)) * 2.0,\n                        faceCoord.y * 2.0 - 1.0 + float(face / 3) * 2.0);\n\n  float r = sqrt(latSphereCoord.x * latSphereCoord.x +\n                latSphereCoord.y * latSphereCoord.y +\n                latSphereCoord.z * latSphereCoord.z);\n\n  vec3 rotatedCoord = latSphereCoord * constructCompleteRotation(rot);\n  vec2 invRotatedSphericalCoord = flatToSpherical(rotatedCoord, r);\n\n  vec2 finalCoordenates;\n  finalCoordenates.x = (invRotatedSphericalCoord.x) / (2.0 * M_PI);\n  finalCoordenates.y = (invRotatedSphericalCoord.y) / (M_PI);\n\n  gl_FragColor = texture2D(BaseImage, mod(finalCoordenates, 1.0));\n} '

class Equirectangular2Cubemap:

    def __init__(self, size=(1200, 900), connected=False):
        self.size = size
        self.connected = connected
        GLUT.glutInit([])
        GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
        (GLUT.glutInitWindowSize)(*size)
        GLUT.glutInitWindowPosition(0, 0)
        GLUT.glutCreateWindow('Render')
        self.vertex_shader = shaders.compileShader(PLAIN_VERTEX_SHADER, GL.GL_VERTEX_SHADER)
        self.fragment_shader = shaders.compileShader(CUBEMAP_FRAGMENT_SHADER, GL.GL_FRAGMENT_SHADER)

    def create_texture(self):
        self.texture = GL.glGenTextures(1)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glUseProgram(self.shader)
        self.index_positions.bind()
        self.vertexPositions.bind()
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 20, None)
        GL.glVertexAttribPointer(1, 2, GL.GL_FLOAT, False, 20, GLU.ctypes.c_void_p(12))
        GL.glEnable(GL.GL_TEXTURE_2D)

    def render(self, frame):
        tex_from_array(frame)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)

    def render_to_image(self, frame):
        self.render(frame)
        buff = GL.glReadPixels(0, 0, self.size[0], self.size[1], GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        image_array = np.fromstring(buff, np.uint8)
        image = image_array.reshape(self.size[1], self.size[0], 3)
        return np.flipud(image)

    def __enter__(self):
        vertices = np.array([
         [
          1, 1, 0, 1, 1],
         [
          1, -1, 0, 1, -1],
         [
          -1, -1, 0, -1, -1],
         [
          -1, 1, 0, -1, 1]],
          dtype='f')
        self.vertexPositions = vbo.VBO(vertices)
        indices = np.array([[0, 1, 2], [0, 2, 3]], dtype=(np.int32))
        self.index_positions = vbo.VBO(indices, target=(GL.GL_ELEMENT_ARRAY_BUFFER))
        self.shader = shaders.compileProgram(self.vertex_shader, self.fragment_shader)
        self.create_texture()
        uConnectedLoc = GL.glGetUniformLocation(self.shader, 'connected')
        GL.glUniform1i(uConnectedLoc, 1 if self.connected else 0)
        return self

    def __exit__(self, type, value, traceback):
        self.clean()

    def clean(self):
        self.vertexPositions.delete()
        self.index_positions.delete()


class Equirectangular2ConnectedCubemap(Equirectangular2Cubemap):

    def __init__(self, size=(1200, 900)):
        super(Equirectangular2ConnectedCubemap, self).__init__(size, connected=True)


class ProjectorNotImplemented(Exception):
    pass


projectors = {'equirectangular': {'cubemap':Equirectangular2Cubemap, 
                     'connected-cubemap':Equirectangular2ConnectedCubemap}}

def get_projector(from_type, to_type):
    if from_type in projectors:
        if to_type in projectors[from_type]:
            return projectors[from_type][to_type]
    message = 'Projetor from %s to %s was not implemented' % (from_type,
     to_type)
    raise ProjectorNotImplemented(message)