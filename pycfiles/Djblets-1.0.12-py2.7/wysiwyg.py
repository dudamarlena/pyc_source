# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/markdown/extensions/wysiwyg.py
# Compiled at: 2019-06-12 01:17:17
"""Markdown extension to render content similar to the source.

This will render Markdown such that the spacing and alignment in the source
text and the rendered content looks roughly the same. It's meant to help ensure
that what's typed is very close to what's viewed when rendered.
"""
from __future__ import absolute_import, unicode_literals
import re
from collections import OrderedDict
import markdown
from django.utils import six
from django.utils.six.moves import range
from markdown.blockprocessors import BlockProcessor, OListProcessor
from markdown.postprocessors import RawHtmlPostprocessor
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree

class SmartEmptyBlockProcessor(BlockProcessor):
    """Handles empty blocks in a more specialized way.

    By default, Python-Markdown will trim away excess empty blocks, with
    the idea being that it doesn't matter how much whitespace exists
    between tags when rendered to HTML. However, in our case, we need to
    preserve whitespace in order to better match the resulting render to
    the input text.

    We replace any empty lines with paragraph tags, which will safely stick
    around.

    This is invoked before EmptyBlockProcessor.
    """

    def test(self, parent, block):
        """Test that the processor should apply to the given block."""
        return not block or block.startswith(b'\n')

    def run(self, parent, blocks):
        """Run the processor on the given blocks."""
        block = blocks.pop(0)
        while self.test(parent, block):
            etree.SubElement(parent, b'p')
            if block:
                block = block[1:]
            else:
                etree.SubElement(parent, b'p')
                return

        blocks.insert(0, block)


class PreserveStartOListBlockProcessor(OListProcessor):
    """Applies CSS styles to any <ol> with a start= attribute.

    This allows for CSS tricks to be performed that ensure that ordered list
    item numbers and item contents line up between source text and rendered
    text. It basically turns off the <li>'s native counter value and instead
    creates its own using :before and CSS counters. These tricks end up causing
    the start= attribute on the <ol> to be ignored.

    This block processor extends the standard OListProcessor to also apply
    a CSS style to set the displayed counter value to the intended start
    value.

    This replaces OListProcessor.
    """

    def run(self, parent, blocks):
        """Run the processor on the given blocks."""
        OListProcessor.run(self, parent, blocks)
        list_el = self.lastChild(parent)
        if list_el.tag == b'ol' and b'start' in list_el.attrib:
            try:
                start = int(list_el.attrib[b'start'])
            except ValueError:
                start = 1

            if start > 1:
                list_el.attrib[b'style'] = b'counter-reset: li %s' % (start - 1)


class TrimTrailingEmptyParagraphs(Treeprocessor):
    """Removes empty paragraphs from the end of the tree.

    This will remove any trailing empty paragraphs formerly added by
    SmartEmptyBlockProcessor. This step must be done after all the blocks are
    processed, so that we have a complete picture of the state of the tree.
    It's therefore performed right before we prettify the tree.
    """

    def run(self, root):
        """Run the processor on the root of the tree."""
        num_children = len(root)
        start_i = num_children
        for child in reversed(root):
            if child.tag != b'p' or child.text or len(child) > 0:
                break
            start_i -= 1

        if start_i < num_children:
            root[start_i:] = []


class TrimmedRawHtmlPostprocessor(RawHtmlPostprocessor):
    """Post-processes raw HTML placeholders, without adding extra newlines.

    Python-Markdown's RawHtmlPostprocessor had a nasty habit of adding an
    extra newline after replacing a placeholder with stored raw HTML. That
    would cause extra newlines to appear in our output. It also (at least
    as of Python-Markdown 2.6 -- the latest release at the time of this
    writing) wasn't very efficient, unnecessarily comparing strings and
    fetching results from the same functions on every loop.

    This version more efficiently replaces the raw HTML placeholders and
    ensures there are no trailing newlines in the resulting HTML. Not only does
    it prevent the newline normally added by the original function, but it
    strips trailing newlines from stashed HTML that may have been generated
    by other extensions, keeping spacing consistent and predictable.
    """

    def run(self, text):
        """Run the processor on the HTML.

        Args:
            text (unicode):
                The text to process.

        Returns:
            unicode:
            The processed text.
        """
        html_stash = self.markdown.htmlStash
        if html_stash.html_counter == 0:
            return text
        else:
            safe_mode = getattr(self.markdown, b'safeMode', None)
            should_escape = False
            should_remove = False
            if safe_mode:
                safe_mode = safe_mode.lower()
                if safe_mode == b'escape':
                    should_escape = True
                elif safe_mode == b'remove':
                    should_remove = True
            replacements = OrderedDict()
            for i in range(html_stash.html_counter):
                html, safe = html_stash.rawHtmlBlocks[i]
                placeholder = html_stash.get_placeholder(i)
                html = html.rstrip(b'\n')
                if not safe:
                    if should_escape:
                        html = self.escape(html)
                    elif should_remove:
                        html = b''
                    else:
                        html = self.markdown.html_replacement_text
                if self.isblocklevel(html) and (safe or not safe_mode):
                    replacements[b'<p>%s</p>' % placeholder] = html
                replacements[placeholder] = html

            return re.sub((b'|').join(re.escape(key) for key in replacements), lambda m: replacements[m.group(0)], text)


class WysiwygFormattingExtension(markdown.Extension):
    """Provides a series of WYSIWYG formatting rules for Markdown rendering.

    We have a lot of specific rendering concerns that Python-Markdown doesn't
    really address, or generally need to care about. We try very hard to match
    up newlines around various code blocks, and we have special ways we do
    ordered lists. The resulting rendered output is meant to look identical
    to the input text, as much as possible.

    This extension renders a series of processors that ensures that the HTML
    output is in the format required for our rendering.

    This is meant to be used with the following Markdown configuration
    and extensions:

    .. code-block:: python

        {
            'lazy_ol': False,
            'extensions': [
                'sane_lists', 'nl2br', 'djblets.markdown.extentions.wysiwyg',
            ],
        }
    """

    def extendMarkdown(self, md, md_globals):
        """Extend the list of Markdown processors.

        Each processor in this file will be registered in the order
        necessary for the smarter formatting.
        """
        md.parser.blockprocessors[b'olist'] = PreserveStartOListBlockProcessor(md.parser)
        md.parser.blockprocessors.add(b'smart-empty', SmartEmptyBlockProcessor(md.parser), b'<empty')
        md.treeprocessors.add(b'trim_empty_p', TrimTrailingEmptyParagraphs(md), b'<prettify')
        md.postprocessors[b'raw_html'] = TrimmedRawHtmlPostprocessor(md)


def makeExtension(*args, **kwargs):
    """Create and return an instance of this extension.

    Args:
        *args (tuple):
            Positional arguments for the extension.

        **kwargs (dict):
            Keyword arguments for the extension.
    """
    return WysiwygFormattingExtension(*args, **kwargs)