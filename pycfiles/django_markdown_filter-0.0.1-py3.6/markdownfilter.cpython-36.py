# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/markdownfilter/templatetags/markdownfilter.py
# Compiled at: 2017-05-10 23:59:44
# Size of source mod 2**32: 371 bytes
from django import template
from django.conf import settings
import markdown2, bleach
register = template.Library()

@register.filter
def markdownfilter(text):
    untrusted_text = markdown2.markdown(text)
    html = bleach.clean(untrusted_text, tags=(settings.MARKDOWNIFY_WHITELIST_TAGS))
    html = bleach.linkify(html)
    return html