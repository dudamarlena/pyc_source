# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/wiki/templatetags/recentpages.py
# Compiled at: 2009-01-08 09:11:51
from django import template
import datetime
from softwarefabrica.django.wiki.models import *
register = template.Library()

@register.inclusion_tag('wiki/tags/last_modified_pages.html')
def last_modified_pages(wiki=None, num=10):
    wikiname = None
    if type(wiki) == type(Wiki):
        wikiname = wiki.name
    elif type(wiki) == type('') or type(wiki) == type(''):
        wikiname = wiki
        wiki = Wiki.objects.get(name=wikiname)
    if wiki:
        pages = Page.objects.filter(wiki=wiki).order_by('-modified')[:num]
    else:
        pages = Page.objects.order_by('-modified', 'wiki')[:num]
    return {'wiki': wiki, 'pages': pages}