# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fei/Development/gibsonv2/gibson2/core/render/mesh_renderer/glutils/utils.py
# Compiled at: 2020-03-24 04:06:03
from PIL import Image
import numpy as np, OpenGL.GL as GL
colormap = [
 [
  1, 0, 0], [0, 1, 0], [0, 0, 1]]

def loadTexture(path, scale=1):
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
    w, h = img.size
    img = img.resize((int(w * scale), int(h * scale)), Image.BICUBIC)
    img_data = np.frombuffer(img.tobytes(), np.uint8)
    width, height = img.size
    texture = GL.glGenTextures(1)
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, img_data)
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
    return texture