# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/queries/__init__.py
# Compiled at: 2010-05-09 08:03:48
from queries.helpers import ACTION_CHECKBOX_NAME
from queries.options import ModelQuery, InlineModelQuery, HORIZONTAL, VERTICAL
from queries.sites import QuerySite, site
from django.utils.importlib import import_module
LOADING = False

def autodiscover():
    """
    Auto-discover INSTALLED_APPS query.py modules and fail silently when
    not present. This forces an import on them to register any query bits they
    may want.
    """
    global LOADING
    if LOADING:
        return
    LOADING = True
    import imp
    from django.conf import settings
    for app in settings.INSTALLED_APPS:
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('query', app_path)
        except ImportError:
            continue

        import_module('%s.query' % app)

    LOADING = False