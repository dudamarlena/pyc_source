# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/forms/tests/test_copyable_text_input.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.forms.widgets.CopyableTextInput."""
from __future__ import unicode_literals
from django import forms
from djblets.forms.widgets import CopyableTextInput
from djblets.testing.testcases import TestCase

class CopyableTextInputTests(TestCase):
    """Unit tests for djblets.forms.widgets.CopyableTextInput."""

    def test_render(self):
        """Testing CopyableTextInput.render"""
        field = forms.CharField(widget=CopyableTextInput())
        rendered = field.widget.render(name=b'my_field', value=b'test', attrs={b'id': b'id_my_field'})
        self.assertIn(b'class="copyable-text-input-link"', rendered)
        self.assertIn(b'data-field-id="id_my_field"', rendered)
        self.assertIn(b'title="Copy to clipboard"', rendered)