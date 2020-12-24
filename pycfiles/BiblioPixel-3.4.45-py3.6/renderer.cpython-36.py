# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/image/renderer.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1438 bytes
from ...util import log
from ...layout import matrix, strip

def renderer(layout, color, pixel_width, pixel_height, ellipse, vertical, frame, padding):
    if not isinstance(layout, (matrix.Matrix, strip.Strip)):
        raise ValueError('Cannot render a layout of type %s' % type(layout))
    else:
        from PIL import Image, ImageDraw
        shape = layout.shape
        if len(shape) == 1:
            if vertical:
                shape, getter = (
                 1, shape[0]), lambda x, y: layout.get(y)
            else:
                shape, getter = (
                 shape[0], 1), lambda x, y: layout.get(x)
        else:
            getter = layout.get
    width, height = shape
    pw, ph = pixel_width, pixel_width
    ph = pw if ph is None else ph
    cw, ch = pw + 2 * padding, ph + 2 * padding
    image_size = (2 * frame + width * cw, 2 * frame + height * ch)

    def render():
        image = Image.new('RGB', image_size, color)
        draw = ImageDraw.Draw(image)
        draw_pixel = draw.ellipse if ellipse else draw.rectangle
        offset = frame + padding
        for x in range(width):
            px = offset + x * cw
            for y in range(height):
                py = offset + y * ch
                pcolor = tuple(int(i) for i in getter(x, y))
                draw_pixel((px, py, px + pw, py + ph), pcolor, pcolor)

        return image

    return render