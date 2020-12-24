# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/watermark.py
# Compiled at: 2019-12-20 07:09:55
# Size of source mod 2**32: 3936 bytes
"""PyAMS_file.watermark module

This module is used to add watermarks to images.
"""
import os.path
from io import BytesIO, StringIO
from PIL import Image, ImageEnhance
from pyams_file.interfaces import IImageFile
from pyams_file.interfaces.thumbnail import IWatermarker
from pyams_utils.registry import utility_config
__docformat__ = 'restructuredtext'

@utility_config(provides=IWatermarker)
class ImageWatermarker:
    __doc__ = 'Image watermarker utility'

    @staticmethod
    def _reduce_opacity(image, opacity):
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

    def add_watermark(self, image, watermark, position='scale', opacity=1, format=None):
        """Adds a watermark to an image and return a new image"""
        if IImageFile.providedBy(image):
            image = image.data
        if isinstance(image, bytes):
            image = BytesIO(image)
        elif isinstance(image, str) and not os.path.exists(image):
            image = StringIO(image)
        image = Image.open(image)
        if not format:
            format = image.format
        format = format.upper()
        if format not in ('GIF', 'JPEG', 'PNG'):
            format = 'JPEG'
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        if isinstance(watermark, str) and os.path.exists(watermark):
            watermark = Image.open(watermark)
        else:
            if IImageFile.providedBy(watermark):
                watermark = Image.open(StringIO(watermark.data))
            else:
                watermark = Image.open(watermark)
            if opacity < 1:
                watermark = self._reduce_opacity(watermark, opacity)
            layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
            if position == 'tile':
                for y in range(0, image.size[1], watermark.size[1]):
                    for x in range(0, image.size[0], watermark.size[0]):
                        layer.paste(watermark, (x, y))

            else:
                if position == 'scale':
                    ratio = min(float(image.size[0]) / watermark.size[0], float(image.size[1]) / watermark.size[1])
                    w = int(watermark.size[0] * ratio)
                    h = int(watermark.size[1] * ratio)
                    watermark = watermark.resize((w, h))
                    layer.paste(watermark, (int((image.size[0] - w) / 2), int((image.size[1] - h) / 2)))
                else:
                    layer.paste(watermark, position)
        new = BytesIO()
        composite = Image.composite(layer, image, layer)
        if format == 'JPEG':
            composite = composite.convert('RGB')
        composite.save(new, format)
        return (new.getvalue(), format.lower())