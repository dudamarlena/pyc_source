# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/pil.py
# Compiled at: 2014-01-03 04:21:11
from cStringIO import StringIO
from PIL import Image, ImageFilter, ImageEnhance
from zope.app.file.interfaces import IImage
from ztfy.file.interfaces import IThumbnailer, IThumbnailGeometry, IWatermarker, DEFAULT_DISPLAYS
from zope.interface import implements

class PILThumbnailer(object):
    """PIL thumbnailer utility"""
    implements(IThumbnailer)
    order = 50

    def createThumbnail(self, image, size, format=None):
        if IImage.providedBy(image):
            image = image.data
        image = Image.open(StringIO(image))
        if not format:
            format = image.format
        format = format.upper()
        if format not in ('GIF', 'JPEG', 'PNG'):
            format = 'JPEG'
        if image.mode == 'P':
            image = image.convert('RGBA')
        new = StringIO()
        image.resize(size, Image.ANTIALIAS).filter(ImageFilter.SHARPEN).save(new, format)
        return (new.getvalue(), format.lower())

    def createSquareThumbnail(self, image, size, source=None, format=None):
        if IImage.providedBy(image):
            img = image.data
        else:
            img = image
        img = Image.open(StringIO(img))
        if not format:
            format = img.format
        format = format.upper()
        if format not in ('GIF', 'JPEG', 'PNG'):
            format = 'JPEG'
        if img.mode == 'P':
            img = img.convert('RGBA')
        img_width, img_height = img.size
        thu_width, thu_height = size, size
        ratio = max(img_width * 1.0 / thu_width, img_height * 1.0 / thu_height)
        if source:
            x, y, w, h = source
        else:
            geometry = IThumbnailGeometry(image, None)
            if geometry is None:
                x, y, w, h = (
                 0, 0, img_width, img_height)
            else:
                (x, y), (w, h) = geometry.position, geometry.size
        box = (
         int(x * ratio), int(y * ratio), int((x + w) * ratio), int((y + h) * ratio))
        new = StringIO()
        img.crop(box).resize((
         DEFAULT_DISPLAYS['cthumb'], DEFAULT_DISPLAYS['cthumb']), Image.ANTIALIAS).filter(ImageFilter.SHARPEN).save(new, format)
        return (new.getvalue(), format.lower())


class PILWatermarker(object):
    """PIL watermarker utility"""
    implements(IWatermarker)
    order = 50

    def _reduce_opacity(self, image, opacity):
        """Returns an image with reduced opacity."""
        assert 0 <= opacity <= 1
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        else:
            image = image.copy()
        alpha = image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        image.putalpha(alpha)
        return image

    def addWatermark(self, image, mark, position='scale', opacity=1, format=None):
        """Adds a watermark to an image and return a new image"""
        if IImage.providedBy(image):
            image = image.data
        image = Image.open(StringIO(image))
        if not format:
            format = image.format
        format = format.upper()
        if format not in ('GIF', 'JPEG', 'PNG'):
            format = 'JPEG'
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        if IImage.providedBy(mark):
            mark = mark.data
        mark = Image.open(StringIO(mark))
        if opacity < 1:
            mark = self._reduce_opacity(mark, opacity)
        layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        if position == 'tile':
            for y in range(0, image.size[1], mark.size[1]):
                for x in range(0, image.size[0], mark.size[0]):
                    layer.paste(mark, (x, y))

        elif position == 'scale':
            ratio = min(float(image.size[0]) / mark.size[0], float(image.size[1]) / mark.size[1])
            w = int(mark.size[0] * ratio)
            h = int(mark.size[1] * ratio)
            mark = mark.resize((w, h))
            layer.paste(mark, ((image.size[0] - w) / 2, (image.size[1] - h) / 2))
        else:
            layer.paste(mark, position)
        new = StringIO()
        Image.composite(layer, image, layer).save(new, format)
        return (new.getvalue(), format.lower())