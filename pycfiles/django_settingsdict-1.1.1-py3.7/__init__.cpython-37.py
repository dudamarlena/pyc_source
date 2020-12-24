# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_settingsdict/__init__.py
# Compiled at: 2019-07-29 09:44:35
# Size of source mod 2**32: 4134 bytes
import warnings
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test.signals import setting_changed
from django.utils.deprecation import RemovedInNextVersionWarning
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

def _migrate_vals(vals):
    if len(vals) == 2:
        return (
         vals[0], vals[1], None)
    if len(vals) == 3:
        return tuple(vals)
    raise ValueError('SettingsDict(migrate=..) requires list of tuples with length 2-3. Found %r' % (
     vals,))


class SettingsDict(object):
    _INTERNAL = frozenset(('_name', '_defaults', '_required', '_removed', '_import_strings',
                           '_migrate'))

    def __init__(self, name, *, defaults=None, required=None, removed=None, import_strings=None, migrate=None):
        self._name = name
        self._defaults = defaults or {}
        self._required = frozenset(required or ())
        self._removed = frozenset(removed or ())
        self._import_strings = frozenset(import_strings or ())
        self._migrate = tuple((_migrate_vals(x) for x in migrate)) if migrate else ()
        self._listen_for_changes()

    @cached_property
    def _user_settings(self):
        """
        Resolve settings dict from django settings module.
        Validate that all the required keys are present and also that none of
        the removed keys do.
        Result is cached.
        """
        user_settings = getattr(settings, self._name, {})
        for new_name, old_name, script in self._migrate:
            if new_name not in user_settings:
                if hasattr(settings, old_name):
                    warnings.warn(('Configuration parameter %s has moved to %s.%s. Please update your local configuration.' % (
                     old_name, self._name, new_name)),
                      category=RemovedInNextVersionWarning,
                      stacklevel=3)
                    value = getattr(settings, old_name)
                    if script:
                        value = script(value, user_settings)
                user_settings[new_name] = value

        if not user_settings:
            if self._required:
                raise ImproperlyConfigured('Settings file is missing dict options with name {}'.format(self._name))
        keys = frozenset(user_settings.keys())
        required = self._required - keys
        if required:
            raise ImproperlyConfigured('Following options for {} are missing from settings file: {}'.format(self._name, ', '.join(sorted(required))))
        removed = keys & self._removed
        if removed:
            raise ImproperlyConfigured('Following options for {} have been removed: {}'.format(self._name, ', '.join(sorted(removed))))
        return user_settings

    def __getattr__(self, key):
        """
        Any attribute request that isn't known before (e.g. cached or
        defined in class) will be resolved as option.
        If value is not found from user provided settings default is used.
        If key is marked as import, value is imported using django.
        Result is cached.
        """
        if key not in self._defaults:
            if key not in self._required:
                raise AttributeError('Invalid {} setting {}'.format(self._name, key))
        try:
            val = self._user_settings[key]
        except KeyError:
            val = self._defaults[key]

        if val:
            if key in self._import_strings:
                val = import_string(val)
        setattr(self, key, val)
        return val

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

    def _clear_cached(self):
        remove = set(self.__dict__.keys()) - self._INTERNAL
        for key in remove:
            del self.__dict__[key]

    def _reload_event(self, **kwargs):
        if kwargs.get('setting') == self._name:
            self._clear_cached()

    def _listen_for_changes(self):
        setting_changed.connect(self._reload_event)