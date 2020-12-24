# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/utils/conf.py
# Compiled at: 2016-05-25 12:12:39
from __future__ import unicode_literals
import os, sys
from warnings import warn
from django import VERSION
from django.conf import global_settings as defaults
from django.template.base import add_to_builtins
from wenlincms.utils.timezone import get_best_local_timezone

class SitesAllowedHosts(object):
    """
    This is a fallback for Django 1.5's ALLOWED_HOSTS setting
    which is required when DEBUG is False. It looks up the
    ``Site`` model and uses any domains added to it, the
    first time the setting is accessed.
    """

    def __iter__(self):
        if getattr(self, b'_hosts', None) is None:
            from django.contrib.sites.models import Site
            self._hosts = [ s.domain.split(b':')[0] for s in Site.objects.all() ]
        return iter(self._hosts)


def set_dynamic_settings(s):
    """
    Called at the end of the project's settings module, and is passed
    its globals dict for updating with some final tweaks for settings
    that generally aren't specified, but can be given some better
    defaults based on other settings that have been specified. Broken
    out into its own function so that the code need not be replicated
    in the settings modules of other project-based apps that leverage
    wenlincms's settings module.
    """
    move = lambda n, k, i: s[n].insert(i, s[n].pop(s[n].index(k)))
    append = lambda n, k: s[n].append(k) if k not in s[n] else None
    prepend = lambda n, k: s[n].insert(0, k) if k not in s[n] else None
    remove = lambda n, k: s[n].remove(k) if k in s[n] else None
    s[b'TEMPLATE_DEBUG'] = s.get(b'TEMPLATE_DEBUG', s.get(b'DEBUG', False))
    add_to_builtins(b'wenlincms.template.loader_tags')
    if not s.get(b'ALLOWED_HOSTS', []):
        warn(b"You haven't defined the ALLOWED_HOSTS settings, which Django 1.5 requires. Will fall back to the domains configured as sites.")
        s[b'ALLOWED_HOSTS'] = SitesAllowedHosts()
    if s.get(b'TIME_ZONE', None) is None:
        tz = get_best_local_timezone()
        s[b'TIME_ZONE'] = tz
        warn(b'TIME_ZONE setting is not set, using closest match: %s' % tz)
    management_command = sys.argv[1] if len(sys.argv) > 1 else b''
    s[b'TESTING'] = management_command in ('test', 'testserver')
    s[b'DEV_SERVER'] = management_command.startswith(('runserver', 'harvest'))
    s.setdefault(b'AUTHENTICATION_BACKENDS', defaults.AUTHENTICATION_BACKENDS)
    s.setdefault(b'STATICFILES_FINDERS', defaults.STATICFILES_FINDERS)
    tuple_list_settings = [b'AUTHENTICATION_BACKENDS', b'INSTALLED_APPS',
     b'MIDDLEWARE_CLASSES', b'STATICFILES_FINDERS',
     b'LANGUAGES', b'TEMPLATE_CONTEXT_PROCESSORS']
    for setting in tuple_list_settings[:]:
        if not isinstance(s.get(setting, []), list):
            s[setting] = list(s[setting])
        else:
            tuple_list_settings.remove(setting)

    storage = b'django.contrib.messages.storage.cookie.CookieStorage'
    s.setdefault(b'MESSAGE_STORAGE', storage)
    if s[b'TESTING']:
        append(b'AUTHENTICATION_BACKENDS', b'django.contrib.auth.backends.ModelBackend')
        remove(b'INSTALLED_APPS', b'django.contrib.redirects')
        remove(b'MIDDLEWARE_CLASSES', b'django.contrib.redirects.middleware.RedirectFallbackMiddleware')
    else:
        optional = list(s.get(b'OPTIONAL_APPS', []))
        s[b'USE_SOUTH'] = s.get(b'USE_SOUTH') and VERSION < (1, 7)
        if s.get(b'USE_SOUTH'):
            optional.append(b'south')
        else:
            if not s.get(b'USE_SOUTH', True) and b'south' in s[b'INSTALLED_APPS']:
                s[b'INSTALLED_APPS'].remove(b'south')
            for app in optional:
                if app not in s[b'INSTALLED_APPS']:
                    try:
                        __import__(app)
                    except ImportError:
                        pass
                    else:
                        s[b'INSTALLED_APPS'].append(app)

            if b'debug_toolbar' in s[b'INSTALLED_APPS']:
                debug_mw = b'debug_toolbar.middleware.DebugToolbarMiddleware'
                append(b'MIDDLEWARE_CLASSES', debug_mw)
            if b'compressor' in s[b'INSTALLED_APPS']:
                append(b'STATICFILES_FINDERS', b'compressor.finders.CompressorFinder')
                s.setdefault(b'COMPRESS_OFFLINE_CONTEXT', {b'MEDIA_URL': s.get(b'MEDIA_URL', b''), 
                   b'STATIC_URL': s.get(b'STATIC_URL', b'')})

                def wenlincms_settings():
                    from wenlincms.conf import settings
                    return settings

                s[b'COMPRESS_OFFLINE_CONTEXT'][b'settings'] = wenlincms_settings
            if b'wlapps.accounts' in s[b'INSTALLED_APPS']:
                auth_backend = b'wenlincms.core.auth_backends.wenlincmsBackend'
                s.setdefault(b'AUTHENTICATION_BACKENDS', [])
                prepend(b'AUTHENTICATION_BACKENDS', auth_backend)
            wladmin_name = s.get(b'PACKAGE_NAME_ADMIN')
            if s[b'TESTING']:
                try:
                    __import__(wladmin_name)
                except ImportError:
                    pass
                else:
                    append(b'INSTALLED_APPS', wladmin_name)

            try:
                move(b'INSTALLED_APPS', wladmin_name, len(s[b'INSTALLED_APPS']))
            except ValueError:
                s[b'WLADMIN_INSTALLED'] = False
            else:
                s[b'WLADMIN_INSTALLED'] = True

            apps = [
             b'django.contrib.admin']
            if VERSION >= (1, 7):
                apps += [b'django.contrib.staticfiles']
            for app in apps:
                try:
                    move(b'INSTALLED_APPS', app, len(s[b'INSTALLED_APPS']))
                except ValueError:
                    pass

            s.setdefault(b'TEST_RUNNER', b'django.test.simple.DjangoTestSuiteRunner')
            if b'wenlincms.generic' in s[b'INSTALLED_APPS']:
                s.setdefault(b'COMMENTS_APP', b'wenlincms.generic')
                append(b'INSTALLED_APPS', b'django.contrib.comments')
            try:
                move(b'INSTALLED_APPS', b'wenlincms.boot', 0)
            except ValueError:
                pass

            if not (s.get(b'CACHE_BACKEND') or s.get(b'CACHES')):
                s[b'MIDDLEWARE_CLASSES'] = [ mw for mw in s[b'MIDDLEWARE_CLASSES'] if not (mw.endswith(b'UpdateCacheMiddleware') or mw.endswith(b'FetchFromCacheMiddleware'))
                                           ]
            if s.get(b'LANGUAGE_CODE') and len(s.get(b'LANGUAGES', [])) == 1 and s[b'LANGUAGE_CODE'] != s[b'LANGUAGES'][0][0]:
                s[b'USE_I18N'] = True
                s[b'LANGUAGES'] = [(s[b'LANGUAGE_CODE'], b'')]
            for setting in tuple_list_settings:
                s[setting] = tuple(s[setting])

        for key, db in s[b'DATABASES'].items():
            shortname = db[b'ENGINE'].split(b'.')[(-1)]
            if shortname == b'sqlite3' and os.sep not in db[b'NAME']:
                db_path = os.path.join(s.get(b'PROJECT_ROOT', b''), db[b'NAME'])
                s[b'DATABASES'][key][b'NAME'] = db_path
            elif shortname == b'mysql':
                s[b'DATABASES'][key][b'TEST_COLLATION'] = b'utf8_general_ci'

    return