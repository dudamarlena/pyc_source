# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/AsteriskChannelHangup/Config.py
# Compiled at: 2009-12-29 13:06:45
"""
Config.py: filesystem configuration reader.
"""
import os, ConfigParser, Asterisk
CONFIG_FILENAME = 'py-asterisk.conf'
CONFIG_PATHNAMES = [
 os.environ.get('PYASTERISK_CONF', ''),
 os.path.join(os.environ.get('HOME', ''), '.py-asterisk.conf'),
 os.path.join(os.environ.get('USERPROFILE', ''), 'py-asterisk.conf'),
 'py-asterisk.conf',
 '/etc/py-asterisk.conf',
 '/etc/asterisk/py-asterisk.conf']

class ConfigurationError(Asterisk.BaseException):
    """This exception is raised when there is a problem with the configuration."""
    _prefix = 'configuration error'


class Config(object):

    def _find_config(self, config_pathname):
        """
        Search the filesystem paths listed in CONFIG_PATHNAMES for a regular file.
        Return the name of the first one found, or <config_pathname>, if it is not
        None.
        """
        if config_pathname is None:
            for pathname in CONFIG_PATHNAMES:
                if os.path.exists(pathname):
                    config_pathname = pathname
                    break

        if config_pathname is None:
            raise ConfigurationError('cannot find a suitable configuration file.')
        return config_pathname

    def refresh(self):
        """Read py-Asterisk configuration data from the filesystem."""
        try:
            self.conf = ConfigParser.SafeConfigParser()
            self.conf.readfp(file(self.config_pathname))
        except ConfigParser.Error, e:
            raise ConfigurationError('%r contains invalid data at line %r' % (
             self.config_pathname, e.lineno))

    def __init__(self, config_pathname=None):
        config_pathname = self._find_config(config_pathname)
        if config_pathname is None:
            raise ConfigurationError('could not find a configuration file.')
        self.config_pathname = config_pathname
        self.refresh()
        return

    def get_connection(self, connection=None):
        """
        Return an (address, username, secret) argument tuple, suitable for
        initialising a Manager instance. If <connection> is specified, use
        the named <connection> instead of the configuration default.
        """
        conf = self.conf
        try:
            if connection is None:
                connection = conf.get('py-asterisk', 'default connection')
            items = dict(conf.items('connection: ' + connection))
        except ConfigParser.Error, e:
            raise ConfigurationError(str(e))

        try:
            address = (items['hostname'], int(items['port']))
        except ValueError:
            raise ConfigurationError('The port number specified in profile %r is not valid.' % profile)

        return (
         address, items['username'], items['secret'])

    def get_max_time_for_calls(self, connection=None):
        """
        Retorna el tiempo maximo de llamadas
        """
        conf = self.conf
        try:
            if connection is None:
                connection = conf.get('py-asterisk', 'default connection')
            items = dict(conf.items('connection: ' + connection))
        except ConfigParser.Error, e:
            raise ConfigurationError(str(e))

        try:
            tiempo_max_de_llamadas = items['tiempo_max_de_llamadas']
        except ValueError:
            raise ConfigurationError('El tiempo max de llamadas no esta definido')
        except KeyError:
            print 'El tiempo max de llamadas no esta definido'
            return

        return tiempo_max_de_llamadas