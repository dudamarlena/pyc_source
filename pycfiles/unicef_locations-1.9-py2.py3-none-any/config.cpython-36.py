# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jojo/workspace/locations/src/unicef_locations/config.py
# Compiled at: 2019-01-11 08:45:53
# Size of source mod 2**32: 2325 bytes
from django.core.exceptions import ImproperlyConfigured
from django.core.signals import setting_changed
from django.urls import get_callable

class AppSettings(object):
    defaults = {'GET_CACHE_KEY':'unicef_locations.cache.get_cache_key', 
     'CACHE_VERSION_KEY':'locations-etag-version'}

    def __init__(self, prefix):
        """
        Loads our settings from django.conf.settings, applying defaults for any
        that are omitted.
        """
        self.prefix = prefix
        setting_changed.connect(self._handler)

    def __getattr__(self, name):
        if name in self.defaults.keys():
            from django.conf import settings
            name_with_prefix = (self.prefix + '_' + name).upper()
            raw_value = getattr(settings, name_with_prefix, self.defaults[name])
            value = self._set_attr(name_with_prefix, raw_value)
            setattr(settings, name_with_prefix, raw_value)
            setting_changed.send((self.__class__), setting=name_with_prefix, value=raw_value, enter=True)
            return value
        else:
            return super(AppSettings, self).__getattr__(name)

    def _set_attr(self, prefix_name, value):
        name = prefix_name[len(self.prefix) + 1:]
        if name in ('GET_CACHE_KEY', 'GET_CACHE_VERSION'):
            try:
                if isinstance(value, str):
                    func = get_callable(value)
                else:
                    if callable(value):
                        func = value
                    else:
                        raise ImproperlyConfigured(f"{value} is not a valid value for `{name}`. It must be a callable or a fullpath to callable. ")
            except Exception as e:
                raise ImproperlyConfigured(e)

            setattr(self, name, func)
            return func
        else:
            setattr(self, name, value)
            return value

    def _handler(self, sender, setting, value, **kwargs):
        """
            handler for ``setting_changed`` signal.

        @see :ref:`django:setting-changed`_
        """
        if setting.startswith(self.prefix):
            name = setting[len(self.prefix) + 1:]
            try:
                delattr(self, name)
            except AttributeError:
                pass


conf = AppSettings('UNICEF_LOCATIONS')