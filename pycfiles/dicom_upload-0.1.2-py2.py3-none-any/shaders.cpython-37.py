# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/opengl/shaders.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 16009 bytes
try:
    from OpenGL import NullFunctionError
except ImportError:
    from OpenGL.error import NullFunctionError

from OpenGL.GL import *
from OpenGL.GL import shaders
import re

def initShaders():
    global Shaders
    Shaders = [ShaderProgram(None, []),
     ShaderProgram('balloon', [
      VertexShader('\n                varying vec3 normal;\n                void main() {\n                    // compute here for use in fragment shader\n                    normal = normalize(gl_NormalMatrix * gl_Normal);\n                    gl_FrontColor = gl_Color;\n                    gl_BackColor = gl_Color;\n                    gl_Position = ftransform();\n                }\n            '),
      FragmentShader('\n                varying vec3 normal;\n                void main() {\n                    vec4 color = gl_Color;\n                    color.w = min(color.w + 2.0 * color.w * pow(normal.x*normal.x + normal.y*normal.y, 5.0), 1.0);\n                    gl_FragColor = color;\n                }\n            ')]),
     ShaderProgram('viewNormalColor', [
      VertexShader('\n                varying vec3 normal;\n                void main() {\n                    // compute here for use in fragment shader\n                    normal = normalize(gl_NormalMatrix * gl_Normal);\n                    gl_FrontColor = gl_Color;\n                    gl_BackColor = gl_Color;\n                    gl_Position = ftransform();\n                }\n            '),
      FragmentShader('\n                varying vec3 normal;\n                void main() {\n                    vec4 color = gl_Color;\n                    color.x = (normal.x + 1.0) * 0.5;\n                    color.y = (normal.y + 1.0) * 0.5;\n                    color.z = (normal.z + 1.0) * 0.5;\n                    gl_FragColor = color;\n                }\n            ')]),
     ShaderProgram('normalColor', [
      VertexShader('\n                varying vec3 normal;\n                void main() {\n                    // compute here for use in fragment shader\n                    normal = normalize(gl_Normal);\n                    gl_FrontColor = gl_Color;\n                    gl_BackColor = gl_Color;\n                    gl_Position = ftransform();\n                }\n            '),
      FragmentShader('\n                varying vec3 normal;\n                void main() {\n                    vec4 color = gl_Color;\n                    color.x = (normal.x + 1.0) * 0.5;\n                    color.y = (normal.y + 1.0) * 0.5;\n                    color.z = (normal.z + 1.0) * 0.5;\n                    gl_FragColor = color;\n                }\n            ')]),
     ShaderProgram('shaded', [
      VertexShader('\n                varying vec3 normal;\n                void main() {\n                    // compute here for use in fragment shader\n                    normal = normalize(gl_NormalMatrix * gl_Normal);\n                    gl_FrontColor = gl_Color;\n                    gl_BackColor = gl_Color;\n                    gl_Position = ftransform();\n                }\n            '),
      FragmentShader('\n                varying vec3 normal;\n                void main() {\n                    float p = dot(normal, normalize(vec3(1.0, -1.0, -1.0)));\n                    p = p < 0. ? 0. : p * 0.8;\n                    vec4 color = gl_Color;\n                    color.x = color.x * (0.2 + p);\n                    color.y = color.y * (0.2 + p);\n                    color.z = color.z * (0.2 + p);\n                    gl_FragColor = color;\n                }\n            ')]),
     ShaderProgram('edgeHilight', [
      VertexShader('\n                varying vec3 normal;\n                void main() {\n                    // compute here for use in fragment shader\n                    normal = normalize(gl_NormalMatrix * gl_Normal);\n                    gl_FrontColor = gl_Color;\n                    gl_BackColor = gl_Color;\n                    gl_Position = ftransform();\n                }\n            '),
      FragmentShader('\n                varying vec3 normal;\n                void main() {\n                    vec4 color = gl_Color;\n                    float s = pow(normal.x*normal.x + normal.y*normal.y, 2.0);\n                    color.x = color.x + s * (1.0-color.x);\n                    color.y = color.y + s * (1.0-color.y);\n                    color.z = color.z + s * (1.0-color.z);\n                    gl_FragColor = color;\n                }\n            ')]),
     ShaderProgram('heightColor', [
      VertexShader('\n                varying vec4 pos;\n                void main() {\n                    gl_FrontColor = gl_Color;\n                    gl_BackColor = gl_Color;\n                    pos = gl_Vertex;\n                    gl_Position = ftransform();\n                }\n            '),
      FragmentShader('\n                uniform float colorMap[9];\n                varying vec4 pos;\n                //out vec4 gl_FragColor;   // only needed for later glsl versions\n                //in vec4 gl_Color;\n                void main() {\n                    vec4 color = gl_Color;\n                    color.x = colorMap[0] * (pos.z + colorMap[1]);\n                    if (colorMap[2] != 1.0)\n                        color.x = pow(color.x, colorMap[2]);\n                    color.x = color.x < 0. ? 0. : (color.x > 1. ? 1. : color.x);\n                    \n                    color.y = colorMap[3] * (pos.z + colorMap[4]);\n                    if (colorMap[5] != 1.0)\n                        color.y = pow(color.y, colorMap[5]);\n                    color.y = color.y < 0. ? 0. : (color.y > 1. ? 1. : color.y);\n                    \n                    color.z = colorMap[6] * (pos.z + colorMap[7]);\n                    if (colorMap[8] != 1.0)\n                        color.z = pow(color.z, colorMap[8]);\n                    color.z = color.z < 0. ? 0. : (color.z > 1. ? 1. : color.z);\n                    \n                    color.w = 1.0;\n                    gl_FragColor = color;\n                }\n            ')],
       uniforms={'colorMap': [1, 1, 1, 1, 0.5, 1, 1, 0, 1]}),
     ShaderProgram('pointSprite', [
      VertexShader('\n                void main() {\n                    gl_FrontColor=gl_Color;\n                    gl_PointSize = gl_Normal.x;\n                    gl_Position = ftransform();\n                } \n            ')])]


CompiledShaderPrograms = {}

def getShaderProgram(name):
    return ShaderProgram.names[name]


class Shader(object):

    def __init__(self, shaderType, code):
        self.shaderType = shaderType
        self.code = code
        self.compiled = None

    def shader(self):
        if self.compiled is None:
            try:
                self.compiled = shaders.compileShader(self.code, self.shaderType)
            except NullFunctionError:
                raise Exception('This OpenGL implementation does not support shader programs; many OpenGL features in pyqtgraph will not work.')
            except RuntimeError as exc:
                try:
                    if len(exc.args) == 3:
                        err, code, typ = exc.args
                        if not err.startswith('Shader compile failure'):
                            raise
                        code = code[0].decode('utf_8').split('\n')
                        err, c, msgs = err.partition(':')
                        err = err + '\n'
                        msgs = re.sub("b'", '', msgs)
                        msgs = re.sub("'$", '', msgs)
                        msgs = re.sub('\\\\n', '\n', msgs)
                        msgs = msgs.split('\n')
                        errNums = [()] * len(code)
                        for i, msg in enumerate(msgs):
                            msg = msg.strip()
                            if msg == '':
                                continue
                            m = re.match('(\\d+\\:)?\\d+\\((\\d+)\\)', msg)
                            if m is not None:
                                line = int(m.groups()[1])
                                errNums[line - 1] = errNums[(line - 1)] + (str(i + 1),)
                            err = err + '%d %s\n' % (i + 1, msg)

                        errNums = [','.join(n) for n in errNums]
                        maxlen = max(map(len, errNums))
                        code = [errNums[i] + ' ' * (maxlen - len(errNums[i])) + line for i, line in enumerate(code)]
                        err = err + '\n'.join(code)
                        raise Exception(err)
                    else:
                        raise
                finally:
                    exc = None
                    del exc

        return self.compiled


class VertexShader(Shader):

    def __init__(self, code):
        Shader.__init__(self, GL_VERTEX_SHADER, code)


class FragmentShader(Shader):

    def __init__(self, code):
        Shader.__init__(self, GL_FRAGMENT_SHADER, code)


class ShaderProgram(object):
    names = {}

    def __init__(self, name, shaders, uniforms=None):
        self.name = name
        ShaderProgram.names[name] = self
        self.shaders = shaders
        self.prog = None
        self.blockData = {}
        self.uniformData = {}
        if uniforms is not None:
            for k, v in uniforms.items():
                self[k] = v

    def setBlockData(self, blockName, data):
        if data is None:
            del self.blockData[blockName]
        else:
            self.blockData[blockName] = data

    def setUniformData(self, uniformName, data):
        if data is None:
            del self.uniformData[uniformName]
        else:
            self.uniformData[uniformName] = data

    def __setitem__(self, item, val):
        self.setUniformData(item, val)

    def __delitem__(self, item):
        self.setUniformData(item, None)

    def program(self):
        if self.prog is None:
            try:
                compiled = [s.shader() for s in self.shaders]
                self.prog = (shaders.compileProgram)(*compiled)
            except:
                self.prog = -1
                raise

        return self.prog

    def __enter__(self):
        if len(self.shaders) > 0:
            if self.program() != -1:
                glUseProgram(self.program())
                try:
                    for uniformName, data in self.uniformData.items():
                        loc = self.uniform(uniformName)
                        if loc == -1:
                            raise Exception('Could not find uniform variable "%s"' % uniformName)
                        glUniform1fv(loc, len(data), data)

                except:
                    glUseProgram(0)
                    raise

    def __exit__(self, *args):
        if len(self.shaders) > 0:
            glUseProgram(0)

    def uniform(self, name):
        """Return the location integer for a uniform variable in this program"""
        return glGetUniformLocation(self.program(), name.encode('utf_8'))


class HeightColorShader(ShaderProgram):

    def __enter__(self):
        bindPoint = 1
        blockIndex = glGetUniformBlockIndex(self.program(), 'blockName')
        glUniformBlockBinding(self.program(), blockIndex, bindPoint)
        buf = glGenBuffers(1)
        glBindBuffer(GL_UNIFORM_BUFFER, buf)
        glBufferData(GL_UNIFORM_BUFFER, size, data, GL_DYNAMIC_DRAW)
        glBindBufferBase(GL_UNIFORM_BUFFER, bindPoint, buf)


initShaders()