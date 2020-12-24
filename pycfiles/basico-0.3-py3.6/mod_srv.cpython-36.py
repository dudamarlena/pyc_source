# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/core/mod_srv.py
# Compiled at: 2019-03-23 11:00:13
# Size of source mod 2**32: 3156 bytes
"""
# File: mod_srv.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Service class
"""
import sys, traceback as tb
from basico.core.mod_env import FILE
from basico.core.mod_log import get_logger

class Service(object):
    __doc__ = '\n    Service class is the base class for those modules acting as services.\n    Different modules (GUI, Database, Ask, etc...) share same methods\n    which is useful to start/stop them, simplify logging and, comunicate\n    each other easily.\n    '

    def __init__(self, app=None):
        """Initialize Service instance
        @type app: Basico instance
        @param app: current Basico instance reference
        """
        if app is not None:
            self.app = app
        self.started = False

    def is_started(self):
        """Return True or False if service is running / not running
        """
        return self.started

    def print_traceback(self):
        self.log.debug(tb.format_exc())

    def get_logger(self, logname):
        """
        Get a logger for those modules that aren't real services.
        """
        self.log = get_logger(logname)

    def start(self, app, logname, section_name):
        """Start service.
        Use initialize for writting a custom init method
        @type app: basico
        @param app: basico Class pointer.
        @type logname: string
        @param logname: name of associated logger. It is used aswell to
        identify configuration section name
        """
        self.started = True
        self.app = app
        self.section = section_name
        self.log = get_logger(logname)
        self.init_section(section_name)
        try:
            self.initialize()
        except Exception as error:
            self.log.debug(self.get_traceback())

        self.log.debug('Module %s started', logname)

    def end(self):
        """End service
        Use finalize for writting a custom end method
        """
        self.started = False
        try:
            self.finalize()
        except Exception as error:
            self.log.debug(self.get_traceback())

    def initialize(self):
        """Initialize service.
        All clases derived from Service class must implement this method
        """
        pass

    def finalize(self):
        """Finalize service.
        All clases derived from Service class must implement this method
        """
        pass

    def init_section(self, section):
        """Check if section exists in config. If not, create it"""
        self.srvstg = self.get_service('Settings')
        config = self.srvstg.load()
        try:
            config[section]
        except:
            config[section] = {}
            self.srvstg.save(config)
            self.log.debug("Section '%s' initialized in config file" % section)

    def get_traceback(self):
        """
        get traceback
        """
        return tb.format_exc()

    def get_service(self, name):
        return self.app.get_service(name)

    def get_config(self):
        self.srvstg = self.get_service('Settings')
        return self.srvstg.load()