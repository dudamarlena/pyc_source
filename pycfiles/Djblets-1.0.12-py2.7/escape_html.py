# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/markdown/extensions/escape_html.py
# Compiled at: 2019-06-12 01:17:17
"""Markdown extension to safely escape HTML content.

This is built as a replacement for the ``safe_mode='escape'`` Markdown render
mode, which is deprecated in Python-Markdown 2.5.
"""
from __future__ import unicode_literals
from markdown.extensions import Extension

class EscapeHTMLExtension(Extension):
    """Extension to safely escape HTML content.

    This will remove any HTML preprocessors and patterns from the renderer,
    preventing HTML from being interpreted in any form. This results in the
    HTML being escaped instead, directly mimicking the behavior of the old
    ``safe_mode='escape'``.
    """

    def extendMarkdown(self, md, md_globals):
        """Extend the list of Markdown processors.

        Rather than extending, this will actually remove all HTML-based
        processors from the renderer, ensuring that the HTML is instead
        escaped.

        Args:
            md (markdown.Markdown):
                The Markdown renderer.

            md_globals (dict):
                Global variables from the :py:mod:`markdown` module.
        """
        md.preprocessors.pop(b'html_block', None)
        md.inlinePatterns.pop(b'html', None)
        return


def makeExtension(*args, **kwargs):
    """Create and return an instance of this extension.

    Args:
        *args (tuple):
            Positional arguments for the extension.

        **kwargs (dict):
            Keyword arguments for the extension.
    """
    return EscapeHTMLExtension(*args, **kwargs)