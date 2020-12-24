# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/theme_editor/templatetags/theme_editor_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 484 bytes
from django.template import Library
register = Library()

@register.inclusion_tag('theme_editor/folder_structure.html', takes_context=True)
def folder_structure(context, value):
    context.update({'value': value})
    return context


@register.inclusion_tag('theme_editor/details.html', takes_context=True)
def theme_detail(context, theme, current_theme):
    context.update({'theme':theme, 
     'current_theme':current_theme})
    return context