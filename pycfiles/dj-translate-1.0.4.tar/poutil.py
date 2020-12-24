# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dadasu/demo/django/dj-translate/autotranslate/poutil.py
# Compiled at: 2016-10-05 04:49:08
from datetime import datetime
from django.conf import settings
from autotranslate.conf import settings as autotranslate_settings
import django, os, inspect
from django.apps import AppConfig, apps
from django.utils import timezone
from django.core.cache import caches
cache = caches[autotranslate_settings.AUTOTRANSLATE_CACHE_NAME]

def timestamp_with_timezone(dt=None):
    """
    Return a timestamp with a timezone for the configured locale.  If all else
    fails, consider localtime to be UTC.
    """
    dt = dt or datetime.now()
    if timezone is None:
        return dt.strftime('%Y-%m-%d %H:%M%z')
    else:
        if not dt.tzinfo:
            tz = timezone.get_current_timezone()
            if not tz:
                tz = timezone.utc
            dt = dt.replace(tzinfo=timezone.get_current_timezone())
        return dt.strftime('%Y-%m-%d %H:%M%z')


def find_pos(lang, project_apps=True, django_apps=False, third_party_apps=False):
    """
    scans a couple possible repositories of gettext catalogs for the given
    language code

    """
    paths = []
    parts = settings.SETTINGS_MODULE.split('.')
    project = __import__(parts[0], {}, {}, [])
    abs_project_path = os.path.normpath(os.path.abspath(os.path.dirname(project.__file__)))
    if project_apps:
        if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(project.__file__), 'locale'))):
            paths.append(os.path.abspath(os.path.join(os.path.dirname(project.__file__), 'locale')))
        if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(project.__file__), '..', 'locale'))):
            paths.append(os.path.abspath(os.path.join(os.path.dirname(project.__file__), '..', 'locale')))
    if django_apps:
        django_paths = cache.get('autotranslate_django_paths')
        if django_paths is None:
            django_paths = []
            for root, dirnames, filename in os.walk(os.path.abspath(os.path.dirname(django.__file__))):
                if 'locale' in dirnames:
                    django_paths.append(os.path.join(root, 'locale'))
                    continue

            cache.set('autotranslate_django_paths', django_paths, 3600)
        paths = paths + django_paths
    for localepath in settings.LOCALE_PATHS:
        if os.path.isdir(localepath):
            paths.append(localepath)

    has_appconfig = False
    for appname in settings.INSTALLED_APPS:
        if autotranslate_settings.EXCLUDED_APPLICATIONS and appname in autotranslate_settings.EXCLUDED_APPLICATIONS:
            continue
        p = appname.rfind('.')
        if p >= 0:
            app = getattr(__import__(appname[:p], {}, {}, [str(appname[p + 1:])]), appname[p + 1:])
        else:
            app = __import__(appname, {}, {}, [])
        if django.VERSION[0:2] >= (1, 7):
            if inspect.isclass(app) and issubclass(app, AppConfig):
                has_appconfig = True
                continue
        app_path = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(app.__file__), 'locale')))
        if 'contrib' in app_path and 'django' in app_path and not django_apps:
            continue
        if not third_party_apps and abs_project_path not in app_path:
            continue
        if not project_apps and abs_project_path in app_path:
            continue
        if os.path.isdir(app_path):
            paths.append(app_path)

    if has_appconfig:
        for app_ in apps.get_app_configs():
            if autotranslate_settings.EXCLUDED_APPLICATIONS and app_.name in autotranslate_settings.EXCLUDED_APPLICATIONS:
                continue
            app_path = app_.path
            if 'contrib' in app_path and 'django' in app_path and not django_apps:
                continue
            if not third_party_apps and abs_project_path not in app_path:
                continue
            if not project_apps and abs_project_path in app_path:
                continue
            if os.path.exists(os.path.abspath(os.path.join(app_path, 'locale'))):
                paths.append(os.path.abspath(os.path.join(app_path, 'locale')))
            if os.path.exists(os.path.abspath(os.path.join(app_path, '..', 'locale'))):
                paths.append(os.path.abspath(os.path.join(app_path, '..', 'locale')))

    ret = set()
    langs = [lang]
    if '-' in lang:
        _l, _c = map(lambda x: x.lower(), lang.split('-', 1))
        langs += ['%s_%s' % (_l, _c), '%s_%s' % (_l, _c.upper()), '%s_%s' % (_l, _c.capitalize())]
    else:
        if '_' in lang:
            _l, _c = map(lambda x: x.lower(), lang.split('_', 1))
            langs += ['%s-%s' % (_l, _c), '%s-%s' % (_l, _c.upper()), '%s_%s' % (_l, _c.capitalize())]
        paths = map(os.path.normpath, paths)
        paths = list(set(paths))
        for path in paths:
            if path not in autotranslate_settings.AUTOTRANSLATE_EXCLUDED_PATHS:
                for lang_ in langs:
                    dirname = os.path.join(path, lang_, 'LC_MESSAGES')
                    for fn in autotranslate_settings.POFILENAMES:
                        filename = os.path.join(dirname, fn)
                        if os.path.isfile(filename):
                            ret.add(os.path.abspath(filename))

    return list(sorted(ret))


def pagination_range(first, last, current):
    r = []
    r.append(first)
    if first + 1 < last:
        r.append(first + 1)
    if current - 2 > first and current - 2 < last:
        r.append(current - 2)
    if current - 1 > first and current - 1 < last:
        r.append(current - 1)
    if current > first and current < last:
        r.append(current)
    if current + 1 < last and current + 1 > first:
        r.append(current + 1)
    if current + 2 < last and current + 2 > first:
        r.append(current + 2)
    if last - 1 > first:
        r.append(last - 1)
    r.append(last)
    r = list(set(r))
    r.sort()
    prev = 10000
    for e in r[:]:
        if prev + 1 < e:
            try:
                r.insert(r.index(e), '...')
            except ValueError:
                pass

        prev = e

    return r