# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/forms/tests/test_list_edit_widget.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.forms.widgets.ListEditWidget."""
from __future__ import unicode_literals
from django import forms
from djblets.forms.widgets import ListEditWidget
from djblets.testing.testcases import TestCase

class ListEditWidgetTests(TestCase):
    """Unit tests for djblets.forms.widgets.ListEditWidget."""

    def test_render(self):
        """Testing ListEditWidget.render"""
        field = forms.CharField(widget=ListEditWidget())
        rendered = field.widget.render(name=b'my_field', value=b' foo,  bar , baz ', attrs={b'id': b'id_my_field', 
           b'class': b'my-value-class'})
        self.assertIn(b'<div class="list-edit-widget" id="id_my_field_container">', rendered)
        self.assertIn(b'<input value="foo" type="text" class="my-value-class list-edit-item">', rendered)
        self.assertIn(b'<input value="bar" type="text" class="my-value-class list-edit-item">', rendered)
        self.assertIn(b'<input value="baz" type="text" class="my-value-class list-edit-item">', rendered)

    def test_render_with_custom_separator(self):
        """Testing ListEditWidget.render with custom separator"""
        field = forms.CharField(widget=ListEditWidget(sep=b';'))
        rendered = field.widget.render(name=b'my_field', value=b' foo;  bar ; baz ', attrs={b'id': b'id_my_field', 
           b'class': b'my-value-class'})
        self.assertIn(b'<div class="list-edit-widget" id="id_my_field_container">', rendered)
        self.assertIn(b'<input value="foo" type="text" class="my-value-class list-edit-item">', rendered)
        self.assertIn(b'<input value="bar" type="text" class="my-value-class list-edit-item">', rendered)
        self.assertIn(b'<input value="baz" type="text" class="my-value-class list-edit-item">', rendered)