# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\cocos\wired.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 2435 bytes
from __future__ import division, print_function, unicode_literals
from cocos.shader import ShaderProgram, VertexShader, FragmentShader
__all__ = [
 'wired']
test_v = '\nvarying vec3 position;\nvoid main()\n{\n  gl_Position = ftransform();\n  position = gl_Position.xyz;\n}\n'
test_f = '\nuniform vec4 color;\nvoid main()\n{\n    gl_FragColor = color;\n}\n'

def load_shader():
    s = ShaderProgram()
    s.setShader(FragmentShader('test_f', test_f))
    return s


wired = load_shader()