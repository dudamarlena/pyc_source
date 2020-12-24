# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mygrate/config.py
# Compiled at: 2014-07-18 08:16:56
import os, os.path
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
from .exceptions import MygrateError

class MygrateConfigError(MygrateError):
    """Informational exception for bad MyGrate configuration."""
    pass


class MygrateConfig(object):

    def __init__(self, section='mygrate'):
        self.section = section
        self.parser = SafeConfigParser()
        self.parser.optionxform = str
        fnames = self._get_paths()
        if not self.parser.read(fnames):
            raise MygrateConfigError('No valid config files in ' + repr(fnames))

    def _get_paths(self):
        env_config = os.getenv('MYGRATE_CONFIG', None)
        if env_config:
            return [os.path.expanduser(env_config)]
        else:
            home_config = os.path.expanduser('~/.mygrate.conf')
            global_config = '/etc/mygrate.conf'
            return [home_config, global_config]
            return

    def call_entry_point(self, callbacks):
        try:
            entry_point = self.parser.get(self.section, 'entry_point')
        except (NoSectionError, NoOptionError):
            msg = 'Please specify entry_point in configuration'
            raise MygrateConfigError(msg)

        mod_name, attr_name = entry_point.rsplit(':', 1)
        mod = __import__(mod_name, fromlist=[attr_name])
        func = getattr(mod, attr_name)
        func(callbacks, self)

    def get_mysql_connection_info(self, section=None):
        section = section or self.section
        ret = {}
        mapping = {'host': 'host', 'port': 'port', 
           'user': 'user', 
           'passwd': 'password', 
           'db': 'database', 
           'unix_socket': 'unix_socket', 
           'charset': 'charset'}
        for key, value in mapping.items():
            try:
                ret[key] = self.parser.get(section, value)
            except (NoSectionError, NoOptionError):
                pass

        return ret

    def get_mysql_binlog_info(self):
        try:
            index_file = self.parser.get(self.section, 'index_file')
        except (NoSectionError, NoOptionError):
            index_file = '/var/lib/mysql/mysql-bin.index'

        if not os.path.exists(index_file):
            raise MygrateConfigError('Invalid binlog index file: ' + index_file)
        try:
            delay = self.parser.getfloat(self.section, 'tracking_delay')
        except (NoSectionError, NoOptionError):
            delay = 1.0

        return (
         index_file, float(delay))

    def get_tracking_dir(self):
        try:
            tracking_dir = self.parser.get(self.section, 'tracking_dir')
        except (NoSectionError, NoOptionError):
            tracking_dir = os.path.expanduser('~/.binlog-tracking')
            try:
                os.makedirs(tracking_dir)
            except OSError:
                pass

        tracking_dir = os.path.expanduser(tracking_dir)
        if not os.path.isdir(tracking_dir):
            msg = 'Tracking directory does not exist: ' + tracking_dir
            raise MygrateConfigError(msg)
        return tracking_dir


cfg = MygrateConfig()