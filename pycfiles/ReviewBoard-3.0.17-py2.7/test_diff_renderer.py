# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_diff_renderer.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.http import HttpResponse
from django.test import RequestFactory
from djblets.cache.backend import cache_memoize
from kgb import SpyAgency
from reviewboard.diffviewer.errors import UserVisibleError
from reviewboard.diffviewer.models import FileDiff
from reviewboard.diffviewer.renderers import DiffRenderer
from reviewboard.testing import TestCase

class DiffRendererTests(SpyAgency, TestCase):
    """Unit tests for DiffRenderer."""

    def test_construction_with_invalid_chunks(self):
        """Testing DiffRenderer construction with invalid chunks"""
        diff_file = {b'chunks': [{}], b'filediff': None, 
           b'interfilediff': None, 
           b'force_interdiff': False, 
           b'chunks_loaded': True}
        renderer = DiffRenderer(diff_file, chunk_index=-1)
        self.assertRaises(UserVisibleError, lambda : renderer.render_to_string_uncached(None))
        renderer = DiffRenderer(diff_file, chunk_index=1)
        self.assertRaises(UserVisibleError, lambda : renderer.render_to_string_uncached(None))
        return

    def test_construction_with_valid_chunks(self):
        """Testing DiffRenderer construction with valid chunks"""
        diff_file = {b'chunks': [{}], b'chunks_loaded': True}
        renderer = DiffRenderer(diff_file, chunk_index=0)
        self.spy_on(renderer.render_to_string, call_original=False)
        self.spy_on(renderer.make_context, call_original=False)
        renderer.render_to_string_uncached(None)
        self.assertEqual(renderer.num_chunks, 1)
        self.assertEqual(renderer.chunk_index, 0)
        return

    def test_render_to_response(self):
        """Testing DiffRenderer.render_to_response"""
        diff_file = {b'chunks': [{}]}
        renderer = DiffRenderer(diff_file)
        self.spy_on(renderer.render_to_string, call_fake=lambda self, request: b'Foo')
        request_factory = RequestFactory()
        request = request_factory.get(b'/')
        response = renderer.render_to_response(request)
        self.assertTrue(renderer.render_to_string.called)
        self.assertTrue(isinstance(response, HttpResponse))
        self.assertEqual(response.content, b'Foo')

    def test_render_to_string(self):
        """Testing DiffRenderer.render_to_string"""
        diff_file = {b'chunks': [{}]}
        renderer = DiffRenderer(diff_file)
        self.spy_on(renderer.render_to_string_uncached, call_fake=lambda self, request: b'Foo')
        self.spy_on(renderer.make_cache_key, call_fake=lambda self: b'my-cache-key')
        self.spy_on(cache_memoize)
        request_factory = RequestFactory()
        request = request_factory.get(b'/')
        response = renderer.render_to_response(request)
        self.assertEqual(response.content, b'Foo')
        self.assertTrue(renderer.render_to_string_uncached.called)
        self.assertTrue(renderer.make_cache_key.called)
        self.assertTrue(cache_memoize.spy.called)

    def test_render_to_string_uncached(self):
        """Testing DiffRenderer.render_to_string_uncached"""
        diff_file = {b'chunks': [{}]}
        renderer = DiffRenderer(diff_file, lines_of_context=[5, 5])
        self.spy_on(renderer.render_to_string_uncached, call_fake=lambda self, request: b'Foo')
        self.spy_on(renderer.make_cache_key, call_fake=lambda self: b'my-cache-key')
        self.spy_on(cache_memoize)
        request_factory = RequestFactory()
        request = request_factory.get(b'/')
        response = renderer.render_to_response(request)
        self.assertEqual(response.content, b'Foo')
        self.assertTrue(renderer.render_to_string_uncached.called)
        self.assertFalse(renderer.make_cache_key.called)
        self.assertFalse(cache_memoize.spy.called)

    def test_make_context_with_chunk_index(self):
        """Testing DiffRenderer.make_context with chunk_index"""
        diff_file = {b'newfile': True, 
           b'interfilediff': None, 
           b'filediff': FileDiff(), 
           b'chunks': [
                     {b'lines': [], b'meta': {}, b'change': b'insert'},
                     {b'lines': range(10), 
                        b'meta': {}, b'change': b'replace'},
                     {b'lines': [], b'meta': {}, b'change': b'delete'}]}
        renderer = DiffRenderer(diff_file, chunk_index=1)
        context = renderer.make_context()
        self.assertEqual(context[b'standalone'], True)
        self.assertEqual(context[b'file'], diff_file)
        self.assertEqual(len(diff_file[b'chunks']), 1)
        chunk = diff_file[b'chunks'][0]
        self.assertEqual(chunk[b'change'], b'replace')
        return