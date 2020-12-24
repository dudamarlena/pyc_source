# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/renderers.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string
from django.utils import six
from django.utils.translation import ugettext as _, get_language
from djblets.cache.backend import cache_memoize
from reviewboard.diffviewer.chunk_generator import compute_chunk_last_header
from reviewboard.diffviewer.diffutils import populate_diff_chunks
from reviewboard.diffviewer.errors import UserVisibleError

class DiffRenderer(object):
    """Renders a file's diffs.

    A DiffRenderer is constructed as needed and set up for render, and then
    thrown away. The rendered diff can show that of a whole file (in a
    collapsed or fully expanded state), or a particular chunk within a file.

    The rendered diff will be optimistically pulled out of cache, if it
    exists. Otherwise, a new one will be rendered and placed in the cache.

    The diff_file (from get_diff_files) is the only required parameter.
    The renderer may modify the contents of this, and should make a copy if
    it needs to be left untouched.

    Note that any of the render functions are meant to be called only once per
    DiffRenderer. It will alter the state of the renderer, possibly
    disrupting future render calls.
    """
    default_template_name = b'diffviewer/diff_file_fragment.html'

    def __init__(self, diff_file, chunk_index=None, highlighting=False, collapse_all=True, lines_of_context=None, extra_context=None, allow_caching=True, template_name=default_template_name, show_deleted=False):
        self.diff_file = diff_file
        self.chunk_index = chunk_index
        self.highlighting = highlighting
        self.collapse_all = collapse_all
        self.lines_of_context = lines_of_context
        self.extra_context = extra_context or {}
        self.allow_caching = allow_caching
        self.template_name = template_name
        self.num_chunks = 0
        self.show_deleted = show_deleted
        if self.lines_of_context and len(self.lines_of_context) == 1:
            self.lines_of_context.append(self.lines_of_context[0])

    def render_to_response(self, request):
        """Renders the diff to an HttpResponse."""
        return HttpResponse(self.render_to_string(request))

    def render_to_string(self, request):
        """Returns the diff as a string.

        The resulting diff may optimistically be pulled from the cache, if
        not rendering a custom line range. This makes diff rendering very
        quick.

        If operating with a cache, and the diff doesn't exist in the cache,
        it will be stored after render.
        """
        cache = self.allow_caching and not self.lines_of_context
        if cache:
            return cache_memoize(self.make_cache_key(), lambda : self.render_to_string_uncached(request), large_data=True)
        else:
            return self.render_to_string_uncached(request)

    def render_to_string_uncached(self, request):
        """Renders a diff to a string without caching.

        This is a potentially expensive operation, and so is meant to be called
        only as often as necessary. render_to_string will call this if it's
        not already in the cache.
        """
        if not self.diff_file.get(b'chunks_loaded', False):
            populate_diff_chunks([self.diff_file], self.highlighting, request=request)
        if self.chunk_index is not None:
            assert not self.lines_of_context or self.collapse_all
            self.num_chunks = len(self.diff_file[b'chunks'])
            if self.chunk_index < 0 or self.chunk_index >= self.num_chunks:
                raise UserVisibleError(_(b'Invalid chunk index %s specified.') % self.chunk_index)
        return render_to_string(self.template_name, Context(self.make_context()))

    def make_cache_key(self):
        """Creates and returns a cache key representing the diff to render."""
        filediff = self.diff_file[b'filediff']
        key = b'%s-%s-%s-' % (self.template_name,
         self.diff_file[b'index'],
         filediff.diffset.revision)
        if self.diff_file[b'force_interdiff']:
            interfilediff = self.diff_file[b'interfilediff']
            key += b'interdiff-%s-' % filediff.pk
            if interfilediff:
                key += six.text_type(interfilediff.pk)
            else:
                key += b'none'
        else:
            key += six.text_type(filediff.pk)
        if self.chunk_index is not None:
            key += b'-chunk-%s' % self.chunk_index
        if self.collapse_all:
            key += b'-collapsed'
        if self.highlighting:
            key += b'-highlighting'
        if self.show_deleted:
            key += b'-show_deleted'
        key += b'-%s-%s' % (get_language(), settings.TEMPLATE_SERIAL)
        return key

    def make_context(self):
        """Creates and returns context for a diff render."""
        context = self.extra_context.copy()
        if self.chunk_index is not None:
            self.diff_file[b'chunks'] = [
             self.diff_file[b'chunks'][self.chunk_index]]
            if self.lines_of_context:
                chunk = self.diff_file[b'chunks'][0]
                lines = chunk[b'lines']
                num_lines = len(lines)
                new_lines = []
                total_lines_of_context = self.lines_of_context[0] + self.lines_of_context[1]
                if total_lines_of_context >= num_lines:
                    self.collapse_all = False
                else:
                    self.lines_of_context[0] = min(num_lines, self.lines_of_context[0])
                    self.lines_of_context[1] = min(num_lines, self.lines_of_context[1])
                    collapse_i = 0
                    if self.chunk_index < self.num_chunks - 1:
                        chunk2_i = max(num_lines - self.lines_of_context[1], 0)
                    else:
                        chunk2_i = num_lines
                    meta = chunk[b'meta']
                    if self.lines_of_context[0] and self.chunk_index > 0:
                        collapse_i = self.lines_of_context[0]
                        self.diff_file[b'chunks'].insert(0, {b'change': chunk[b'change'], 
                           b'collapsable': False, 
                           b'index': self.chunk_index, 
                           b'lines': lines[:collapse_i], 
                           b'meta': meta, 
                           b'numlines': collapse_i})
                    new_lines += lines[collapse_i:chunk2_i]
                    if self.chunk_index < self.num_chunks - 1 and chunk2_i + self.lines_of_context[1] <= num_lines:
                        self.diff_file[b'chunks'].append({b'change': chunk[b'change'], 
                           b'collapsable': False, 
                           b'index': self.chunk_index, 
                           b'lines': lines[chunk2_i:], 
                           b'meta': meta, 
                           b'numlines': num_lines - chunk2_i})
                    if new_lines:
                        num_lines = len(new_lines)
                        chunk.update({b'lines': new_lines, 
                           b'numlines': num_lines, 
                           b'collapsable': True})
                        if self.chunk_index < self.num_chunks - 1:
                            for prefix, index in (('left', 1), ('right', 4)):
                                meta[prefix + b'_headers'] = [ header for header in meta[(prefix + b'_headers')] if header[0] <= new_lines[(-1)][index]
                                                             ]

                            meta[b'headers'] = compute_chunk_last_header(new_lines, num_lines, meta)
                    else:
                        self.diff_file[b'chunks'].remove(chunk)
        equal_lines = 0
        for chunk in self.diff_file[b'chunks']:
            if chunk[b'change'] == b'equal':
                equal_lines += chunk[b'numlines']

        context.update({b'collapseall': self.collapse_all, 
           b'file': self.diff_file, 
           b'lines_of_context': self.lines_of_context or (0, 0), 
           b'equal_lines': equal_lines, 
           b'standalone': self.chunk_index is not None, 
           b'show_deleted': self.show_deleted})
        return context


_diff_renderer_class = DiffRenderer

def get_diff_renderer_class():
    """Returns the DiffRenderer class used for rendering diffs."""
    return _diff_renderer_class


def set_diff_renderer_class(renderer):
    """Sets the DiffRenderer class used for rendering diffs."""
    assert renderer
    globals()[b'_diff_renderer_class'] = renderer


def get_diff_renderer(*args, **kwargs):
    """Returns a DiffRenderer instance used for rendering diffs."""
    return _diff_renderer_class(*args, **kwargs)