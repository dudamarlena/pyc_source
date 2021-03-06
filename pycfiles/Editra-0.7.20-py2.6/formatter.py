# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/formatter.py
# Compiled at: 2011-04-22 17:53:28
"""
    pygments.formatter
    ~~~~~~~~~~~~~~~~~~

    Base formatter class.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import codecs
from pygments.util import get_bool_opt
from pygments.styles import get_style_by_name
__all__ = [
 'Formatter']

def _lookup_style(style):
    if isinstance(style, basestring):
        return get_style_by_name(style)
    return style


class Formatter(object):
    """
    Converts a token stream to text.

    Options accepted:

    ``style``
        The style to use, can be a string or a Style subclass
        (default: "default"). Not used by e.g. the
        TerminalFormatter.
    ``full``
        Tells the formatter to output a "full" document, i.e.
        a complete self-contained document. This doesn't have
        any effect for some formatters (default: false).
    ``title``
        If ``full`` is true, the title that should be used to
        caption the document (default: '').
    ``encoding``
        If given, must be an encoding name. This will be used to
        convert the Unicode token strings to byte strings in the
        output. If it is "" or None, Unicode strings will be written
        to the output file, which most file-like objects do not
        support (default: None).
    ``outencoding``
        Overrides ``encoding`` if given.
    """
    name = None
    aliases = []
    filenames = []
    unicodeoutput = True

    def __init__(self, **options):
        self.style = _lookup_style(options.get('style', 'default'))
        self.full = get_bool_opt(options, 'full', False)
        self.title = options.get('title', '')
        self.encoding = options.get('encoding', None) or None
        self.encoding = options.get('outencoding', None) or self.encoding
        self.options = options
        return

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