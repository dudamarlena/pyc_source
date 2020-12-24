# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_djblets_image_tags.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.templatetags.djblets_images."""
from __future__ import unicode_literals
from collections import OrderedDict
from django.template import Context, Template, TemplateSyntaxError
from djblets.testing.testcases import TestCase

class SrcSetTagTests(TestCase):
    """Unit tests for the {% srcset %} template tag."""

    def test_with_valid_sources(self):
        """Testing {% srcset %} with valid sources"""
        t = Template(b'{% load djblets_images %}<img srcset="{% srcset sources %}">')
        self.assertEqual(t.render(Context({b'sources': {b'1x': b'/path/to/image.png', 
                        b'2x': b'/path/to/image@2x.png', 
                        b'3x': b'/path/to/image@3x.png', 
                        b'10w': b'/path/to/image@10w.png'}})), b'<img srcset="/path/to/image.png 1x, /path/to/image@2x.png 2x, /path/to/image@3x.png 3x, /path/to/image@10w.png 10w">')

    def test_with_invalid_sources(self):
        """Testing {% srcset %} with invalid sources"""
        t = Template(b'{% load djblets_images %}<img srcset="{% srcset sources %}">')
        message = b'"ax" is not a valid srcset size descriptor.'
        with self.assertRaisesMessage(TemplateSyntaxError, message):
            t.render(Context({b'sources': {b'ax': b'/path/to/image.png'}}))

    def test_sorts(self):
        """Testing {% srcset %} sorts sources"""
        t = Template(b'{% load djblets_images %}<img srcset="{% srcset sources %}">')
        sources = OrderedDict()
        sources[b'100w'] = b'/path/to/image@100w.png'
        sources[b'10w'] = b'/path/to/image@10w.png'
        sources[b'3x'] = b'/path/to/image@3x.png'
        sources[b'1x'] = b'/path/to/image.png'
        sources[b'2x'] = b'/path/to/image@2x.png'
        sources[b'20w'] = b'/path/to/image@20w.png'
        sources[b'1.5x'] = b'/path/to/image@1.5x.png'
        sources[b'2w'] = b'/path/to/image@2w.png'
        sources[b'10x'] = b'/path/to/image@10x.png'
        self.assertEqual(t.render(Context({b'sources': sources})), b'<img srcset="/path/to/image.png 1x, /path/to/image@1.5x.png 1.5x, /path/to/image@2x.png 2x, /path/to/image@3x.png 3x, /path/to/image@10x.png 10x, /path/to/image@2w.png 2w, /path/to/image@10w.png 10w, /path/to/image@20w.png 20w, /path/to/image@100w.png 100w">')


class ImageSourceAttrsTagTests(TestCase):
    """Unit tests for the {% image_source_attrs %} template tag."""

    def test_with_valid_sources(self):
        """Testing {% image_source_attrs %} with valid sources"""
        t = Template(b'{% load djblets_images %}<img {% image_source_attrs %}\n      1x /path/to/image.png\n      2x /path/to/image@2x.png\n      3x /path/to/image@3x.png\n      10w /path/to/image@10w.png\n     {% end_image_source_attrs %}>')
        self.assertEqual(t.render(Context()), b'<img src="/path/to/image.png" srcset="/path/to/image.png 1x, /path/to/image@2x.png 2x, /path/to/image@3x.png 3x, /path/to/image@10w.png 10w">')

    def test_with_invalid_sources(self):
        """Testing {% image_source_attrs %} with invalid sources definition"""
        t = Template(b'{% load djblets_images %}<img {% image_source_attrs %}\n      /path/to/image.png\n      2x /path/to/image@2x.png\n     {% end_image_source_attrs %}>')
        message = b'The source definition passed to {% image_source_attrs %} is not structured correctly. Make sure that there is one source definition per line and that it contains a descriptor and a URL.'
        with self.assertRaisesMessage(TemplateSyntaxError, message):
            t.render(Context())

    def test_with_no_1x(self):
        """Testing {% image_source_attrs %} with no 1x source"""
        t = Template(b'{% load djblets_images %}<img {% image_source_attrs %}\n      2x /path/to/image@2x.png\n      3x /path/to/image@3x.png\n     {% end_image_source_attrs %}>')
        message = b'The source definition passed to {% image_source_attr %} must contain a "1x" descriptor.'
        with self.assertRaisesMessage(TemplateSyntaxError, message):
            t.render(Context())