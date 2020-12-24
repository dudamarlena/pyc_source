# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/show/templatetags/show_inclusion_tags.py
# Compiled at: 2010-08-24 03:41:12
from django import template
from show.models import Show
register = template.Library()

@register.inclusion_tag('show/inclusion_tags/radioshow_entryitem_listing.html', takes_context=True)
def radioshow_entryitem_listing(context, object_list):
    context.update({'object_list': object_list})
    return context


@register.inclusion_tag('show/inclusion_tags/showcontributor_header.html')
def showcontributor_header(obj):
    from cal.models import Entry
    shows = Show.objects.filter(contributor=obj)
    modelbase_objs = [ show.modelbase_obj for show in shows ]
    entries = Entry.objects.filter(content__in=modelbase_objs)
    return {'entries': entries, 
       'object': obj}


@register.inclusion_tag('show/inclusion_tags/showcontributor_detail.html')
def showcontributor_detail(obj):
    return {'object': obj}