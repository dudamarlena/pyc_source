# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nijel/weblate/weblate/weblate/fonts/utils.py
# Compiled at: 2020-03-12 04:44:12
# Size of source mod 2**32: 6344 bytes
"""Font handling wrapper."""
import os
from io import BytesIO
from tempfile import NamedTemporaryFile
import cairo, gi
from django.conf import settings
import django.core.cache as cache
from django.core.checks import Critical
from django.utils.html import escape
from PIL import ImageFont
from weblate.utils.data import data_dir
from weblate.utils.docs import get_doc_url
gi.require_version('PangoCairo', '1.0')
gi.require_version('Pango', '1.0')
from gi.repository import Pango, PangoCairo
FONTCONFIG_CONFIG = '<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n<fontconfig>\n    <cachedir>{}</cachedir>\n    <dir>{}</dir>\n    <dir>{}</dir>\n    <dir>{}</dir>\n    <dir>{}</dir>\n    <config>\n        <rescan>\n            <int>30</int>\n        </rescan>\n    </config>\n\n    <!--\n     Synthetic emboldening for fonts that do not have bold face available\n    -->\n    <match target="font">\n        <test name="weight" compare="less_eq">\n            <const>medium</const>\n        </test>\n        <test target="pattern" name="weight" compare="more_eq">\n            <const>bold</const>\n        </test>\n        <edit name="embolden" mode="assign">\n            <bool>true</bool>\n        </edit>\n        <edit name="weight" mode="assign">\n            <const>bold</const>\n        </edit>\n    </match>\n\n</fontconfig>\n'
FONT_WEIGHTS = {'normal':Pango.Weight.NORMAL, 
 'light':Pango.Weight.LIGHT, 
 'bold':Pango.Weight.BOLD, 
 '':None}

def configure_fontconfig():
    """Configures fontconfig to use custom configuration."""
    if getattr(configure_fontconfig, 'is_configured', False):
        return
    fonts_dir = data_dir('fonts')
    config_name = os.path.join(fonts_dir, 'fonts.conf')
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
    with open(config_name, 'w') as (handle):
        handle.write(FONTCONFIG_CONFIG.format(data_dir('cache', 'fonts'), fonts_dir, os.path.join(settings.STATIC_ROOT, 'font-source', 'TTF'), os.path.join(settings.STATIC_ROOT, 'font-dejavu'), os.path.join(settings.STATIC_ROOT, 'font-droid')))
    os.environ['FONTCONFIG_FILE'] = config_name
    configure_fontconfig.is_configured = True


def get_font_weight(weight):
    return FONT_WEIGHTS[weight]


def render_size(font, weight, size, spacing, text, width=1000, lines=1, cache_key=None):
    """Check whether rendered text fits."""
    configure_fontconfig()
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width * 2, lines * size * 4)
    context = cairo.Context(surface)
    layout = PangoCairo.create_layout(context)
    fontdesc = Pango.FontDescription.from_string(font)
    fontdesc.set_size(size * Pango.SCALE)
    if weight:
        fontdesc.set_weight(weight)
    layout.set_font_description(fontdesc)
    layout.set_markup('<span letter_spacing="{}">{}</span>'.format(spacing, escape(text)))
    layout.set_width(width * Pango.SCALE)
    layout.set_wrap(Pango.WrapMode.WORD)
    line_count = layout.get_line_count()
    pixel_size = layout.get_pixel_size()
    PangoCairo.show_layout(context, layout)
    expected_height = lines * pixel_size.height / line_count
    context.new_path()
    context.set_source_rgb(246, 102, 76)
    context.set_source_rgb(0.9647058823529412, 0.4, 0.2980392156862745)
    context.set_line_width(1)
    context.move_to(1, 1)
    context.line_to(width, 1)
    context.line_to(width, expected_height)
    context.line_to(1, expected_height)
    context.line_to(1, 1)
    context.stroke()
    if cache_key:
        with BytesIO() as (buff):
            surface.write_to_png(buff)
            cache.set(cache_key, buff.getvalue())
    return (
     pixel_size, line_count)


def check_render_size(font, weight, size, spacing, text, width, lines, cache_key=None):
    """Checks whether rendered text fits."""
    size, actual_lines = render_size(font, weight, size, spacing, text, width, lines, cache_key)
    return size.width <= width and actual_lines <= lines


def get_font_name(filelike):
    """Returns tuple of font family and style, for example ('Ubuntu', 'Regular')."""
    if not hasattr(filelike, 'loaded_font'):
        temp = NamedTemporaryFile(delete=False)
        try:
            temp.write(filelike.read())
            filelike.seek(0)
            temp.close()
            filelike.loaded_font = ImageFont.truetype(temp.name)
        finally:
            os.unlink(temp.name)

    return filelike.loaded_font.getname()


def check_fonts(app_configs=None, **kwargs):
    """Checks font rendering."""
    try:
        render_size('DejaVu Sans', Pango.Weight.NORMAL, 11, 0, 'test')
        return []
    except Exception as error:
        try:
            return [Critical(('Failed to use Pango: {}'.format(error)),
               hint=(get_doc_url('admin/install', 'pangocairo')),
               id='weblate.C024')]
        finally:
            error = None
            del error