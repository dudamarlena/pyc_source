# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/image/codecs/png.py
# Compiled at: 2009-02-07 06:48:49
"""Encoder and decoder for PNG files, using PyPNG (pypng.py).
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: $'
import array
from pyglet.gl import *
from pyglet.image import *
from pyglet.image.codecs import *
import pyglet.image.codecs.pypng

class PNGImageDecoder(ImageDecoder):

    def get_file_extensions(self):
        return [
         '.png']

    def decode(self, file, filename):
        try:
            reader = pyglet.image.codecs.pypng.Reader(file=file)
            (width, height, pixels, metadata) = reader.read()
        except Exception, e:
            raise ImageDecodeException('PyPNG cannot read %r: %s' % (filename or file, e))

        if metadata['greyscale']:
            if metadata['has_alpha']:
                format = 'LA'
            else:
                format = 'L'
        elif metadata['has_alpha']:
            format = 'RGBA'
        else:
            format = 'RGB'
        pitch = len(format) * width
        return ImageData(width, height, format, pixels.tostring(), -pitch)


class PNGImageEncoder(ImageEncoder):

    def get_file_extensions(self):
        return [
         '.png']

    def encode(self, image, file, filename):
        image = image.get_image_data()
        has_alpha = 'A' in image.format
        greyscale = len(image.format) < 3
        if has_alpha:
            if greyscale:
                image.format = 'LA'
            else:
                image.format = 'RGBA'
        elif greyscale:
            image.format = 'L'
        else:
            image.format = 'RGB'
        image.pitch = -(image.width * len(image.format))
        writer = pyglet.image.codecs.pypng.Writer(image.width, image.height, bytes_per_sample=1, greyscale=greyscale, has_alpha=has_alpha)
        data = array.array('B')
        data.fromstring(image.data)
        writer.write_array(file, data)


def get_decoders():
    return [
     PNGImageDecoder()]


def get_encoders():
    return [
     PNGImageEncoder()]