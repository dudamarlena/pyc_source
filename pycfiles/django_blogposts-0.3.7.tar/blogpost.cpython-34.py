# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/templatetags/blogpost.py
# Compiled at: 2018-08-06 17:49:30
# Size of source mod 2**32: 1766 bytes
from django import template
from django.conf import settings
from ..models.blogpost import BlogPost
from ..models.categories import Categories
from ..models.tags import Tags
__author__ = 'spi4ka'
register = template.Library()

@register.inclusion_tag('django_blogposts/list-item.html')
def blogpost_list_item(page, is_odd=False):
    return {'object': page, 
     'is_odd': is_odd}


@register.inclusion_tag('django_blogposts/categories/list.html')
def categories_list(active):
    if getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
        object_list = Categories.objects.filter(is_moderated=True)
    else:
        object_list = Categories.objects.none()
    return {'object_list': object_list,  'active': active}


@register.inclusion_tag('django_blogposts/tags/list.html')
def tags_list(tags=None, active=None):
    if tags:
        object_list = tags
    else:
        if getattr(settings, 'BLOGPOSTS_USE_TAGS', True):
            object_list = Tags.objects.filter(is_moderated=True)
        else:
            object_list = Tags.objects.none()
    return {'object_list': object_list,  'active': active}


@register.inclusion_tag('django_blogposts/last_posts/list.html')
def last_post(exclude=[]):
    if exclude:
        if isinstance(exclude, int):
            exclude = [
             exclude]
        object_list = BlogPost.active.filter(category__is_moderated=True, is_moderated=True).prefetch_related('category')
        if exclude:
            object_list = object_list.exclude(pk__in=exclude)
        return {'object_list': object_list[0:6]}


@register.simple_tag
def get_last_posts(count=6):
    return BlogPost.active.filter(category__is_moderated=True, is_moderated=True).prefetch_related('category')[0:count]