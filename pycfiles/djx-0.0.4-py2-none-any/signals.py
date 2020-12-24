# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/test/signals.py
# Compiled at: 2019-02-14 00:35:17
import os, threading, time, warnings
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.db import connections, router
from django.db.utils import ConnectionRouter
from django.dispatch import Signal, receiver
from django.utils import six, timezone
from django.utils.formats import FORMAT_SETTINGS, reset_format_cache
from django.utils.functional import empty
template_rendered = Signal(providing_args=['template', 'context'])
COMPLEX_OVERRIDE_SETTINGS = {
 'DATABASES'}

@receiver(setting_changed)
def clear_cache_handlers(**kwargs):
    if kwargs['setting'] == 'CACHES':
        from django.core.cache import caches
        caches._caches = threading.local()


@receiver(setting_changed)
def update_installed_apps(**kwargs):
    if kwargs['setting'] == 'INSTALLED_APPS':
        from django.contrib.staticfiles.finders import get_finder
        get_finder.cache_clear()
        from django.core.management import get_commands
        get_commands.cache_clear()
        from django.template.utils import get_app_template_dirs
        get_app_template_dirs.cache_clear()
        from django.utils.translation import trans_real
        trans_real._translations = {}


@receiver(setting_changed)
def update_connections_time_zone(**kwargs):
    if kwargs['setting'] == 'TIME_ZONE':
        if hasattr(time, 'tzset'):
            if kwargs['value']:
                os.environ['TZ'] = kwargs['value']
            else:
                os.environ.pop('TZ', None)
            time.tzset()
        timezone.get_default_timezone.cache_clear()
    if kwargs['setting'] in {'TIME_ZONE', 'USE_TZ'}:
        for conn in connections.all():
            try:
                del conn.timezone
            except AttributeError:
                pass

            try:
                del conn.timezone_name
            except AttributeError:
                pass

            conn.ensure_timezone()

    return


@receiver(setting_changed)
def clear_routers_cache(**kwargs):
    if kwargs['setting'] == 'DATABASE_ROUTERS':
        router.routers = ConnectionRouter().routers


@receiver(setting_changed)
def reset_template_engines(**kwargs):
    if kwargs['setting'] in {
     'TEMPLATES',
     'DEBUG',
     'FILE_CHARSET',
     'INSTALLED_APPS'}:
        from django.template import engines
        try:
            del engines.templates
        except AttributeError:
            pass

        engines._templates = None
        engines._engines = {}
        from django.template.engine import Engine
        Engine.get_default.cache_clear()
        from django.forms.renderers import get_default_renderer
        get_default_renderer.cache_clear()
    return


@receiver(setting_changed)
def clear_serializers_cache(**kwargs):
    if kwargs['setting'] == 'SERIALIZATION_MODULES':
        from django.core import serializers
        serializers._serializers = {}


@receiver(setting_changed)
def language_changed(**kwargs):
    if kwargs['setting'] in {'LANGUAGES', 'LANGUAGE_CODE', 'LOCALE_PATHS'}:
        from django.utils.translation import trans_real
        trans_real._default = None
        trans_real._active = threading.local()
    if kwargs['setting'] in {'LANGUAGES', 'LOCALE_PATHS'}:
        from django.utils.translation import trans_real
        trans_real._translations = {}
        trans_real.check_for_language.cache_clear()
    return


@receiver(setting_changed)
def localize_settings_changed(**kwargs):
    if kwargs['setting'] in FORMAT_SETTINGS or kwargs['setting'] == 'USE_THOUSAND_SEPARATOR':
        reset_format_cache()


@receiver(setting_changed)
def file_storage_changed(**kwargs):
    if kwargs['setting'] == 'DEFAULT_FILE_STORAGE':
        from django.core.files.storage import default_storage
        default_storage._wrapped = empty


@receiver(setting_changed)
def complex_setting_changed(**kwargs):
    if kwargs['enter'] and kwargs['setting'] in COMPLEX_OVERRIDE_SETTINGS:
        warnings.warn('Overriding setting %s can lead to unexpected behavior.' % kwargs['setting'], stacklevel=5 if six.PY2 else 6)


@receiver(setting_changed)
def root_urlconf_changed(**kwargs):
    if kwargs['setting'] == 'ROOT_URLCONF':
        from django.urls import clear_url_caches, set_urlconf
        clear_url_caches()
        set_urlconf(None)
    return


@receiver(setting_changed)
def static_storage_changed(**kwargs):
    if kwargs['setting'] in {
     'STATICFILES_STORAGE',
     'STATIC_ROOT',
     'STATIC_URL'}:
        from django.contrib.staticfiles.storage import staticfiles_storage
        staticfiles_storage._wrapped = empty


@receiver(setting_changed)
def static_finders_changed(**kwargs):
    if kwargs['setting'] in {
     'STATICFILES_DIRS',
     'STATIC_ROOT'}:
        from django.contrib.staticfiles.finders import get_finder
        get_finder.cache_clear()


@receiver(setting_changed)
def auth_password_validators_changed(**kwargs):
    if kwargs['setting'] == 'AUTH_PASSWORD_VALIDATORS':
        from django.contrib.auth.password_validation import get_default_password_validators
        get_default_password_validators.cache_clear()


@receiver(setting_changed)
def user_model_swapped(**kwargs):
    if kwargs['setting'] == 'AUTH_USER_MODEL':
        apps.clear_cache()
        try:
            from django.contrib.auth import get_user_model
            UserModel = get_user_model()
        except ImproperlyConfigured:
            pass
        else:
            from django.contrib.auth import backends
            backends.UserModel = UserModel
            from django.contrib.auth import forms
            forms.UserModel = UserModel
            from django.contrib.auth.handlers import modwsgi
            modwsgi.UserModel = UserModel
            from django.contrib.auth.management.commands import changepassword
            changepassword.UserModel = UserModel
            from django.contrib.auth import views
            views.UserModel = UserModel