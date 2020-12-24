# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twod/wsgi/factories.py
# Compiled at: 2011-06-28 10:17:42
"""
Miscellaneous PasteDeploy Application Factories.

"""
from os import path
from paste.urlmap import URLMap
from paste.urlparser import StaticURLParser
from django import __file__ as django_init
__all__ = ('make_full_django_app', 'add_media_to_app')
_DJANGO_ROOT = path.dirname(django_init)

def make_full_django_app(loader, global_conf, **local_conf):
    """
    Return a WSGI application made up of the Django application, its media and
    the Django Admin media.
    
    This is a PasteDeploy Composite Application Factory.
    
    """
    django_app = loader.get_app(local_conf['django_app'], global_conf=global_conf)
    return add_media_to_app(django_app)


def add_media_to_app(django_app):
    """
    Return a WSGI application made up of the Django application, its media and
    the Django Admin media.
    
    """
    app = URLMap()
    app['/'] = django_app
    from django.conf import settings
    admin_media = path.join(_DJANGO_ROOT, 'contrib', 'admin', 'media')
    app[settings.ADMIN_MEDIA_PREFIX] = StaticURLParser(admin_media)
    app[settings.MEDIA_URL] = StaticURLParser(settings.MEDIA_ROOT)
    return app