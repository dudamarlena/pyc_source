# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/formatter.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 2948 bytes
"""
    pygments.formatter
    ~~~~~~~~~~~~~~~~~~

    Base formatter class.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import codecs
from pygments.util import get_bool_opt, string_types
from pygments.styles import get_style_by_name
__all__ = [
 'Formatter']

def _lookup_style(style):
    if isinstance(style, string_types):
        return get_style_by_name(style)
    else:
        return style


class Formatter(object):
    __doc__ = '\n    Converts a token stream to text.\n\n    Options accepted:\n\n    ``style``\n        The style to use, can be a string or a Style subclass\n        (default: "default"). Not used by e.g. the\n        TerminalFormatter.\n    ``full``\n        Tells the formatter to output a "full" document, i.e.\n        a complete self-contained document. This doesn\'t have\n        any effect for some formatters (default: false).\n    ``title``\n        If ``full`` is true, the title that should be used to\n        caption the document (default: \'\').\n    ``encoding``\n        If given, must be an encoding name. This will be used to\n        convert the Unicode token strings to byte strings in the\n        output. If it is "" or None, Unicode strings will be written\n        to the output file, which most file-like objects do not\n        support (default: None).\n    ``outencoding``\n        Overrides ``encoding`` if given.\n    '
    name = None
    aliases = []
    filenames = []
    unicodeoutput = True

    def __init__(self, **options):
        self.style = _lookup_style(options.get('style', 'default'))
        self.full = get_bool_opt(options, 'full', False)
        self.title = options.get('title', '')
        self.encoding = options.get('encoding', None) or None
        if self.encoding in ('guess', 'chardet'):
            self.encoding = 'utf-8'
        self.encoding = options.get('outencoding') or self.encoding
        self.options = options

    def get_style_defs(self, arg=''):
        """
        Return the style definitions for the current style as a string.

        ``arg`` is an additional argument whose meaning depends on the
        formatter used. Note that ``arg`` can also be a list or tuple
        for some formatters like the html formatter.
        """
        return ''

    def format(self, tokensource, outfile):
        """
        Format ``tokensource``, an iterable of ``(tokentype, tokenstring)``
        tuples and write it into ``outfile``.
        """
        if self.encoding:
            outfile = codecs.lookup(self.encoding)[3](outfile)
        return self.format_unencoded(tokensource, outfile)