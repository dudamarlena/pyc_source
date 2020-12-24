# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/70/_7dmwj6x12q099dhb0z0p7p80000gn/T/pycharm-packaging/djangorestframework/rest_framework/utils/breadcrumbs.py
# Compiled at: 2018-05-14 04:48:23
# Size of source mod 2**32: 2141 bytes
from __future__ import unicode_literals
from django.urls import get_script_prefix, resolve

def get_breadcrumbs(url, request=None):
    """
    Given a url returns a list of breadcrumbs, which are each a
    tuple of (name, url).
    """
    from rest_framework.reverse import preserve_builtin_query_params
    from rest_framework.views import APIView

    def breadcrumbs_recursive(url, breadcrumbs_list, prefix, seen):
        try:
            view, unused_args, unused_kwargs = resolve(url)
        except Exception:
            pass
        else:
            cls = getattr(view, 'cls', None)
            initkwargs = getattr(view, 'initkwargs', {})
            if cls is not None:
                if issubclass(cls, APIView):
                    if not seen or seen[(-1)] != view:
                        c = cls(**initkwargs)
                        c.suffix = getattr(view, 'suffix', None)
                        name = c.get_view_name()
                        insert_url = preserve_builtin_query_params(prefix + url, request)
                        breadcrumbs_list.insert(0, (name, insert_url))
                        seen.append(view)
            if url == '':
                return breadcrumbs_list
            else:
                if url.endswith('/'):
                    url = url.rstrip('/')
                    return breadcrumbs_recursive(url, breadcrumbs_list, prefix, seen)
                url = url[:url.rfind('/') + 1]
                return breadcrumbs_recursive(url, breadcrumbs_list, prefix, seen)

    prefix = get_script_prefix().rstrip('/')
    url = url[len(prefix):]
    return breadcrumbs_recursive(url, [], prefix, [])