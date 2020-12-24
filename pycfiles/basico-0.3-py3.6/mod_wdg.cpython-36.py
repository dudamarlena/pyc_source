# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/core/mod_wdg.py
# Compiled at: 2019-03-26 12:48:49
# Size of source mod 2**32: 1308 bytes
"""
# File: mod_wdg.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Basico Widget Base class
"""
import sys, traceback as tb
from basico.core.mod_env import FILE
from basico.core.mod_log import get_logger

class BasicoWidget(object):
    __doc__ = '\n    Service class is the base class for Basico widgets.\n    '
    log = None

    def __init__(self, app, logname):
        """Initialize Service instance
        @type app: Basico instance
        @param app: current Basico instance reference
        """
        if app is not None:
            self.app = app
        self.log = get_logger(logname)

    def get_traceback(self):
        """
        get traceback
        """
        return tb.format_exc()

    def get_service(self, name):
        """
        get a service
        """
        return self.app.get_service(name)

    def init_section(self, name):
        """
        Check if section exists in config. If not, create it
        """
        self.srvstg = self.get_service('Settings')
        config = self.srvstg.load()
        try:
            config['Widgets']
        except:
            config['Widgets'] = {}
            self.srvstg.save(config)
            self.log.debug("Section '%s' initialized in config file" % section)