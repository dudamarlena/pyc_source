# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/framework/Config.py
# Compiled at: 2016-12-16 14:55:45
"""Handle the config file and such for the Skytap system."""
import json, os, six, skytap.framework.Utils as Utils
INITIAL_CONFIG = {'user': '', 'token': '', 
   'log_level': 30, 
   'base_url': 'https://cloud.skytap.com', 
   'max_http_attempts': 4, 
   'retry_wait': 10, 
   'add_note_on_state_change': True}

class ConfigType(type):
    """A meta class for Config.

    This allows magic methods to be used on the Config class, making things
    like 'Config.token' work as well as len(Config) even when Config is a class
    and not an object. This makes for cleaner use in other classes.
    """

    def __getattr__(cls, key):
        """Make the config values accessible.

        This allows all config values to be available via calls like:
        Config.user
        """
        if key not in cls.config_data:
            if key not in ('__test__', 'address', 'im_class', '__self__'):
                Utils.error("Tried to access config value '" + str(key) + "', which doesn't exist.")
            raise AttributeError
        return cls.config_data[key]

    def __len__(cls):
        """Expose how many config items we have."""
        return len(cls.config_data)

    def __str__(cls):
        """A string representation of the config, JSON formatted, and prettified.

        Token is excluded from this, so this can be safely printed for
        debugging.
        """
        temp_config = cls.config_data.copy()
        temp_config['token'] = ''
        return json.dumps(temp_config, indent=4)

    def __repr__(cls):
        """A string representation of the config, JSON formatted.

        Token is excluded from this, so this can be safely printed for
        debugging.
        """
        temp_config = cls.config_data.copy()
        temp_config['token'] = ''
        return json.dumps(temp_config)

    def __dir__(cls):
        """List only items in the config_data list.

        Polite since we're implementing __getattr__.
        """
        dir_list = []
        for config_item in cls.config_data:
            dir_list.append(config_item)

        return dir_list

    def __contains__(cls, item):
        """Allow checks for items in the config list."""
        return item in cls.config_data

    def __iter__(cls):
        """Allow 'for x in config'.

        Ultimately, this passes the 'how to iterate' problem down to the
        config_data object and lets that object handle the actual iteration.
        """
        return iter(cls.config_data)


@six.add_metaclass(ConfigType)
class Config(object):
    """Contain all of our config values into this object."""
    config_data = INITIAL_CONFIG


for key in Config:
    env_val = 'SKYTAP_' + key.upper()
    if env_val in os.environ:
        Config.config_data[key] = os.environ[env_val]
        try:
            Config.config_data[key] = int(Config.config_data[key])
        except ValueError:
            pass

if os.environ.get('READTHEDOCS', None) != 'True':
    if Config.base_url != 'https://cloud.skytap.com':
        Utils.warning("Base URL is not Skytap's recommended value. " + 'This very likely will break things.')
    if len(Config.token) == 0:
        Utils.error('No environment variable SKYTAP_TOKEN found. ' + 'Set this variable and try again.')
        raise ValueError
    if len(Config.user) == 0:
        Utils.error('No environment variable SKYTAP_USER found. ' + 'Set this variable and try again.')
        raise ValueError
Utils.log_level(Config.log_level)