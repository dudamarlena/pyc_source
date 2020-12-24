# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/simplehtml.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.pkg.core.simplehtml\n    ~~~~~~~~~~~~~~~~~~~~~~~~~\n\n    This module provides a MarkupFormat that allows the user to use\n    HTML as markup but strips dangerous tags like ``<script>`` and others.\n\n    It uses the ``secure_html`` method from the ``html`` util.\n\n    :copyright: 2006 by Armin Ronacher.\n    :license: GNU GPL, see LICENSE for more details.\n'
from pocoo.utils.html import secure_html
from pocoo.pkg.core.textfmt import MarkupFormat

class SimpleHTML(MarkupFormat):
    __module__ = __name__
    name = 'simplehtml'

    def parse(self, text):
        return secure_html(text)

    def quote_text(self, req, text, username=None):
        if username is not None:
            _ = req.gettext
            text = '<em>%s:</em><br />%s' % (_('%s wrote') % username, text)
        return '<blockquote>%s</blockquote>' % text