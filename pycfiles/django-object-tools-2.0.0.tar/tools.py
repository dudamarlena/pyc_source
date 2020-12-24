# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/silly/dev/django-object-tools/object_tools/tests/tools.py
# Compiled at: 2018-12-21 02:57:07
from __future__ import unicode_literals
from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
import object_tools

class TestForm(forms.Form):
    pass


class TestMediaForm(forms.Form):
    media_field = forms.fields.DateTimeField(widget=AdminSplitDateTime)


class TestTool(object_tools.ObjectTool):
    name = b'test_tool'
    label = b'Test Tool'
    form_class = TestForm

    def view(self, request, extra_context=None):
        pass


class TestMediaTool(object_tools.ObjectTool):
    name = b'test_media_tool'
    label = b'Test Media Tool'
    form_class = TestMediaForm

    def view(self, request, extra_context=None):
        pass


class TestInvalidTool(object_tools.ObjectTool):
    pass


object_tools.tools.register(TestTool)
object_tools.tools.register(TestMediaTool)