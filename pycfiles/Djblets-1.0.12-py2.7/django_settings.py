# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/siteconfig/django_settings.py
# Compiled at: 2019-06-12 01:17:17
"""Utilities for going between SiteConfiguration and Django settings."""
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.cache import DEFAULT_CACHE_ALIAS
from django.utils import six, timezone
from djblets.cache.backend_compat import normalize_cache_backend
from djblets.cache.forwarding_backend import DEFAULT_FORWARD_CACHE_ALIAS, ForwardingCacheBackend

def _set_cache_backend(settings, key, value):
    """Set the default cache backend.

    This will set the default cache backend to use Djblets's
    :py:class:`~djblets.cache.forwarding_backend.ForwardingCacheBackend`,
    and use that to forward on to the provided cache backend.

    The new cache settings will be instantly usable by the application
    without having to restart.

    Args:
        settings (django.conf.LazySettings):
            The Django settings object.

        key (unicode, unused):
            The settings key (``CACHES``).

        value (object):
            The cache backend settings. This may be a legacy URI or a
            dictionary containing cache backend information.
    """
    settings.CACHES.update({DEFAULT_FORWARD_CACHE_ALIAS: normalize_cache_backend(value, DEFAULT_FORWARD_CACHE_ALIAS) or normalize_cache_backend(value), 
       DEFAULT_CACHE_ALIAS: {b'BACKEND': b'%s.%s' % (ForwardingCacheBackend.__module__,
                                        ForwardingCacheBackend.__name__), 
                             b'LOCATION': DEFAULT_FORWARD_CACHE_ALIAS}})
    from django.core.cache import cache
    if isinstance(cache, ForwardingCacheBackend):
        cache.reset_backend()


def _set_static_url(settings, key, value):
    """Set the URL for static media.

    Args:
        settings (django.conf.LazySettings):
            The Django settings object.

        key (unicode, unused):
            The settings key (``STATIC_URL``).

        value (object):
            The new static URL.
    """
    settings.STATIC_URL = value
    staticfiles_storage.base_url = value


def _set_timezone(settings, key, value):
    """Set the server's timezone.

    Args:
        settings (django.conf.LazySettings):
            The Django settings object.

        key (unicode, unused):
            The settings key (``TIME_ZONE``).

        value (object):
            The new timezone.
    """
    settings.TIME_ZONE = value
    timezone.activate(settings.TIME_ZONE)


locale_settings_map = {b'locale_timezone': {b'key': b'TIME_ZONE', b'deserialize_func': six.text_type, 
                        b'setter': _set_timezone}, 
   b'locale_language_code': b'LANGUAGE_CODE', 
   b'locale_date_format': b'DATE_FORMAT', 
   b'locale_datetime_format': b'DATETIME_FORMAT', 
   b'locale_default_charset': {b'key': b'DEFAULT_CHARSET', b'deserialize_func': six.text_type}, 
   b'locale_language_code': b'LANGUAGE_CODE', 
   b'locale_month_day_format': b'MONTH_DAY_FORMAT', 
   b'locale_time_format': b'TIME_FORMAT', 
   b'locale_year_month_format': b'YEAR_MONTH_FORMAT'}
mail_settings_map = {b'mail_server_address': b'SERVER_EMAIL', 
   b'mail_default_from': b'DEFAULT_FROM_EMAIL', 
   b'mail_host': b'EMAIL_HOST', 
   b'mail_port': b'EMAIL_PORT', 
   b'mail_host_user': {b'key': b'EMAIL_HOST_USER', b'deserialize_func': bytes}, 
   b'mail_host_password': {b'key': b'EMAIL_HOST_PASSWORD', b'deserialize_func': bytes}, 
   b'mail_use_tls': b'EMAIL_USE_TLS'}
site_settings_map = {b'site_media_root': b'MEDIA_ROOT', 
   b'site_media_url': b'MEDIA_URL', 
   b'site_static_root': b'STATIC_ROOT', 
   b'site_static_url': {b'key': b'STATIC_URL', b'setter': _set_static_url}, 
   b'site_prepend_www': b'PREPEND_WWW', 
   b'site_upload_temp_dir': b'FILE_UPLOAD_TEMP_DIR', 
   b'site_upload_max_memory_size': b'FILE_UPLOAD_MAX_MEMORY_SIZE'}
cache_settings_map = {b'cache_backend': {b'key': b'CACHES', b'setter': _set_cache_backend}, 
   b'cache_expiration_time': b'CACHE_EXPIRATION_TIME'}
_django_settings_map = {}

def get_django_settings_map():
    """Return a map of customizable Django settings.

    These maps are passed to other functions, like :py:func:`generate_defaults`
    and :py:func:`apply_django_settings`. Consumers can make their own
    settings map based on this with additional settings they want to provide.

    Each entry maps a siteconfig settings key to either a Django settings key
    or detailed information on serializing/deserializing a Django setting.

    An entry with detailed information represents that as a dictionary
    containing the following fields:

    ``key`` (:py:class:`unicode`):
        The Django settings key.

    ``deserialize_func`` (callable, optional):
        A function taking the value from the siteconfig and returning a value
        usable in Django settings.

    ``setter`` (callable, optional):
        A function taking the Django settings object, the Django settings key,
        and the new value from the siteconfig (after going through
        ``deserialize_func``, if provided). This will set the value in Django's
        settings object.

    Returns:
        dict:
        The resulting settings map. This is generated once and cached for
        future calls.
    """
    if not _django_settings_map:
        _django_settings_map.update(locale_settings_map)
        _django_settings_map.update(mail_settings_map)
        _django_settings_map.update(site_settings_map)
        _django_settings_map.update(cache_settings_map)
    return _django_settings_map


def generate_defaults(settings_map):
    """Return a dictionary of siteconfig defaults for Django settings.

    This will iterate through the provided settings map and return a dictionary
    mapping a siteconfig settings key to the value from Django's settings (if
    one is found).

    Args:
        settings_map (dict):
            A settings map, generated from :py:func:`get_django_settings_map`
            or a similar function.

    Returns:
        dict:
        A dictionary of siteconfig defaults.
    """
    defaults = {}
    for siteconfig_key, setting_data in six.iteritems(settings_map):
        if isinstance(setting_data, dict):
            setting_key = setting_data[b'key']
        else:
            setting_key = setting_data
        if hasattr(settings, setting_key):
            defaults[siteconfig_key] = getattr(settings, setting_key)

    return defaults


def get_locale_defaults():
    """Return a dictionary of siteconfig defaults for Django locale settings.

    The generated defaults are specific to the values in
    :py:data:`locale_settings_map`.

    Returns:
        dict:
        A dictionary of siteconfig defaults.
    """
    return generate_defaults(locale_settings_map)


def get_mail_defaults():
    """Return a dictionary of siteconfig defaults for Django e-mail settings.

    The generated defaults are specific to the values in
    :py:data:`mail_settings_map`.

    Returns:
        dict:
        A dictionary of siteconfig defaults.
    """
    return generate_defaults(mail_settings_map)


def get_site_defaults():
    """Return a dictionary of siteconfig defaults for Django site settings.

    The generated defaults are specific to the values in
    :py:data:`site_settings_map`.

    Returns:
        dict:
        A dictionary of siteconfig defaults.
    """
    return generate_defaults(site_settings_map)


def get_cache_defaults():
    """Return a dictionary of siteconfig defaults for Django caching settings.

    The generated defaults are specific to the values in
    :py:data:`cache_settings_map`.

    Returns:
        dict:
        A dictionary of siteconfig defaults.
    """
    return generate_defaults(cache_settings_map)


def get_django_defaults():
    """Return a dictionary of siteconfig defaults for Django settings.

    The generated defaults are specific to the values returned by
    :py:func:`get_django_settings_map`.

    Returns:
        dict:
        A dictionary of siteconfig defaults.
    """
    return generate_defaults(get_django_settings_map())


def apply_django_settings(siteconfig, settings_map=None):
    """Apply Django settings stored in the site configuration.

    This takes a siteconfiguration storing Django settings and a settings map,
    applying each of the settings to Django. Setting will generally be stored
    in the Django settings object, but some settings will be specially applied
    based on their rules in the settings map.

    Args:
        siteconfig (djblets.siteconfig.models.SiteConfiguration):
            The site configuration containing the Django settings to apply.

        settings_map (dict, optional):
            A map of siteconfig keys to Django settings information. See
            :py:func:`get_django_settings_map` for details.

            If not provided, the result of :py:func:`get_django_settings_map`
            will be used.
    """
    if settings_map is None:
        settings_map = get_django_settings_map()
    for key, setting_data in six.iteritems(settings_map):
        if key in siteconfig.settings:
            value = siteconfig.get(key)
            setter = setattr
            if isinstance(setting_data, dict):
                setting_key = setting_data[b'key']
                if b'setter' in setting_data:
                    setter = setting_data[b'setter']
                if b'deserialize_func' in setting_data and six.callable(setting_data[b'deserialize_func']):
                    value = setting_data[b'deserialize_func'](value)
            else:
                setting_key = setting_data
            setter(settings, setting_key, value)

    return