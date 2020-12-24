# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/template/builtins/global_context.py
# Compiled at: 2015-05-19 08:55:16
from django.core.urlresolvers import reverse as django_reverse, NoReverseMatch
from django.contrib.staticfiles.storage import staticfiles_storage
__all__ = [
 'url', 'static']

def url(view_name, *args, **kwargs):
    """
    Shortcut filter for reverse url on templates. Is a alternative to
    django {% url %} tag, but more simple.

    Usage example:
        {{ url('web:timeline', userid=2) }}

    This is a equivalent to django:
        {% url 'web:timeline' userid=2 %}

    """
    return django_reverse(view_name, args=args, kwargs=kwargs)


def static(path):
    return staticfiles_storage.url(path)