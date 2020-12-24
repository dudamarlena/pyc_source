# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/runner/importer.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import imp, six, sys, click

def install(name, config_path, default_settings, callback=None):
    sys.meta_path.append(Importer(name, config_path, default_settings, callback))


class ConfigurationError(ValueError, click.ClickException):

    def show(self, file=None):
        if file is None:
            from click._compat import get_text_stderr
            file = get_text_stderr()
        click.secho('!! Configuration error: %s' % self.format_message(), file=file, fg='red')
        return


class Importer(object):

    def __init__(self, name, config_path, default_settings=None, callback=None):
        self.name = name
        self.config_path = config_path
        self.default_settings = default_settings
        self.callback = callback

    def __repr__(self):
        return "<%s for '%s' (%s)>" % (type(self), self.name, self.config_path)

    def find_module(self, fullname, path=None):
        if fullname != self.name:
            return
        return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        else:
            try:
                mod = self._load_module(fullname)
            except Exception as e:
                from sentry.utils.settings import reraise_as
                msg = six.text_type(e)
                if msg:
                    msg = '%s: %s' % (type(e).__name__, msg)
                else:
                    msg = type(e).__name__
                reraise_as(ConfigurationError(msg))
            else:
                sys.modules[fullname] = mod
                if self.callback is not None:
                    self.callback(mod)
                return mod

            return

    def _load_module(self, fullname):
        if self.default_settings:
            from importlib import import_module
            default_settings_mod = import_module(self.default_settings)
        else:
            default_settings_mod = None
        settings_mod = imp.new_module(self.name)
        settings_mod.__file__ = self.config_path
        load_settings(default_settings_mod, settings=settings_mod)
        load_settings(self.config_path, settings=settings_mod, silent=True)
        install_plugin_apps('sentry.apps', settings_mod)
        return settings_mod


def load_settings(mod_or_filename, settings, silent=False):
    if isinstance(mod_or_filename, six.string_types):
        conf = imp.new_module('temp_config')
        conf.__file__ = mod_or_filename
        try:
            with open(mod_or_filename) as (source_file):
                six.exec_(source_file.read(), conf.__dict__)
        except IOError as e:
            import errno
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return settings
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise

    else:
        conf = mod_or_filename
    add_settings(conf, settings=settings)


def install_plugin_apps(entry_point, settings):
    from pkg_resources import iter_entry_points
    installed_apps = list(settings.INSTALLED_APPS)
    for ep in iter_entry_points(entry_point):
        if ep.module_name not in installed_apps:
            installed_apps.append(ep.module_name)

    settings.INSTALLED_APPS = tuple(installed_apps)


def add_settings(mod, settings):
    """
    Adds all settings that are part of ``mod`` to the global settings object.
    Special cases ``EXTRA_APPS`` to append the specified applications to the
    list of ``INSTALLED_APPS``.
    """
    for setting in dir(mod):
        if not setting.isupper():
            continue
        setting_value = getattr(mod, setting)
        if setting in ('INSTALLED_APPS', 'TEMPLATE_DIRS') and isinstance(setting_value, six.string_types):
            setting_value = (setting_value,)
        if setting[:6] == 'EXTRA_':
            base_setting = setting[6:]
            if isinstance(getattr(settings, base_setting), (list, tuple)):
                curval = getattr(settings, base_setting)
                setattr(settings, base_setting, curval + type(curval)(setting_value))
                continue
        setattr(settings, setting, setting_value)