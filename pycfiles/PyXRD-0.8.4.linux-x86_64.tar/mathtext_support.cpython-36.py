# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/mathtext_support.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 5743 bytes
import logging
logger = logging.getLogger(__name__)
import re
from fractions import Fraction
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
try:
    gi.require_foreign('cairo')
except ImportError as orig:
    try:
        import cairocffi as cairo
    except ImportError as snd:
        logger.error('No cairo integration :(')
        raise snd from orig

from matplotlib import rcParams
import matplotlib.mathtext as mathtext
pbmt_cache = dict()
display = Gdk.Display.get_default()
screen = display.get_default_screen()
dpi = screen.get_resolution() or 96

def create_pb_from_mathtext(text, align='center', weight='heavy', color='b', style='normal'):
    """
        Create a Gdk.Pixbuf from a mathtext string
    """
    global dpi
    global pbmt_cache
    if text not in pbmt_cache:
        parts, fontsize = _handle_customs(text)
        pbs = []
        width = 0
        height = 0
        old_params = (
         rcParams['font.weight'], rcParams['text.color'], rcParams['font.style'])
        rcParams['font.weight'] = weight
        rcParams['text.color'] = color
        rcParams['font.style'] = style
        parser = mathtext.MathTextParser('Bitmap')
        for part in parts:
            png_loader = GdkPixbuf.PixbufLoader.new_with_type('png')
            parser.to_png(png_loader, part, dpi=dpi, fontsize=fontsize)
            png_loader.close()
            pb = png_loader.get_pixbuf()
            w, h = pb.get_width(), pb.get_height()
            width = max(width, w)
            height += h
            pbs.append((pb, w, h))

        rcParams['font.weight'], rcParams['text.color'], rcParams['font.style'] = old_params
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(surface)
        cr.save()
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.restore()
        cr.save()
        offsetx = 0
        offsety = 0
        for pb, w, h in pbs:
            if align == 'center':
                offsetx = int((width - w) / 2)
            else:
                if align == 'left':
                    offsetx = 0
                if align == 'right':
                    offsetx = int(width - w)
            Gdk.cairo_set_source_pixbuf(cr, pb, offsetx, offsety)
            cr.rectangle(offsetx, offsety, w, h)
            cr.paint()
            offsety += h

        del pbs
        cr.restore()
        pbmt_cache[text] = Gdk.pixbuf_get_from_surface(surface, 0, 0, width, height)
    return pbmt_cache[text]


def create_image_from_mathtext(text, align='center', weight='heavy', color='b', style='normal'):
    """
        Create a Gtk.Image widget from a mathtext string
    """
    image = Gtk.Image()
    image.set_from_pixbuf(create_pb_from_mathtext(text, align=align))
    return image


def _handle_customs(text):
    text = text.decode('utf-8')
    if '\\larger' in text:
        fontsize = 20
    else:
        if '\\large' in text:
            fontsize = 15
        else:
            fontsize = 10
    replacers = [('²', '$^{2}$'),
     ('³', '$^{3}$'),
     ('α', '$\\alpha$'),
     ('β', '$\\beta$'),
     ('γ', '$\\gamma$'),
     ('δ', '$\\delta$'),
     ('γ', '$\\digamma$'),
     ('η', '$\\eta$'),
     ('ι', '$\\iota$'),
     ('κ', '$\\kappa$'),
     ('λ', '$\\lambda$'),
     ('μ', '$\\mu$'),
     ('ω', '$\\omega$'),
     ('φ', '$\\phi$'),
     ('π', '$\\pi$'),
     ('ψ', '$\\psi$'),
     ('ρ', '$\\rho$'),
     ('σ', '$\\sigma$'),
     ('τ', '$\\tau$'),
     ('θ', '$\\theta$'),
     ('υ', '$\\upsilon$'),
     ('ξ', '$\\xi$'),
     ('ζ', '$\\zeta$'),
     ('\\larger', ''),
     ('\\large', ''),
     ('\\newline', '$\\newline$')]
    for val, rep in replacers:
        text = text.replace(val, rep)

    parts = text.replace('$$', '').split('\\newline')
    while '$$' in parts:
        parts.remove('$$')

    return (
     parts, fontsize)


def mt_frac(val):
    val = Fraction(val).limit_denominator()
    if val.denominator > 1:
        return '\\frac{%d}{%d}' % (val.numerator, val.denominator)
    else:
        return '%d' % val.numerator


def mt_range(lower, name, upper):
    return '\\left({ %s \\leq %s \\leq %s }\\right)' % (mt_frac(lower), name, mt_frac(upper))


def get_plot_safe(expression):
    return ''.join(_handle_customs(expression)[0])


def get_string_safe(expression):
    replacers = [
     ('$', ''),
     ('\\larger', ''),
     ('\\left', ''),
     ('\\right', ''),
     ('\\leq', '≤'),
     ('\\geq', '≥'),
     ('\\large', ''),
     ('\\newline', '\n')]
    for val, rep in replacers:
        expression = expression.replace(val, rep)

    regex_replacers = [
     ('\\\\sum_\\{(\\S+)\\}\\^\\{(\\S+)\\}', 'Σ(\\1->\\2)'),
     ('(\\S+)_(?:\\{(\\S+)\\})', '\\1\\2'),
     ('(\\S+)_(\\S+)', '\\1\\2'),
     ('\\\\frac\\{([^}])\\}\\{([^}])\\}', '\\1\\\\\\2'),
     ('\\\\frac\\{(.+)\\}\\{(.+)\\}', '(\\1)\\\\(\\2)'),
     ('\\(\\{([^})]+)\\}\\)', '(\\1)')]
    for regexpr, sub in regex_replacers:
        pattern = re.compile(regexpr)
        expression = pattern.sub(sub, expression)

    return expression