# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/libs/tinymce/templatetags/tinymce_tags.py
# Compiled at: 2020-02-11 12:52:19
# Size of source mod 2**32: 504 bytes
from django import template
from django.template.loader import render_to_string
import tendenci.libs.tinymce.settings as tinymce_settings
register = template.Library()

def tinymce_preview(element_id):
    return render_to_string(template_name='tinymce/preview_javascript.html', context={'base_url':tinymce_settings.JS_BASE_URL, 
     'element_id':element_id})


register.simple_tag(tinymce_preview)