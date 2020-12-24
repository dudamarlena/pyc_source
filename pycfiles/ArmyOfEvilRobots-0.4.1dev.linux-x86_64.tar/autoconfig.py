# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/armyofevilrobots/autoconfig.py
# Compiled at: 2009-10-13 00:24:04
import os, sys, ConfigParser, os.path
config = None

class AutoConfig(ConfigParser.SafeConfigParser):

    def __init__(self, defaults={}, dict_type=dict, appname=None, configpath=False):
        """Autogenerates a config file if needed, figures out where it lives,
        and works correctly in windows even (I think)"""
        if appname == None:
            appname = 'foo'
        self.appname = appname
        if not configpath:
            try:
                from win32com.shell import shellcon, shell
                homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
                configpath = os.path.join(homedir, appname)
                if not os.path.exists(configpath):
                    os.makedirs(configpath)
            except ImportError:
                homedir = os.path.expanduser('~')
                configpath = os.path.join(homedir, '.%s' % appname)
                if not os.path.exists(configpath):
                    os.makedirs(configpath)

        self.configpath = configpath
        self.configfile = os.path.join(configpath, 'config.ini')
        defaults['configfile'] = self.configfile
        defaults['configpath'] = self.configpath
        ConfigParser.SafeConfigParser.__init__(self, defaults, dict_type)
        if not os.path.exists(self.configfile):
            self.add_section(appname)
            self.save()
        self.read(self.configfile)
        return

    def save(self):
        fp = open(self.configfile, 'w+')
        self.write(fp)
        fp.close()


def getapp():
    global config
    if config.__class__ == AutoConfig:
        return config.appname
    raise ConfigParser.Error('Cannot get appname unless you run start() first.')


def revert(appname, defaults={}, configpath=False):
    """Discard the current config and reload/regen"""
    global config
    config = AutoConfig(defaults, dict, appname)


def start(appname, defaults={}, configpath=False):
    """Safe start for the config, will not hammer a running config"""
    if config.__class__ != AutoConfig:
        revert(appname, defaults, configpath)


def get(section, key, default=None):
    """Get a key, default allowed"""
    if config.__class__ == AutoConfig:
        if config.has_option(section, key):
            return config.get(section, key)
        else:
            return default
    else:
        raise ConfigParser.Error('Cannot get keys unless you run start() first.')


def iterate(section):
    if config.__class__ == AutoConfig:
        try:
            for (name, value) in config.items(section):
                if name not in config.defaults().keys():
                    yield (
                     name, value)

        except ConfigParser.NoSectionError:
            return

    else:
        raise ConfigParser.Error('Cannot get keys unless you run start() first.')


def set(section, key, value):
    """Set a value in the config. Will not persist unless you hit save() too."""
    if config.__class__ == AutoConfig:
        if not config.has_section(section):
            config.add_section(section)
        return config.set(section, key, value)
    raise ConfigParser.Error('Cannot get keys unless you run start() first.')


def save():
    """Save the config to the initialized filename"""
    if config.__class__ == AutoConfig:
        config.save()
    else:
        raise ConfigParser.Error('Cannot save configuration unless it is initialized first.')