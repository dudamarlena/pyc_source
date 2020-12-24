# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\pedro\OneDrive\dev\github\django-inlineedit\inlineedit\templatetags\inlineedit_default_script.py
# Compiled at: 2020-02-18 17:48:11
# Size of source mod 2**32: 422 bytes
from django.template.library import Library
import django.urls as reverse_url
from inlineedit.apps import InlineeditConfig
register = Library()

@register.inclusion_tag('inlineedit/default_bevahiour.html', takes_context=False)
def inlineedit_default_script():
    return {'inlineedit_endpoint': reverse_url(':'.join([InlineeditConfig.name, 'inlineedit']))}