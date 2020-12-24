# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-link/link/utils.py
# Compiled at: 2018-05-10 08:28:02
# Size of source mod 2**32: 1228 bytes
from importlib import import_module
from django.conf import settings
try:
    from django.urls import URLResolver as RegexURLResolver
    from django.urls import URLPattern as RegexURLPattern
except ImportError:
    from django.core.urlresolvers import RegexURLResolver, RegexURLPattern

from link import SETTINGS

def get_view_names(urlpatterns=None, view_names=[], namespace=None):
    if urlpatterns is None:
        urlpatterns = import_module(settings.ROOT_URLCONF).urlpatterns
    if namespace not in SETTINGS.get('excluded-viewname-choices'):
        for pattern in urlpatterns:
            if isinstance(pattern, RegexURLResolver):
                get_view_names(pattern.url_patterns, view_names, pattern.namespace)
            elif isinstance(pattern, RegexURLPattern):
                view_name = pattern.name
                if view_name:
                    if namespace:
                        view_name = '%s:%s' % (namespace, view_name)
                    if view_name not in view_names:
                        view_names.append(view_name)

    return view_names


def get_view_name_choices():
    return [tuple([view_name, view_name]) for view_name in get_view_names()]