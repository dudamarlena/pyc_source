# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rstuart/.pyenv/versions/gcloudoem/lib/python2.7/site-packages/gcloudoem/django/shortcuts.py
# Compiled at: 2015-04-20 22:18:08
from __future__ import absolute_import, division, print_function, unicode_literals
from ..exceptions import ValidationError
from ..queryset import QuerySet

def _get_queryset(cls):
    """Inspired by django.shortcuts.*"""
    if isinstance(cls, QuerySet):
        return cls
    else:
        return cls.objects


def get_entity_or_404(cls, *args, **kwargs):
    """
    Uses get() to return an document, or raises a Http404 exception if the document does not exist.

    cls may be a Document or QuerySet object. All other passed arguments and keyword arguments are used in the get()
    query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one object is found.

    Inspired by django.shortcuts.*
    """
    queryset = _get_queryset(cls)
    try:
        return queryset.get(*args, **kwargs)
    except (queryset.entity.DoesNotExist, ValidationError):
        from django.http import Http404
        raise Http404(b'No %s matches the given query.' % queryset.entity._meta.kind)


def get_list_or_404(cls, *args, **kwargs):
    """
    Uses filter() to return a list of documents, or raise a Http404 exception if the list is empty.

    cls may be a Document or QuerySet object. All other passed arguments and keyword arguments are used in the filter()
    query.

    Inspired by django.shortcuts.*
    """
    queryset = _get_queryset(cls)
    obj_list = list(queryset.filter(*args, **kwargs))
    if not obj_list:
        from django.http import Http404
        raise Http404(b'No %s matches the given query.' % queryset.entity._meta.kind)
    return obj_list