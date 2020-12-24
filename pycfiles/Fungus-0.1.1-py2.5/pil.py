# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/image/codecs/pil.py
# Compiled at: 2009-02-07 06:48:49
"""
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: pil.py 1768 2008-02-17 12:45:54Z Alex.Holkner $'
import os.path
from pyglet.gl import *
from pyglet.image import *
from pyglet.image.codecs import *
import Image

class PILImageDecoder(ImageDecoder):

    def get_file_extensions(self):
        return [
         '.bmp', '.cur', '.gif', '.ico', '.jpg', '.jpeg', '.pcx', '.png',
         '.tga', '.tif', '.tiff', '.xbm', '.xpm']

    def decode(self, file, filename):
        try:
            image = Image.open(file)
        except Exception, e:
            raise ImageDecodeException('PIL cannot read %r: %s' % (filename or file, e))

        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        if image.mode in ('1', 'P'):
            image = image.convert()
        if image.mode not in ('L', 'LA', 'RGB', 'RGBA'):
            raise ImageDecodeException('Unsupported mode "%s"' % image.mode)
        type = GL_UNSIGNED_BYTE
        (width, height) = image.size
        return ImageData(width, height, image.mode, image.tostring())


class PILImageEncoder(ImageEncoder):

    def get_file_extensions(self):
        return [
         '.bmp', '.eps', '.gif', '.jpg', '.jpeg',
         '.pcx', '.png', '.ppm', '.tiff', '.xbm']

    def encode(self, image, file, filename):
        pil_format = filename and os.path.splitext(filename)[1][1:] or 'png'
        if pil_format.lower() == 'jpg':
            pil_format = 'JPEG'
        image = image.get_image_data()
        format = image.format
        if format != 'RGB':
            format = 'RGBA'
        pitch = -(image.width * len(format))
        pil_image = Image.fromstring(format, (image.width, image.height), image.get_data(format, pitch))
        try:
            pil_image.save(file, pil_format)
        except Exception, e:
            raise ImageEncodeException(e)


def get_decoders():
    return [PILImageDecoder()]


def get_encoders():
    return [
     PILImageEncoder()]