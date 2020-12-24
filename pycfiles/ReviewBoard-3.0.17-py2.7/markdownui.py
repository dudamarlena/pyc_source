# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/ui/markdownui.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging
from django.utils.translation import ugettext as _
from djblets.markdown import iter_markdown_lines
from pygments.lexers import TextLexer
from reviewboard.reviews.chunk_generators import MarkdownDiffChunkGenerator
from reviewboard.reviews.ui.text import TextBasedReviewUI
from reviewboard.reviews.markdown_utils import render_markdown_from_file

class MarkdownReviewUI(TextBasedReviewUI):
    """A Review UI for markdown files.

    This renders the markdown to HTML, and allows users to comment on each
    top-level block (header, paragraph, list, code block, etc).
    """
    supported_mimetypes = [
     b'text/x-markdown']
    object_key = b'markdown'
    can_render_text = True
    rendered_chunk_generator_cls = MarkdownDiffChunkGenerator
    extra_css_classes = [
     b'markdown-review-ui']
    js_view_class = b'RB.MarkdownReviewableView'

    def generate_render(self):
        with self.obj.file as (f):
            f.open()
            rendered = render_markdown_from_file(f)
        try:
            for line in iter_markdown_lines(rendered):
                yield line

        except Exception as e:
            logging.error(b'Failed to parse resulting Markdown XHTML for file attachment %d: %s', self.obj.pk, e, exc_info=True)
            yield _(b'Error while rendering Markdown content: %s') % e

    def get_source_lexer(self, filename, data):
        return TextLexer()