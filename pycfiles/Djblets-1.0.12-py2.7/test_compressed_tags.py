# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_compressed_tags.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.templatetags.djblets_forms."""
from __future__ import unicode_literals
from django.template import Context, Template
from pipeline.conf import settings as pipeline_settings
from djblets.testing.testcases import TestCase

class CompressedTagsTests(TestCase):
    """Unit tests for the {% compressed_* %} template tags."""

    def test_compressed_css_tag(self):
        """Testing {% compressed_css %}"""
        pipeline_settings.STYLESHEETS = {b'test': {b'source_filenames': [], b'output_filename': b'test.css'}}
        t = Template(b'{% load compressed %}{% compressed_css "test" %}')
        self.assertEqual(t.render(Context({b'test': b'test'})), b'/test.css\n')

    def test_compressed_js_tag(self):
        """Testing {% compressed_js %}"""
        pipeline_settings.JAVASCRIPT = {b'test': {b'source_filenames': [], b'output_filename': b'test.js'}}
        t = Template(b'{% load compressed %}{% compressed_js "test" %}')
        self.assertEqual(t.render(Context({b'test': b'test'})), b'/test.js\n')