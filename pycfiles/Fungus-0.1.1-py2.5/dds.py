# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/image/codecs/dds.py
# Compiled at: 2009-02-07 06:48:49
"""DDS texture loader.

Reference: http://msdn2.microsoft.com/en-us/library/bb172993.aspx
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: dds.py 1579 2008-01-15 14:47:19Z Alex.Holkner $'
from ctypes import *
import struct
from pyglet.gl import *
from pyglet.gl import gl_info
from pyglet.image import CompressedImageData
from pyglet.image import codecs
from pyglet.image.codecs import s3tc

class DDSException(codecs.ImageDecodeException):
    pass


DDSD_CAPS = 1
DDSD_HEIGHT = 2
DDSD_WIDTH = 4
DDSD_PITCH = 8
DDSD_PIXELFORMAT = 4096
DDSD_MIPMAPCOUNT = 131072
DDSD_LINEARSIZE = 524288
DDSD_DEPTH = 8388608
DDPF_ALPHAPIXELS = 1
DDPF_FOURCC = 4
DDPF_RGB = 64
DDSCAPS_COMPLEX = 8
DDSCAPS_TEXTURE = 4096
DDSCAPS_MIPMAP = 4194304
DDSCAPS2_CUBEMAP = 512
DDSCAPS2_CUBEMAP_POSITIVEX = 1024
DDSCAPS2_CUBEMAP_NEGATIVEX = 2048
DDSCAPS2_CUBEMAP_POSITIVEY = 4096
DDSCAPS2_CUBEMAP_NEGATIVEY = 8192
DDSCAPS2_CUBEMAP_POSITIVEZ = 16384
DDSCAPS2_CUBEMAP_NEGATIVEZ = 32768
DDSCAPS2_VOLUME = 2097152

class _filestruct(object):

    def __init__(self, data):
        if len(data) < self.get_size():
            raise DDSException('Not a DDS file')
        items = struct.unpack(self.get_format(), data)
        for (field, value) in map(None, self._fields, items):
            setattr(self, field[0], value)

        return

    def __repr__(self):
        name = self.__class__.__name__
        return '%s(%s)' % (
         name,
         (', \n%s' % (' ' * (len(name) + 1))).join([ '%s = %s' % (field[0], repr(getattr(self, field[0]))) for field in self._fields
                                          ]))

    @classmethod
    def get_format(cls):
        return '<' + ('').join([ f[1] for f in cls._fields ])

    @classmethod
    def get_size(cls):
        return struct.calcsize(cls.get_format())


class DDSURFACEDESC2(_filestruct):
    _fields = [
     ('dwMagic', '4s'),
     ('dwSize', 'I'),
     ('dwFlags', 'I'),
     ('dwHeight', 'I'),
     ('dwWidth', 'I'),
     ('dwPitchOrLinearSize', 'I'),
     ('dwDepth', 'I'),
     ('dwMipMapCount', 'I'),
     ('dwReserved1', '44s'),
     ('ddpfPixelFormat', '32s'),
     ('dwCaps1', 'I'),
     ('dwCaps2', 'I'),
     ('dwCapsReserved', '8s'),
     ('dwReserved2', 'I')]

    def __init__(self, data):
        super(DDSURFACEDESC2, self).__init__(data)
        self.ddpfPixelFormat = DDPIXELFORMAT(self.ddpfPixelFormat)


class DDPIXELFORMAT(_filestruct):
    _fields = [
     ('dwSize', 'I'),
     ('dwFlags', 'I'),
     ('dwFourCC', '4s'),
     ('dwRGBBitCount', 'I'),
     ('dwRBitMask', 'I'),
     ('dwGBitMask', 'I'),
     ('dwBBitMask', 'I'),
     ('dwRGBAlphaBitMask', 'I')]


_compression_formats = {('DXT1', False): (
                   GL_COMPRESSED_RGB_S3TC_DXT1_EXT, s3tc.decode_dxt1_rgb), 
   ('DXT1', True): (
                  GL_COMPRESSED_RGBA_S3TC_DXT1_EXT, s3tc.decode_dxt1_rgba), 
   ('DXT3', False): (
                   GL_COMPRESSED_RGBA_S3TC_DXT3_EXT, s3tc.decode_dxt3), 
   ('DXT3', True): (
                  GL_COMPRESSED_RGBA_S3TC_DXT3_EXT, s3tc.decode_dxt3), 
   ('DXT5', False): (
                   GL_COMPRESSED_RGBA_S3TC_DXT5_EXT, s3tc.decode_dxt5), 
   ('DXT5', True): (
                  GL_COMPRESSED_RGBA_S3TC_DXT5_EXT, s3tc.decode_dxt5)}

def _check_error():
    e = glGetError()
    if e != 0:
        print 'GL error %d' % e


class DDSImageDecoder(codecs.ImageDecoder):

    def get_file_extensions(self):
        return [
         '.dds']

    def decode(self, file, filename):
        header = file.read(DDSURFACEDESC2.get_size())
        desc = DDSURFACEDESC2(header)
        if desc.dwMagic != 'DDS ' or desc.dwSize != 124:
            raise DDSException('Invalid DDS file (incorrect header).')
        width = desc.dwWidth
        height = desc.dwHeight
        compressed = False
        volume = False
        mipmaps = 1
        if desc.dwFlags & DDSD_PITCH:
            pitch = desc.dwPitchOrLinearSize
        elif desc.dwFlags & DDSD_LINEARSIZE:
            image_size = desc.dwPitchOrLinearSize
            compressed = True
        if desc.dwFlags & DDSD_DEPTH:
            raise DDSException('Volume DDS files unsupported')
            volume = True
            depth = desc.dwDepth
        if desc.dwFlags & DDSD_MIPMAPCOUNT:
            mipmaps = desc.dwMipMapCount
        if desc.ddpfPixelFormat.dwSize != 32:
            raise DDSException('Invalid DDS file (incorrect pixel format).')
        if desc.dwCaps2 & DDSCAPS2_CUBEMAP:
            raise DDSException('Cubemap DDS files unsupported')
        if not desc.ddpfPixelFormat.dwFlags & DDPF_FOURCC:
            raise DDSException('Uncompressed DDS textures not supported.')
        has_alpha = desc.ddpfPixelFormat.dwRGBAlphaBitMask != 0
        format = None
        (format, decoder) = _compression_formats.get((
         desc.ddpfPixelFormat.dwFourCC, has_alpha), None)
        if not format:
            raise DDSException('Unsupported texture compression %s' % desc.ddpfPixelFormat.dwFourCC)
        if format == GL_COMPRESSED_RGB_S3TC_DXT1_EXT:
            block_size = 8
        else:
            block_size = 16
        datas = []
        w, h = width, height
        for i in range(mipmaps):
            if not w and not h:
                break
            if not w:
                w = 1
            if not h:
                h = 1
            size = (w + 3) / 4 * ((h + 3) / 4) * block_size
            data = file.read(size)
            datas.append(data)
            w >>= 1
            h >>= 1

        image = CompressedImageData(width, height, format, datas[0], 'GL_EXT_texture_compression_s3tc', decoder)
        level = 0
        for data in datas[1:]:
            level += 1
            image.set_mipmap_data(level, data)

        return image


def get_decoders():
    return [
     DDSImageDecoder()]


def get_encoders():
    return []