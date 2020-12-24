# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/core/simplehtml.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.pkg.core.simplehtml
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    This module provides a MarkupFormat that allows the user to use
    HTML as markup but strips dangerous tags like ``<script>`` and others.

    It uses the ``secure_html`` method from the ``html`` util.

    :copyright: 2006 by Armin Ronacher.
    :license: GNU GPL, see LICENSE for more details.
"""
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