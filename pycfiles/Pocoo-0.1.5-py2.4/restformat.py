# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/restformat.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.pkg.core.restformat
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Pocoo ReST Parser.

    A thin wrapper around the docutils ReST parser.

    :copyright: 2006 by Georg Brandl.
    :license: GNU GPL, see LICENSE for more details.
"""
from pocoo.pkg.core.textfmt import MarkupFormat
from pocoo.utils.html import escape_html
from pocoo.pkg.core.smilies import replace_smilies

class ReST(MarkupFormat):
    """
    ReST markup format.
    """
    __module__ = __name__
    name = 'rest'

    def parse(self, text, signature):
        from docutils.core import publish_parts
        try:
            parts = publish_parts(source=text, writer_name='html4css1')
            text = parts['fragment'].strip()
        except Exception:
            text = escape_html(text).strip()

        return replace_smilies(self.ctx, text)

    def quote_text(self, req, text, username=None):
        lines = [ '    %s' % line for line in text.splitlines() ]
        if username is not None:
            _ = req.gettext
            lines.insert(0, '    **%s**:' % _('%s wrote') % username)
        return ('\n').join(lines)