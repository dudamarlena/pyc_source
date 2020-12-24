# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/usersettings.py
# Compiled at: 2013-05-31 19:59:22
"""
Provide interface for persistent portable editable user settings
"""
import os, ConfigParser, ast, appdirs

class Settings(dict):
    """ Provide interface for portable persistent user editable settings """
    app_id = None
    settings_directory = None
    settings_file = None
    _settings_types = {}
    _settings_defaults = {}

    def __init__(self, app_id):
        """
        Create the settings object, using the specified app id (a reversed rfc
        1034 identifier, e.g. com.example.apps.thisapp
        """
        self.app_id = app_id
        self.settings_directory = appdirs.user_data_dir(app_id, appauthor=app_id, roaming=True)
        self.settings_file = os.path.join(self.settings_directory, 'settings.cfg')
        super(Settings, self).__init__()

    def add_setting(self, setting_name, setting_type=str, default=None):
        """ Define a settings option (and default value) """
        self._settings_types[setting_name] = setting_type
        self._settings_defaults[setting_name] = default

    def load_settings(self):
        """ Set default values and parse stored settings file """
        for key, value in self._settings_defaults.items():
            if key not in self._settings_types:
                self._settings_types[key] = str
            super(Settings, self).__setitem__(key, value)

        parser = ConfigParser.RawConfigParser()
        try:
            with open(self.settings_file, 'r') as (settings_fp):
                parser.readfp(settings_fp)
                for key, value in parser.items('settings'):
                    if key not in self._settings_types:
                        self._settings_types[key] = str
                    adjusted_value = value
                    if issubclass(self._settings_types[key], bool):
                        adjusted_value = parser.getboolean('settings', key)
                    elif issubclass(self._settings_types[key], int):
                        adjusted_value = parser.getint('settings', key)
                    elif issubclass(self._settings_types[key], float):
                        adjusted_value = parser.getfloat('settings', key)
                    elif issubclass(self._settings_types[key], (
                     dict, list, set)):
                        adjusted_value = self._settings_types[key](ast.literal_eval(value))
                    else:
                        adjusted_value = self._settings_types[key](value)
                    super(Settings, self).__setitem__(key, adjusted_value)

        except IOError:
            pass

    def save_settings(self):
        """ Write the settings data to disk """
        if not os.path.exists(self.settings_directory):
            os.makedirs(self.settings_directory, 493)
        parser = ConfigParser.RawConfigParser()
        parser.add_section('settings')
        for key, value in self.items():
            parser.set('settings', key, value)

        with open(self.settings_file, 'wb') as (settings_fp):
            parser.write(settings_fp)

    def __getattr__(self, setting_name):
        """ Provide attribute-based access to stored config data """
        try:
            return super(Settings, self).__getitem__(setting_name)
        except KeyError:
            raise AttributeError

    def __setattr__(self, setting_name, setting_value):
        """ Provide attribute-based access to stored config data """
        if setting_name in self._settings_defaults:
            try:
                return super(Settings, self).__setitem__(setting_name, setting_value)
            except KeyError:
                raise AttributeError

        return super(Settings, self).__setattr__(setting_name, setting_value)