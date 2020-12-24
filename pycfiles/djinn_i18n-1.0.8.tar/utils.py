# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_i18n/djinn_i18n/utils.py
# Compiled at: 2014-10-06 05:47:45
import gettext, os
from django.conf import settings
from django.utils import translation
from django.utils.translation import trans_real, get_language

def get_translatable_apps():
    _apps = {}
    for path in settings.LOCALE_PATHS:
        if path == get_override_base():
            continue
        parts = path.split(os.path.sep)
        if parts[(-1)]:
            _app = parts[(-2)]
        else:
            _app = parts[(-3)]
        _apps[_app] = path

    return _apps


def get_override_base():
    return getattr(settings, 'PO_OVERRIDES', '%s/var/locale' % settings.PROJECT_ROOT)


def generate_po_path(base, locale):
    return '%s/%s/LC_MESSAGES/django.po' % (base, locale)


def clear_trans_cache():
    try:
        gettext._translations = {}
        trans_real._translations = {}
        trans_real._default = None
        translation.activate(get_language())
    except AttributeError:
        pass

    return