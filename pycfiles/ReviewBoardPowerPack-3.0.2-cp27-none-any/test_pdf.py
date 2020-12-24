# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/pdf/tests/test_pdf.py
# Compiled at: 2019-06-17 15:11:31
"""Unit tests for PDF review."""
from __future__ import unicode_literals
from reviewboard.site.urlresolvers import local_site_reverse
from rbpowerpack.testing.testcases import PowerPackExtensionTestCase

class PDFTests(PowerPackExtensionTestCase):
    """Tests for PDF functionality."""

    def test_pdf_diff_url_resolver(self):
        """Testing resolution of PDF diff URLs"""
        self.assertEqual(local_site_reverse(b'powerpack-pdf-diff', kwargs={b'old_attachment_id': 5, 
           b'new_attachment_id': 6}), b'/pdf/diff/5-6/')
        self.assertEqual(local_site_reverse(b'powerpack-pdf-diff', local_site_name=b'test-site', kwargs={b'old_attachment_id': 5, 
           b'new_attachment_id': 6}), b'/s/test-site/pdf/diff/5-6/')