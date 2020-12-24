# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/markdown/extensions/wysiwyg_email.py
# Compiled at: 2019-06-12 01:17:17
"""Markdown extension to render content similar to the source in e-mails.

This will render Markdown such that the spacing and alignment in the source
text and the rendered content looks roughly the same. It's meant to help ensure
that what's typed is very close to what's viewed when rendered.
"""
from __future__ import absolute_import, unicode_literals
from django import template
from django.utils import six
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
register = template.Library()

class InlineStyleProcessor(Treeprocessor):
    """Injects CSS styles directly into the tags, for use in e-mails.

    This will process each element and, depending on the element type,
    create inline styles. These styles are meant to match the stylesheets
    in the :file:`markdown-wysiwyg.less` file.
    """

    def process_element(self, context, el):
        """Process an element in the tree.

        This adds a handful of inline styles to the resulting document which
        mimic the .rich-text rules in markdown-wysiwyg.less.

        This does not do quite everything that the markdown-wysiwyg.less rules
        do, due to the complexity in implementing CSS selectors in Python,
        and the CSS compatibility logic in most e-mail clients.

        The end result is that the e-mail will look similar but not identical
        to the page.
        """
        style = {b'margin': 0, 
           b'padding': 0, 
           b'line-height': b'inherit', 
           b'text-rendering': b'inherit', 
           b'white-space': b'normal'}
        tag = el.tag
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            style[b'font-size'] = b'100%'
        else:
            if tag == b'ul':
                style[b'margin'] = b'0 0 0 1em'
            elif tag == b'ol':
                style[b'margin'] = b'0 0 0 2em'
            elif tag == b'code':
                style[b'color'] = b'#4444cc'
            elif tag == b'p':
                style[b'white-space'] = b'inherit'
            elif tag == b'blockquote':
                style.update({b'border-left': b'1px solid #bbb', 
                   b'padding': b'0 0 0 1em', 
                   b'margin': b'0 0 0 0.5em'})
            elif tag == b'hr':
                style[b'border'] = b'1px solid #ddd'
            elif tag in ('th', 'td'):
                style.update({b'border-bottom': b'1px solid #bbb', 
                   b'padding': b'0.2em 1em'})
            el.set(b'style', (b'').join(b'%s: %s;' % (k, v) for k, v in six.iteritems(style)))
            context.append(tag)
            for child in el:
                self.process_element(context, child)

        context.pop()

    def run(self, root):
        for child in root:
            self.process_element([], child)


class WysiwygEMailExtension(Extension):
    """A Markdown extension to inject CSS into elements for HTML output.

    This is meant as a counterpart to the Wysiwyg Markdown extension. It
    aims to provide HTML output that looks as similar as possible to the
    input, preserving the spacing, font sizes, alignment, and other styles
    from the raw text.

    This is meant to be used with the following Markdown configuration
    and extensions:

    .. code-block:: python

        {
            'extensions': [
                'codehilite(noclasss=True)', 'tables',
                'djblets.markdown.extentions.wysiwyg',
            ],
        }
    """

    def extendMarkdown(self, md, md_globals):
        """Extend the list of Markdown processors."""
        md.treeprocessors.add(b'inlinestyle', InlineStyleProcessor(), b'_end')


def makeExtension(*args, **kwargs):
    """Create and return an instance of this extension.

    Args:
        *args (tuple):
            Positional arguments for the extension.

        **kwargs (dict):
            Keyword arguments for the extension.
    """
    return WysiwygEMailExtension(*args, **kwargs)