# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tgcaptcha/plugins/image/mcdermott.py
# Compiled at: 2007-05-31 01:58:59
import random, Image, ImageFont, ImageDraw, ImageFilter
from pkg_resources import resource_filename
import os.path
from turbogears import config
font_path = config.get('tgcaptcha.plugin.mcdermott.font_path')
if not font_path:
    font_path = os.path.abspath(resource_filename('tgcaptcha', 'static/fonts/tuffy/Tuffy.ttf'))
assert os.path.exists(font_path), 'The font_path "%s" does not exist' % (font_path,)
font_size = int(config.get('tgcaptcha.plugin.mcdermott.font_size', 36))

def generate_jpeg(text, file_obj):
    """Generate a captcha image"""
    fgcolor = random.randint(0, 16776960)
    bgcolor = fgcolor ^ 16777215
    font = ImageFont.truetype(font_path, font_size)
    dim = font.getsize(text)
    im = Image.new('RGB', (dim[0] + 5, dim[1] + 5), bgcolor)
    d = ImageDraw.Draw(im)
    (x, y) = im.size
    r = random.randint
    for num in range(100):
        d.rectangle((r(0, x), r(0, y), r(0, x), r(0, y)), fill=r(0, 16777215))

    d.text((3, 3), text, font=font, fill=fgcolor)
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    im.save(file_obj, format='JPEG')