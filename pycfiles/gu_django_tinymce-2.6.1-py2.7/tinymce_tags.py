# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Bucket/projects/tinymce/gu-django-tinymce/tinymce/templatetags/tinymce_tags.py
# Compiled at: 2016-04-21 01:35:11
from django import template
from django.template.loader import render_to_string
import tinymce.settings
register = template.Library()

def tinymce_preview(element_id):
    return render_to_string('tinymce/preview_javascript.html', {'base_url': tinymce.settings.JS_BASE_URL, 'element_id': element_id})


register.simple_tag(tinymce_preview)