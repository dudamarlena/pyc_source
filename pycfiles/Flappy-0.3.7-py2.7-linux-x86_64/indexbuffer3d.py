# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flappy/display3d/indexbuffer3d.py
# Compiled at: 2014-03-13 10:09:15
import struct
from flappy import _gl as gl

class IndexBuffer3D(object):

    def __init__(self, data=None):
        self.gl_buffer = gl.createBuffer()
        self.num_indeces = 0
        if data:
            self.upload(data)

    def __del__(self):
        gl.deleteBuffer(self.gl_buffer)

    def upload(self, data):
        ndata = struct.pack(('%sH' % len(data)), *data)
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, self.gl_buffer)
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, ndata, gl.STATIC_DRAW)
        self.num_indeces = len(data)