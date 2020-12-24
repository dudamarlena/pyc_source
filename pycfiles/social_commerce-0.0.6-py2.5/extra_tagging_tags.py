# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/tag_app/templatetags/extra_tagging_tags.py
# Compiled at: 2009-10-31 23:19:40
from django.template import Library
from django.conf import settings
register = Library()

@register.inclusion_tag('tag_app/tag_list.html')
def show_tags_for(obj):
    return {'obj': obj, 
       'MEDIA_URL': settings.MEDIA_URL}


@register.inclusion_tag('tag_app/tag_count_list.html')
def show_tag_counts(tag_counts):
    return {'tag_counts': tag_counts}