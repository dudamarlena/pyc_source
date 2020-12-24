# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/slam/workspace/django-editor/editor/admin.py
# Compiled at: 2013-03-19 05:26:46
from django.db import models
from django.contrib import admin
from django.forms.widgets import Textarea
from django.conf import settings
rich_text_module = None
if 'imperavi' in settings.INSTALLED_APPS:
    try:
        from imperavi.admin import ImperaviAdmin, ImperaviStackedInlineAdmin, ImperaviWidget
        rich_text_module = 'imperavi'
    except ImportError:
        rich_text_module = None

if not rich_text_module and 'tinymce' in settings.INSTALLED_APPS:
    try:
        from tinymce.widgets import TinyMCE
        rich_text_module = 'tinymce'
    except ImportError:
        rich_text_module = None

if rich_text_module == 'imperavi':
    StackedInline = ImperaviStackedInlineAdmin
    Admin = ImperaviAdmin
    Widget = ImperaviWidget
else:
    StackedInline = admin.StackedInline
    Admin = admin.ModelAdmin
    if rich_text_module == 'tinymce':
        Widget = TinyMCE
    else:
        Widget = Textarea

class EditorAdmin(Admin):
    """
    Universal Admin class for pluggable editor
    """
    if rich_text_module == 'tinymce':
        formfield_overrides = {models.TextField: {'widget': Widget}}


class EditorStackedInline(StackedInline):
    """
    Universal StackedInline class for pluggable editor
    """
    if rich_text_module == 'tinymce':
        formfield_overrides = {models.TextField: {'widget': Widget}}


class EditorWidget(Widget):
    """
    Universal TextField Widget class for pluggable editor
    """

    class Media:
        if rich_text_module == 'imperavi':
            js = ('%simperavi/jquery.js' % settings.STATIC_URL,
             '%simperavi/redactor/redactor.min.js' % settings.STATIC_URL)
            css = {'all': (
                     '%simperavi/redactor/css/redactor.css' % settings.STATIC_URL,)}