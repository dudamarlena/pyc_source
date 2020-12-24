# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/formatters/svg.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 5840 bytes
"""
    pygments.formatters.svg
    ~~~~~~~~~~~~~~~~~~~~~~~

    Formatter for SVG output.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.formatter import Formatter
from pygments.util import get_bool_opt, get_int_opt
__all__ = [
 'SvgFormatter']

def escape_html(text):
    """Escape &, <, > as well as single and double quotes for HTML."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')


class2style = {}

class SvgFormatter(Formatter):
    __doc__ = '\n    Format tokens as an SVG graphics file.  This formatter is still experimental.\n    Each line of code is a ``<text>`` element with explicit ``x`` and ``y``\n    coordinates containing ``<tspan>`` elements with the individual token styles.\n\n    By default, this formatter outputs a full SVG document including doctype\n    declaration and the ``<svg>`` root element.\n\n    .. versionadded:: 0.9\n\n    Additional options accepted:\n\n    `nowrap`\n        Don\'t wrap the SVG ``<text>`` elements in ``<svg><g>`` elements and\n        don\'t add a XML declaration and a doctype.  If true, the `fontfamily`\n        and `fontsize` options are ignored.  Defaults to ``False``.\n\n    `fontfamily`\n        The value to give the wrapping ``<g>`` element\'s ``font-family``\n        attribute, defaults to ``"monospace"``.\n\n    `fontsize`\n        The value to give the wrapping ``<g>`` element\'s ``font-size``\n        attribute, defaults to ``"14px"``.\n\n    `xoffset`\n        Starting offset in X direction, defaults to ``0``.\n\n    `yoffset`\n        Starting offset in Y direction, defaults to the font size if it is given\n        in pixels, or ``20`` else.  (This is necessary since text coordinates\n        refer to the text baseline, not the top edge.)\n\n    `ystep`\n        Offset to add to the Y coordinate for each subsequent line.  This should\n        roughly be the text size plus 5.  It defaults to that value if the text\n        size is given in pixels, or ``25`` else.\n\n    `spacehack`\n        Convert spaces in the source to ``&#160;``, which are non-breaking\n        spaces.  SVG provides the ``xml:space`` attribute to control how\n        whitespace inside tags is handled, in theory, the ``preserve`` value\n        could be used to keep all whitespace as-is.  However, many current SVG\n        viewers don\'t obey that rule, so this option is provided as a workaround\n        and defaults to ``True``.\n    '
    name = 'SVG'
    aliases = ['svg']
    filenames = ['*.svg']

    def __init__(self, **options):
        (Formatter.__init__)(self, **options)
        self.nowrap = get_bool_opt(options, 'nowrap', False)
        self.fontfamily = options.get('fontfamily', 'monospace')
        self.fontsize = options.get('fontsize', '14px')
        self.xoffset = get_int_opt(options, 'xoffset', 0)
        fs = self.fontsize.strip()
        if fs.endswith('px'):
            fs = fs[:-2].strip()
        try:
            int_fs = int(fs)
        except:
            int_fs = 20

        self.yoffset = get_int_opt(options, 'yoffset', int_fs)
        self.ystep = get_int_opt(options, 'ystep', int_fs + 5)
        self.spacehack = get_bool_opt(options, 'spacehack', True)
        self._stylecache = {}

    def format_unencoded(self, tokensource, outfile):
        """
        Format ``tokensource``, an iterable of ``(tokentype, tokenstring)``
        tuples and write it into ``outfile``.

        For our implementation we put all lines in their own 'line group'.
        """
        x = self.xoffset
        y = self.yoffset
        if not self.nowrap:
            if self.encoding:
                outfile.write('<?xml version="1.0" encoding="%s"?>\n' % self.encoding)
            else:
                outfile.write('<?xml version="1.0"?>\n')
            outfile.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
            outfile.write('<svg xmlns="http://www.w3.org/2000/svg">\n')
            outfile.write('<g font-family="%s" font-size="%s">\n' % (
             self.fontfamily, self.fontsize))
        outfile.write('<text x="%s" y="%s" xml:space="preserve">' % (x, y))
        for ttype, value in tokensource:
            style = self._get_style(ttype)
            tspan = style and '<tspan' + style + '>' or ''
            tspanend = tspan and '</tspan>' or ''
            value = escape_html(value)
            if self.spacehack:
                value = value.expandtabs().replace(' ', '&#160;')
            parts = value.split('\n')
            for part in parts[:-1]:
                outfile.write(tspan + part + tspanend)
                y += self.ystep
                outfile.write('</text>\n<text x="%s" y="%s" xml:space="preserve">' % (
                 x, y))

            outfile.write(tspan + parts[(-1)] + tspanend)

        outfile.write('</text>')
        if not self.nowrap:
            outfile.write('</g></svg>\n')

    def _get_style(self, tokentype):
        if tokentype in self._stylecache:
            return self._stylecache[tokentype]
        else:
            otokentype = tokentype
            while not self.style.styles_token(tokentype):
                tokentype = tokentype.parent

            value = self.style.style_for_token(tokentype)
            result = ''
            if value['color']:
                result = ' fill="#' + value['color'] + '"'
            if value['bold']:
                result += ' font-weight="bold"'
            if value['italic']:
                result += ' font-style="italic"'
            self._stylecache[otokentype] = result
            return result