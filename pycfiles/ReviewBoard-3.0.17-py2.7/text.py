# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/ui/text.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging
from django.template.context import Context
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from djblets.cache.backend import cache_memoize
from pygments import highlight
from pygments.lexers import ClassNotFound, guess_lexer_for_filename, TextLexer
from reviewboard.attachments.models import FileAttachment
from reviewboard.diffviewer.chunk_generator import NoWrapperHtmlFormatter, RawDiffChunkGenerator
from reviewboard.diffviewer.diffutils import get_chunks_in_range
from reviewboard.reviews.ui.base import FileAttachmentReviewUI

class TextBasedReviewUI(FileAttachmentReviewUI):
    """A Review UI for text-based files.

    This renders the text file, applying syntax highlighting, and allows users
    to comment on one or more lines.
    """
    name = b'Text'
    object_key = b'text'
    supported_mimetypes = [b'text/*']
    template_name = b'reviews/ui/text.html'
    comment_thumbnail_template_name = b'reviews/ui/text_comment_thumbnail.html'
    can_render_text = False
    supports_diffing = True
    source_chunk_generator_cls = RawDiffChunkGenerator
    rendered_chunk_generator_cls = RawDiffChunkGenerator
    extra_css_classes = []
    js_model_class = b'RB.TextBasedReviewable'
    js_view_class = b'RB.TextBasedReviewableView'

    def get_js_model_data(self):
        data = super(TextBasedReviewUI, self).get_js_model_data()
        data[b'hasRenderedView'] = self.can_render_text
        if self.can_render_text:
            data[b'viewMode'] = b'rendered'
        else:
            data[b'viewMode'] = b'source'
        return data

    def get_extra_context(self, request):
        context = {}
        diff_type_mismatch = False
        if self.diff_against_obj:
            diff_against_review_ui = self.diff_against_obj.review_ui
            context.update({b'diff_caption': self.diff_against_obj.caption, 
               b'diff_filename': self.diff_against_obj.filename, 
               b'diff_revision': self.diff_against_obj.attachment_revision})
            if type(self) != type(diff_against_review_ui):
                diff_type_mismatch = True
            else:
                chunk_generator = self._get_source_diff_chunk_generator()
                context[b'source_chunks'] = chunk_generator.get_chunks()
                chunk_generator = self._get_rendered_diff_chunk_generator()
                context[b'rendered_chunks'] = chunk_generator.get_chunks()
        else:
            file_line_list = [ mark_safe(line) for line in self.get_text_lines()
                             ]
            rendered_line_list = [ mark_safe(line) for line in self.get_rendered_lines()
                                 ]
            context.update({b'text_lines': file_line_list, 
               b'rendered_lines': rendered_line_list})
        if self.obj.attachment_history is not None:
            num_revisions = FileAttachment.objects.filter(attachment_history=self.obj.attachment_history).count()
        else:
            num_revisions = 1
        context.update({b'filename': self.obj.filename, 
           b'revision': self.obj.attachment_revision, 
           b'is_diff': self.diff_against_obj is not None, 
           b'num_revisions': num_revisions, 
           b'diff_type_mismatch': diff_type_mismatch})
        return context

    def get_text(self):
        """Return the file contents as a string.

        This will fetch the file and then cache it for future renders.
        """
        return cache_memoize(b'text-attachment-%d-string' % self.obj.pk, self._get_text_uncached)

    def get_text_lines(self):
        """Return the file contents as syntax-highlighted lines.

        This will fetch the file, render it however appropriate for the review
        UI, and split it into reviewable lines. It will then cache it for
        future renders.
        """
        return cache_memoize(b'text-attachment-%d-lines' % self.obj.pk, lambda : list(self.generate_highlighted_text()))

    def get_rendered_lines(self):
        """Returns the file contents as a render, based on the raw text.

        If a subclass sets ``can_render_text = True`` and implements
        ``generate_render``, then this will render the contents in some
        specialized form, cache it as a list of lines, and return it.
        """
        if self.can_render_text:
            return cache_memoize(b'text-attachment-%d-rendered' % self.obj.pk, lambda : list(self.generate_render()))
        else:
            return []

    def _get_text_uncached(self):
        """Return the text from the file."""
        self.obj.file.open()
        with self.obj.file as (f):
            data = f.read()
        return data

    def generate_highlighted_text(self):
        """Generates syntax-highlighted text for the file.

        This will render the text file to HTML, applying any syntax
        highlighting that's appropriate. The contents will be split into
        reviewable lines and will be cached for future renders.
        """
        data = self.get_text()
        lexer = self.get_source_lexer(self.obj.filename, data)
        lines = highlight(data, lexer, NoWrapperHtmlFormatter()).splitlines()
        return [ b'<pre>%s</pre>' % line for line in lines
               ]

    def get_source_lexer(self, filename, data):
        """Returns the lexer that should be used for the text.

        By default, this will attempt to guess the lexer based on the
        filename, falling back to a plain-text lexer.

        Subclasses can override this to choose a more specific lexer.
        """
        try:
            return guess_lexer_for_filename(filename, data)
        except ClassNotFound:
            return TextLexer()

    def generate_render(self):
        """Generates a render of the text.

        By default, this won't do anything. Subclasses should override it
        to turn the raw text into some form of rendered content. For
        example, rendering Markdown.
        """
        raise NotImplementedError

    def serialize_comments(self, comments):
        """Return a dictionary of the comments for this file attachment."""
        result = {}
        for comment in comments:
            try:
                key = b'%s-%s' % (comment.extra_data[b'beginLineNum'],
                 comment.extra_data[b'endLineNum'])
            except KeyError:
                continue

            result.setdefault(key, []).append(self.serialize_comment(comment))

        return result

    def get_comment_thumbnail(self, comment):
        """Generates and returns a thumbnail representing this comment.

        This will find the appropriate lines the comment applies to and
        return it as HTML suited for rendering in reviews.
        """
        try:
            begin_line_num = int(comment.extra_data[b'beginLineNum'])
            end_line_num = int(comment.extra_data[b'endLineNum'])
            view_mode = comment.extra_data[b'viewMode']
        except (KeyError, ValueError):
            return

        return cache_memoize(b'text-review-ui-comment-thumbnail-%s-%s' % (self.obj.pk,
         comment.pk), lambda : self.render_comment_thumbnail(comment, begin_line_num, end_line_num, view_mode))

    def render_comment_thumbnail(self, comment, begin_line_num, end_line_num, view_mode):
        """Renders the content of a comment thumbnail.

        This will, by default, call render() and then pull out the lines
        that were commented on.

        Subclasses can override to do more specialized thumbnail rendering.
        """
        if view_mode not in ('source', 'rendered'):
            logging.warning(b'Unexpected view mode "%s" when rendering comment thumbnail.', view_mode)
            return b''
        else:
            context = {b'is_diff': self.diff_against_obj is not None, 
               b'review_ui': self, 
               b'revision': self.obj.attachment_revision}
            if self.diff_against_obj:
                if view_mode == b'source':
                    chunk_generator = self._get_source_diff_chunk_generator()
                elif view_mode == b'rendered':
                    chunk_generator = self._get_rendered_diff_chunk_generator()
                chunks = get_chunks_in_range(chunk_generator.get_chunks(), begin_line_num, end_line_num - begin_line_num + 1)
                context.update({b'chunks': chunks, 
                   b'diff_revision': self.diff_against_obj.attachment_revision})
            else:
                try:
                    if view_mode == b'source':
                        lines = self.get_text_lines()
                    elif view_mode == b'rendered':
                        lines = self.get_rendered_lines()
                except Exception as e:
                    logging.error(b'Unable to generate text attachment comment thumbnail for comment %s: %s', comment, e)
                    return b''

                lines = lines[begin_line_num - 1:end_line_num]
                context[b'lines'] = [ {b'line_num': begin_line_num + i, b'text': mark_safe(line)} for i, line in enumerate(lines)
                                    ]
            return render_to_string(self.comment_thumbnail_template_name, Context(context))

    def get_comment_link_url(self, comment):
        """Returns the URL to the file and line commented on.

        This will link to the correct file, view mode, and line for the
        given comment.
        """
        base_url = super(TextBasedReviewUI, self).get_comment_link_url(comment)
        try:
            begin_line_num = int(comment.extra_data[b'beginLineNum'])
            view_mode = comment.extra_data[b'viewMode']
        except (KeyError, ValueError):
            return base_url

        return b'%s#%s/line%s' % (base_url, view_mode, begin_line_num)

    def _get_diff_chunk_generator(self, chunk_generator_cls, orig, modified):
        """Return a chunk generator showing a diff for the text.

        The chunk generator will diff the text of this attachment against
        the text of the attachment being diffed against.

        This is used both for displaying the file attachment and
        rendering the thumbnail.
        """
        assert self.diff_against_obj
        return chunk_generator_cls(orig, modified, self.obj.filename, self.diff_against_obj.filename)

    def _get_source_diff_chunk_generator(self):
        """Return a chunk generator for diffing source text."""
        return self._get_diff_chunk_generator(self.source_chunk_generator_cls, self.diff_against_obj.review_ui.get_text(), self.get_text())

    def _get_rendered_diff_chunk_generator(self):
        """Return a chunk generator for diffing rendered text."""
        return self._get_diff_chunk_generator(self.rendered_chunk_generator_cls, self.diff_against_obj.review_ui.get_rendered_lines(), self.get_rendered_lines())