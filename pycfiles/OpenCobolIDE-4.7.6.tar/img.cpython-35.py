# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/formatters/img.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 18158 bytes
"""
    pygments.formatters.img
    ~~~~~~~~~~~~~~~~~~~~~~~

    Formatter for Pixmap output.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import sys
from pygments.formatter import Formatter
from pygments.util import get_bool_opt, get_int_opt, get_list_opt, get_choice_opt, xrange
import subprocess
try:
    from PIL import Image, ImageDraw, ImageFont
    pil_available = True
except ImportError:
    pil_available = False

try:
    import _winreg
except ImportError:
    try:
        import winreg as _winreg
    except ImportError:
        _winreg = None

__all__ = [
 'ImageFormatter', 'GifImageFormatter', 'JpgImageFormatter',
 'BmpImageFormatter']
STYLES = {'NORMAL': ['', 'Roman', 'Book', 'Normal', 'Regular', 'Medium'], 
 'ITALIC': ['Oblique', 'Italic'], 
 'BOLD': ['Bold'], 
 'BOLDITALIC': ['Bold Oblique', 'Bold Italic']}
DEFAULT_FONT_NAME_NIX = 'Bitstream Vera Sans Mono'
DEFAULT_FONT_NAME_WIN = 'Courier New'

class PilNotAvailable(ImportError):
    __doc__ = 'When Python imaging library is not available'


class FontNotFound(Exception):
    __doc__ = 'When there are no usable fonts specified'


class FontManager(object):
    __doc__ = '\n    Manages a set of fonts: normal, italic, bold, etc...\n    '

    def __init__(self, font_name, font_size=14):
        self.font_name = font_name
        self.font_size = font_size
        self.fonts = {}
        self.encoding = None
        if sys.platform.startswith('win'):
            if not font_name:
                self.font_name = DEFAULT_FONT_NAME_WIN
            self._create_win()
        else:
            if not font_name:
                self.font_name = DEFAULT_FONT_NAME_NIX
            self._create_nix()

    def _get_nix_font_path(self, name, style):
        proc = subprocess.Popen(['fc-list', '%s:style=%s' % (name, style), 'file'], stdout=subprocess.PIPE, stderr=None)
        stdout, _ = proc.communicate()
        if proc.returncode == 0:
            lines = stdout.splitlines()
            for line in lines:
                if line.startswith(b'Fontconfig warning:'):
                    pass
                else:
                    path = line.decode().strip().strip(':')
                    if path:
                        return path

            return

    def _create_nix(self):
        for name in STYLES['NORMAL']:
            path = self._get_nix_font_path(self.font_name, name)
            if path is not None:
                self.fonts['NORMAL'] = ImageFont.truetype(path, self.font_size)
                break
        else:
            raise FontNotFound('No usable fonts named: "%s"' % self.font_name)

        for style in ('ITALIC', 'BOLD', 'BOLDITALIC'):
            for stylename in STYLES[style]:
                path = self._get_nix_font_path(self.font_name, stylename)
                if path is not None:
                    self.fonts[style] = ImageFont.truetype(path, self.font_size)
                    break
            else:
                if style == 'BOLDITALIC':
                    self.fonts[style] = self.fonts['BOLD']
                else:
                    self.fonts[style] = self.fonts['NORMAL']

    def _lookup_win(self, key, basename, styles, fail=False):
        for suffix in ('', ' (TrueType)'):
            for style in styles:
                try:
                    valname = '%s%s%s' % (basename, style and ' ' + style, suffix)
                    val, _ = _winreg.QueryValueEx(key, valname)
                    return val
                except EnvironmentError:
                    continue

        else:
            if fail:
                raise FontNotFound('Font %s (%s) not found in registry' % (
                 basename, styles[0]))
            return

    def _create_win(self):
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts')
        except EnvironmentError:
            try:
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows\\CurrentVersion\\Fonts')
            except EnvironmentError:
                raise FontNotFound("Can't open Windows font registry key")

        try:
            path = self._lookup_win(key, self.font_name, STYLES['NORMAL'], True)
            self.fonts['NORMAL'] = ImageFont.truetype(path, self.font_size)
            for style in ('ITALIC', 'BOLD', 'BOLDITALIC'):
                path = self._lookup_win(key, self.font_name, STYLES[style])
                if path:
                    self.fonts[style] = ImageFont.truetype(path, self.font_size)
                else:
                    if style == 'BOLDITALIC':
                        self.fonts[style] = self.fonts['BOLD']
                    else:
                        self.fonts[style] = self.fonts['NORMAL']

        finally:
            _winreg.CloseKey(key)

    def get_char_size(self):
        """
        Get the character size.
        """
        return self.fonts['NORMAL'].getsize('M')

    def get_font(self, bold, oblique):
        """
        Get the font based on bold and italic flags.
        """
        if bold and oblique:
            return self.fonts['BOLDITALIC']
        else:
            if bold:
                return self.fonts['BOLD']
            if oblique:
                return self.fonts['ITALIC']
            return self.fonts['NORMAL']


class ImageFormatter(Formatter):
    __doc__ = '\n    Create a PNG image from source code. This uses the Python Imaging Library to\n    generate a pixmap from the source code.\n\n    .. versionadded:: 0.10\n\n    Additional options accepted:\n\n    `image_format`\n        An image format to output to that is recognised by PIL, these include:\n\n        * "PNG" (default)\n        * "JPEG"\n        * "BMP"\n        * "GIF"\n\n    `line_pad`\n        The extra spacing (in pixels) between each line of text.\n\n        Default: 2\n\n    `font_name`\n        The font name to be used as the base font from which others, such as\n        bold and italic fonts will be generated.  This really should be a\n        monospace font to look sane.\n\n        Default: "Bitstream Vera Sans Mono" on Windows, Courier New on \\*nix\n\n    `font_size`\n        The font size in points to be used.\n\n        Default: 14\n\n    `image_pad`\n        The padding, in pixels to be used at each edge of the resulting image.\n\n        Default: 10\n\n    `line_numbers`\n        Whether line numbers should be shown: True/False\n\n        Default: True\n\n    `line_number_start`\n        The line number of the first line.\n\n        Default: 1\n\n    `line_number_step`\n        The step used when printing line numbers.\n\n        Default: 1\n\n    `line_number_bg`\n        The background colour (in "#123456" format) of the line number bar, or\n        None to use the style background color.\n\n        Default: "#eed"\n\n    `line_number_fg`\n        The text color of the line numbers (in "#123456"-like format).\n\n        Default: "#886"\n\n    `line_number_chars`\n        The number of columns of line numbers allowable in the line number\n        margin.\n\n        Default: 2\n\n    `line_number_bold`\n        Whether line numbers will be bold: True/False\n\n        Default: False\n\n    `line_number_italic`\n        Whether line numbers will be italicized: True/False\n\n        Default: False\n\n    `line_number_separator`\n        Whether a line will be drawn between the line number area and the\n        source code area: True/False\n\n        Default: True\n\n    `line_number_pad`\n        The horizontal padding (in pixels) between the line number margin, and\n        the source code area.\n\n        Default: 6\n\n    `hl_lines`\n        Specify a list of lines to be highlighted.\n\n        .. versionadded:: 1.2\n\n        Default: empty list\n\n    `hl_color`\n        Specify the color for highlighting lines.\n\n        .. versionadded:: 1.2\n\n        Default: highlight color of the selected style\n    '
    name = 'img'
    aliases = ['img', 'IMG', 'png']
    filenames = ['*.png']
    unicodeoutput = False
    default_image_format = 'png'

    def __init__(self, **options):
        """
        See the class docstring for explanation of options.
        """
        if not pil_available:
            raise PilNotAvailable('Python Imaging Library is required for this formatter')
        Formatter.__init__(self, **options)
        self.encoding = 'latin1'
        self.styles = dict(self.style)
        if self.style.background_color is None:
            self.background_color = '#fff'
        else:
            self.background_color = self.style.background_color
        self.image_format = get_choice_opt(options, 'image_format', ['png', 'jpeg', 'gif', 'bmp'], self.default_image_format, normcase=True)
        self.image_pad = get_int_opt(options, 'image_pad', 10)
        self.line_pad = get_int_opt(options, 'line_pad', 2)
        fontsize = get_int_opt(options, 'font_size', 14)
        self.fonts = FontManager(options.get('font_name', ''), fontsize)
        self.fontw, self.fonth = self.fonts.get_char_size()
        self.line_number_fg = options.get('line_number_fg', '#886')
        self.line_number_bg = options.get('line_number_bg', '#eed')
        self.line_number_chars = get_int_opt(options, 'line_number_chars', 2)
        self.line_number_bold = get_bool_opt(options, 'line_number_bold', False)
        self.line_number_italic = get_bool_opt(options, 'line_number_italic', False)
        self.line_number_pad = get_int_opt(options, 'line_number_pad', 6)
        self.line_numbers = get_bool_opt(options, 'line_numbers', True)
        self.line_number_separator = get_bool_opt(options, 'line_number_separator', True)
        self.line_number_step = get_int_opt(options, 'line_number_step', 1)
        self.line_number_start = get_int_opt(options, 'line_number_start', 1)
        if self.line_numbers:
            self.line_number_width = self.fontw * self.line_number_chars + self.line_number_pad * 2
        else:
            self.line_number_width = 0
        self.hl_lines = []
        hl_lines_str = get_list_opt(options, 'hl_lines', [])
        for line in hl_lines_str:
            try:
                self.hl_lines.append(int(line))
            except ValueError:
                pass

        self.hl_color = options.get('hl_color', self.style.highlight_color) or '#f90'
        self.drawables = []

    def get_style_defs(self, arg=''):
        raise NotImplementedError('The -S option is meaningless for the image formatter. Use -O style=<stylename> instead.')

    def _get_line_height(self):
        """
        Get the height of a line.
        """
        return self.fonth + self.line_pad

    def _get_line_y(self, lineno):
        """
        Get the Y coordinate of a line number.
        """
        return lineno * self._get_line_height() + self.image_pad

    def _get_char_width(self):
        """
        Get the width of a character.
        """
        return self.fontw

    def _get_char_x(self, charno):
        """
        Get the X coordinate of a character position.
        """
        return charno * self.fontw + self.image_pad + self.line_number_width

    def _get_text_pos(self, charno, lineno):
        """
        Get the actual position for a character and line position.
        """
        return (
         self._get_char_x(charno), self._get_line_y(lineno))

    def _get_linenumber_pos(self, lineno):
        """
        Get the actual position for the start of a line number.
        """
        return (
         self.image_pad, self._get_line_y(lineno))

    def _get_text_color(self, style):
        """
        Get the correct color for the token from the style.
        """
        if style['color'] is not None:
            fill = '#' + style['color']
        else:
            fill = '#000'
        return fill

    def _get_style_font(self, style):
        """
        Get the correct font for the style.
        """
        return self.fonts.get_font(style['bold'], style['italic'])

    def _get_image_size(self, maxcharno, maxlineno):
        """
        Get the required image size.
        """
        return (
         self._get_char_x(maxcharno) + self.image_pad,
         self._get_line_y(maxlineno + 0) + self.image_pad)

    def _draw_linenumber(self, posno, lineno):
        """
        Remember a line number drawable to paint later.
        """
        self._draw_text(self._get_linenumber_pos(posno), str(lineno).rjust(self.line_number_chars), font=self.fonts.get_font(self.line_number_bold, self.line_number_italic), fill=self.line_number_fg)

    def _draw_text(self, pos, text, font, **kw):
        """
        Remember a single drawable tuple to paint later.
        """
        self.drawables.append((pos, text, font, kw))

    def _create_drawables(self, tokensource):
        """
        Create drawables for the token content.
        """
        lineno = charno = maxcharno = 0
        for ttype, value in tokensource:
            while ttype not in self.styles:
                ttype = ttype.parent

            style = self.styles[ttype]
            value = value.expandtabs(4)
            lines = value.splitlines(True)
            for i, line in enumerate(lines):
                temp = line.rstrip('\n')
                if temp:
                    self._draw_text(self._get_text_pos(charno, lineno), temp, font=self._get_style_font(style), fill=self._get_text_color(style))
                    charno += len(temp)
                    maxcharno = max(maxcharno, charno)
                if line.endswith('\n'):
                    charno = 0
                    lineno += 1

        self.maxcharno = maxcharno
        self.maxlineno = lineno

    def _draw_line_numbers(self):
        """
        Create drawables for the line numbers.
        """
        if not self.line_numbers:
            return
        for p in xrange(self.maxlineno):
            n = p + self.line_number_start
            if n % self.line_number_step == 0:
                self._draw_linenumber(p, n)

    def _paint_line_number_bg(self, im):
        """
        Paint the line number background on the image.
        """
        if not self.line_numbers:
            return
        if self.line_number_fg is None:
            return
        draw = ImageDraw.Draw(im)
        recth = im.size[(-1)]
        rectw = self.image_pad + self.line_number_width - self.line_number_pad
        draw.rectangle([(0, 0), (rectw, recth)], fill=self.line_number_bg)
        draw.line([(rectw, 0), (rectw, recth)], fill=self.line_number_fg)
        del draw

    def format(self, tokensource, outfile):
        """
        Format ``tokensource``, an iterable of ``(tokentype, tokenstring)``
        tuples and write it into ``outfile``.

        This implementation calculates where it should draw each token on the
        pixmap, then calculates the required pixmap size and draws the items.
        """
        self._create_drawables(tokensource)
        self._draw_line_numbers()
        im = Image.new('RGB', self._get_image_size(self.maxcharno, self.maxlineno), self.background_color)
        self._paint_line_number_bg(im)
        draw = ImageDraw.Draw(im)
        if self.hl_lines:
            x = self.image_pad + self.line_number_width - self.line_number_pad + 1
            recth = self._get_line_height()
            rectw = im.size[0] - x
            for linenumber in self.hl_lines:
                y = self._get_line_y(linenumber - 1)
                draw.rectangle([(x, y), (x + rectw, y + recth)], fill=self.hl_color)

        for pos, value, font, kw in self.drawables:
            draw.text(pos, value, font=font, **kw)

        im.save(outfile, self.image_format.upper())


class GifImageFormatter(ImageFormatter):
    __doc__ = '\n    Create a GIF image from source code. This uses the Python Imaging Library to\n    generate a pixmap from the source code.\n\n    .. versionadded:: 1.0\n    '
    name = 'img_gif'
    aliases = ['gif']
    filenames = ['*.gif']
    default_image_format = 'gif'


class JpgImageFormatter(ImageFormatter):
    __doc__ = '\n    Create a JPEG image from source code. This uses the Python Imaging Library to\n    generate a pixmap from the source code.\n\n    .. versionadded:: 1.0\n    '
    name = 'img_jpg'
    aliases = ['jpg', 'jpeg']
    filenames = ['*.jpg']
    default_image_format = 'jpeg'


class BmpImageFormatter(ImageFormatter):
    __doc__ = '\n    Create a bitmap image from source code. This uses the Python Imaging Library to\n    generate a pixmap from the source code.\n\n    .. versionadded:: 1.0\n    '
    name = 'img_bmp'
    aliases = ['bmp', 'bitmap']
    filenames = ['*.bmp']
    default_image_format = 'bmp'