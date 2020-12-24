# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/formatters/rtf.py
# Compiled at: 2011-04-22 17:53:24
"""
    pygments.formatters.rtf
    ~~~~~~~~~~~~~~~~~~~~~~~

    A formatter that generates RTF files.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.formatter import Formatter
__all__ = [
 'RtfFormatter']

class RtfFormatter(Formatter):
    """
    Format tokens as RTF markup. This formatter automatically outputs full RTF
    documents with color information and other useful stuff. Perfect for Copy and
    Paste into Microsoft® Word® documents.

    *New in Pygments 0.6.*

    Additional options accepted:

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).

    `fontface`
        The used font famliy, for example ``Bitstream Vera Sans``. Defaults to
        some generic font which is supposed to have fixed width.
    """
    name = 'RTF'
    aliases = ['rtf']
    filenames = ['*.rtf']
    unicodeoutput = False

    def __init__(self, **options):
        """
        Additional options accepted:

        ``fontface``
            Name of the font used. Could for example be ``'Courier New'``
            to further specify the default which is ``'\x0cmodern'``. The RTF
            specification claims that ``\x0cmodern`` are "Fixed-pitch serif
            and sans serif fonts". Hope every RTF implementation thinks
            the same about modern...
        """
        Formatter.__init__(self, **options)
        self.fontface = options.get('fontface') or ''

    def _escape(self, text):
        return text.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')

    def _escape_text(self, text):
        if not text:
            return ''
        text = self._escape(text)
        if self.encoding in ('utf-8', 'utf-16', 'utf-32'):
            encoding = 'iso-8859-15'
        else:
            encoding = self.encoding or 'iso-8859-15'
        buf = []
        for c in text:
            if ord(c) > 128:
                ansic = c.encode(encoding, 'ignore') or '?'
                if ord(ansic) > 128:
                    ansic = "\\'%x" % ord(ansic)
                else:
                    ansic = c
                buf.append('\\ud{\\u%d%s}' % (ord(c), ansic))
            else:
                buf.append(str(c))

        return ('').join(buf).replace('\n', '\\par\n')

    def format_unencoded(self, tokensource, outfile):
        outfile.write('{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0\\fmodern\\fprq1\\fcharset0%s;}}{\\colortbl;' % (self.fontface and ' ' + self._escape(self.fontface) or ''))
        color_mapping = {}
        offset = 1
        for (_, style) in self.style:
            for color in (style['color'], style['bgcolor'], style['border']):
                if color and color not in color_mapping:
                    color_mapping[color] = offset
                    outfile.write('\\red%d\\green%d\\blue%d;' % (
                     int(color[0:2], 16),
                     int(color[2:4], 16),
                     int(color[4:6], 16)))
                    offset += 1

        outfile.write('}\\f0')
        for (ttype, value) in tokensource:
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
            start = ('').join(buf)
            if start:
                outfile.write('{%s ' % start)
            outfile.write(self._escape_text(value))
            if start:
                outfile.write('}')

        outfile.write('}')