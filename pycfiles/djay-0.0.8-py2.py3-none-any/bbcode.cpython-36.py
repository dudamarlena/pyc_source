# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/formatters/bbcode.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 3314 bytes
"""
    pygments.formatters.bbcode
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    BBcode formatter.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.formatter import Formatter
from pygments.util import get_bool_opt
__all__ = [
 'BBCodeFormatter']

class BBCodeFormatter(Formatter):
    __doc__ = "\n    Format tokens with BBcodes. These formatting codes are used by many\n    bulletin boards, so you can highlight your sourcecode with pygments before\n    posting it there.\n\n    This formatter has no support for background colors and borders, as there\n    are no common BBcode tags for that.\n\n    Some board systems (e.g. phpBB) don't support colors in their [code] tag,\n    so you can't use the highlighting together with that tag.\n    Text in a [code] tag usually is shown with a monospace font (which this\n    formatter can do with the ``monofont`` option) and no spaces (which you\n    need for indentation) are removed.\n\n    Additional options accepted:\n\n    `style`\n        The style to use, can be a string or a Style subclass (default:\n        ``'default'``).\n\n    `codetag`\n        If set to true, put the output into ``[code]`` tags (default:\n        ``false``)\n\n    `monofont`\n        If set to true, add a tag to show the code with a monospace font\n        (default: ``false``).\n    "
    name = 'BBCode'
    aliases = ['bbcode', 'bb']
    filenames = []

    def __init__(self, **options):
        (Formatter.__init__)(self, **options)
        self._code = get_bool_opt(options, 'codetag', False)
        self._mono = get_bool_opt(options, 'monofont', False)
        self.styles = {}
        self._make_styles()

    def _make_styles(self):
        for ttype, ndef in self.style:
            start = end = ''
            if ndef['color']:
                start += '[color=#%s]' % ndef['color']
                end = '[/color]' + end
            if ndef['bold']:
                start += '[b]'
                end = '[/b]' + end
            if ndef['italic']:
                start += '[i]'
                end = '[/i]' + end
            if ndef['underline']:
                start += '[u]'
                end = '[/u]' + end
            self.styles[ttype] = (
             start, end)

    def format_unencoded(self, tokensource, outfile):
        if self._code:
            outfile.write('[code]')
        else:
            if self._mono:
                outfile.write('[font=monospace]')
            else:
                lastval = ''
                lasttype = None
                for ttype, value in tokensource:
                    while ttype not in self.styles:
                        ttype = ttype.parent

                    if ttype == lasttype:
                        lastval += value
                    else:
                        if lastval:
                            start, end = self.styles[lasttype]
                            outfile.write(''.join((start, lastval, end)))
                        lastval = value
                        lasttype = ttype

                if lastval:
                    start, end = self.styles[lasttype]
                    outfile.write(''.join((start, lastval, end)))
                if self._mono:
                    outfile.write('[/font]')
                if self._code:
                    outfile.write('[/code]')
            if self._code or self._mono:
                outfile.write('\n')