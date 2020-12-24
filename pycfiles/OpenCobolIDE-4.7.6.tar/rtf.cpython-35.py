# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/formatters/rtf.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 5049 bytes
"""
    pygments.formatters.rtf
    ~~~~~~~~~~~~~~~~~~~~~~~

    A formatter that generates RTF files.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.formatter import Formatter
from pygments.util import get_int_opt, _surrogatepair
__all__ = [
 'RtfFormatter']

class RtfFormatter(Formatter):
    __doc__ = "\n    Format tokens as RTF markup. This formatter automatically outputs full RTF\n    documents with color information and other useful stuff. Perfect for Copy and\n    Paste into Microsoft(R) Word(R) documents.\n\n    Please note that ``encoding`` and ``outencoding`` options are ignored.\n    The RTF format is ASCII natively, but handles unicode characters correctly\n    thanks to escape sequences.\n\n    .. versionadded:: 0.6\n\n    Additional options accepted:\n\n    `style`\n        The style to use, can be a string or a Style subclass (default:\n        ``'default'``).\n\n    `fontface`\n        The used font famliy, for example ``Bitstream Vera Sans``. Defaults to\n        some generic font which is supposed to have fixed width.\n\n    `fontsize`\n        Size of the font used. Size is specified in half points. The\n        default is 24 half-points, giving a size 12 font.\n\n        .. versionadded:: 2.0\n    "
    name = 'RTF'
    aliases = ['rtf']
    filenames = ['*.rtf']

    def __init__(self, **options):
        r"""
        Additional options accepted:

        ``fontface``
            Name of the font used. Could for example be ``'Courier New'``
            to further specify the default which is ``'\fmodern'``. The RTF
            specification claims that ``\fmodern`` are "Fixed-pitch serif
            and sans serif fonts". Hope every RTF implementation thinks
            the same about modern...

        """
        Formatter.__init__(self, **options)
        self.fontface = options.get('fontface') or ''
        self.fontsize = get_int_opt(options, 'fontsize', 0)

    def _escape(self, text):
        return text.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')

    def _escape_text(self, text):
        if not text:
            return ''
        text = self._escape(text)
        buf = []
        for c in text:
            cn = ord(c)
            if cn < 128:
                buf.append(str(c))
            else:
                if 128 <= cn < 65536:
                    buf.append('{\\u%d}' % cn)
                elif 65536 <= cn:
                    buf.append('{\\u%d}{\\u%d}' % _surrogatepair(cn))

        return ''.join(buf).replace('\n', '\\par\n')

    def format_unencoded(self, tokensource, outfile):
        outfile.write('{\\rtf1\\ansi\\uc0\\deff0{\\fonttbl{\\f0\\fmodern\\fprq1\\fcharset0%s;}}{\\colortbl;' % (self.fontface and ' ' + self._escape(self.fontface) or ''))
        color_mapping = {}
        offset = 1
        for _, style in self.style:
            for color in (style['color'], style['bgcolor'], style['border']):
                if color and color not in color_mapping:
                    color_mapping[color] = offset
                    outfile.write('\\red%d\\green%d\\blue%d;' % (
                     int(color[0:2], 16),
                     int(color[2:4], 16),
                     int(color[4:6], 16)))
                    offset += 1

        outfile.write('}\\f0 ')
        if self.fontsize:
            outfile.write('\\fs%d' % self.fontsize)
        for ttype, value in tokensource:
            while not self.style.styles_token(ttype) and ttype.parent:
                ttype = ttype.parent

            style = self.style.style_for_token(ttype)
            buf = []
            if style['bgcolor']:
                buf.append('\\cb%d' % color_mapping[style['bgcolor']])
            if style['color']:
                buf.append('\\cf%d' % color_mapping[style['color']])
            if style['bold']:
                buf.append('\\b')
            if style['italic']:
                buf.append('\\i')
            if style['underline']:
                buf.append('\\ul')
            if style['border']:
                buf.append('\\chbrdr\\chcfpat%d' % color_mapping[style['border']])
            start = ''.join(buf)
            if start:
                outfile.write('{%s ' % start)
            outfile.write(self._escape_text(value))
            if start:
                outfile.write('}')

        outfile.write('}')