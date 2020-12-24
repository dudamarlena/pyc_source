# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/wiki/templatetags/wiki.py
# Compiled at: 2009-01-08 09:11:51
from django import template
from django.utils.safestring import mark_safe
from softwarefabrica.django.wiki.models import *
from softwarefabrica.django.wiki.wikiparse import wikiparse
register = template.Library()

def wiki(value, page=None, makesafe=True):
    assert isinstance(value, PageContent)
    (text, linked_pages) = wikiparse(value, makesafe)
    return text


wiki.is_safe = True
register.filter('wiki', wiki)