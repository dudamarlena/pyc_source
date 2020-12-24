# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/conf/urls.py
# Compiled at: 2016-02-09 18:08:02
# Size of source mod 2**32: 601 bytes
from django.conf.urls import patterns, include, url
from ginger.views import utils
__all__ = ('pattern', 'include', 'url', 'scan', 'scan_to_include')

def scan(module, predicate=None):
    view_classes = utils.find_views(module, predicate=predicate)
    urls = []
    for view in view_classes:
        if hasattr(view, 'as_urls'):
            urls.extend(view.as_urls())
        else:
            urls.append(view.as_url())

    pattern = urls
    return pattern


def scan_to_include(module, predicate=None, app_name=None, namespace=None):
    return (scan(module, predicate), app_name, namespace)