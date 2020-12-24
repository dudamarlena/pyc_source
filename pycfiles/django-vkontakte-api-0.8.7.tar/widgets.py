# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-api/vkontakte_api/widgets.py
# Compiled at: 2015-01-25 02:59:11
from django import forms
from django.utils.safestring import mark_safe

class AdminImageWidget(forms.FileInput):
    """
    A ImageField Widget for admin that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, 'url'):
            output.append('<a target="_blank" href="%s"><img src="%s" style="height: 28px;" /></a> ' % (
             value.url, value.url))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(('').join(output))