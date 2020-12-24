# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modify_history/__init__.py
# Compiled at: 2011-06-10 23:28:22
from django.conf import settings
settings.HISTORY_ENABLE = getattr(settings, 'HISTORY_ENABLE', True)
settings.HISTORY_USER_ATTRS = getattr(settings, 'HISTORY_USER_ATTRS', ['updated_by', 'user', 'author', 'created_by'])
from sites import site

def autodiscover():
    """
    Automatically build the site index.
    
    Again, almost exactly as django.contrib.admin does things, for consistency.
    """
    from django.conf import settings
    import imp
    for app in settings.INSTALLED_APPS:
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[(-1)]]).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('history_site', app_path)
        except ImportError:
            continue

        __import__('%s.history_site' % app)


autodiscover()