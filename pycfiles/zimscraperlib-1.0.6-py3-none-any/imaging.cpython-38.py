# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/bt/ctdt6vrj33n8yhzhpvyfy53h0000gn/T/pip-unpacked-wheel-a7yo76wc/zimscraperlib/imaging.py
# Compiled at: 2020-05-05 04:38:33
# Size of source mod 2**32: 2753 bytes
import re, colorsys, PIL, colorthief
from resizeimage import resizeimage

def get_colors(image_path, use_palette=True):
    """ (main, secondary) HTML color codes from an image path """

    def rgb_to_hex(r, g, b):
        """ hexadecimal HTML-friendly color code for RGB tuple """
        return ('#{}{}{}'.format)(*[str(hex(x)[2:]).zfill(2) for x in (r, g, b)]).upper()

    def solarize(r, g, b):
        h, l, s = colorsys.rgb_to_hls(float(r) / 256, float(g) / 256, float(b) / 256)
        r2, g2, b2 = [int(x * 256) for x in colorsys.hls_to_rgb(h, 0.95, s)]
        return (r2, g2, b2)

    ct = colorthief.ColorThief(image_path)
    if use_palette:
        palette = ct.get_palette(color_count=2, quality=1)
        mr, mg, mb = palette[0]
        sr, sg, sb = solarize(*palette[1])
    else:
        mr, mg, mb = ct.get_color(quality=1)
        sr, sg, sb = solarize(mr, mg, mb)
    return (rgb_to_hex(mr, mg, mb), rgb_to_hex(sr, sg, sb))


def resize_image(fpath, width, height=None, to=None, method='width'):
    """ resize an image file (dimensions)

        methods: width, height, cover """
    with open(str(fpath), 'rb') as (fp):
        with PIL.Image.open(fp) as (image):
            if method == 'width':
                resized = resizeimage.resize(method, image, width)
            else:
                if method == 'height':
                    resized = resizeimage.resize(method, image, height)
                else:
                    resized = resizeimage.resize(method, image, [width, height])
    kwargs = {'JPEG':{'quality': 100}, 
     'PNG':{}}
    (resized.save)(
     (str(to) if to is not None else fpath), (image.format), **kwargs.get(image.format))


def is_hex_color(text):
    """ whether supplied text is a valid hex-formated color code """
    return re.search('^#(?:[0-9a-fA-F]{3}){1,2}$', text)


def create_favicon(source_image, dest_ico):
    """ generate a squared favicon from a source image """
    if dest_ico.suffix != '.ico':
        raise ValueError('favicon extension must be ICO')
    img = PIL.Image.open(source_image)
    w, h = img.size
    if w != h:
        size = min([w, h])
        resized = dest_ico.parent.joinpath(f"{source_image.stem}.tmp.{source_image.suffix}")
        resize_image(source_image, size, size, resized, 'contain')
        img = PIL.Image.open(resized)
    img.save(str(dest_ico))