# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jpapouse/workspace/adaptive-learning/proso-apps/proso_common/templatetags/common_js.py
# Compiled at: 2020-03-19 09:15:44
# Size of source mod 2**32: 446 bytes
from django import template
import django.templatetags.static as static
from django.conf import settings
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def js_files():
    js_files = []
    if hasattr(settings, 'PROSO_JS_FILES'):
        for f in settings.PROSO_JS_FILES:
            js_files.append('<script src="{}"></script>'.format(static(f)))

    return mark_safe('\n'.join(js_files))