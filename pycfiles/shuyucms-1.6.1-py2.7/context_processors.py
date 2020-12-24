# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/conf/context_processors.py
# Compiled at: 2016-05-20 23:26:47
from __future__ import unicode_literals
from shuyucms.utils.cache import cache_key_prefix, cache_installed, cache_get, cache_set
DEPRECATED = {b'PAGES_MENU_SHOW_ALL': True}

class TemplateSettings(dict):
    """
    Dict wrapper for template settings. This exists only to warn when
    deprecated settings are accessed in templates.
    """

    def __getitem__(self, k):
        if k in DEPRECATED:
            from warnings import warn
            warn(b'%s is deprecated, please remove it from your templates' % k)
        return super(TemplateSettings, self).__getitem__(k)

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError


def settings(request=None):
    """
    Add the settings object to the template context.
    """
    from shuyucms.conf import settings
    settings_dict = None
    cache_settings = request and cache_installed()
    if cache_settings:
        cache_key = cache_key_prefix(request) + b'context-settings'
        settings_dict = cache_get(cache_key)
    if not settings_dict:
        settings.use_editable()
        settings_dict = TemplateSettings()
        for k in settings.TEMPLATE_ACCESSIBLE_SETTINGS:
            settings_dict[k] = getattr(settings, k, b'')

        for k in DEPRECATED:
            settings_dict[k] = getattr(settings, k, DEPRECATED)

        if cache_settings:
            cache_set(cache_key, settings_dict)
    if settings.WLADMIN_INSTALLED:
        settings_dict[b'shuyucms_ADMIN_PREFIX'] = b'wladmin/'
    else:
        settings_dict[b'shuyucms_ADMIN_PREFIX'] = b'admin/'
    return {b'settings': settings_dict}