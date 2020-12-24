# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/basico/services/srv_settings.py
# Compiled at: 2019-03-31 12:04:48
# Size of source mod 2**32: 2225 bytes
"""
# File: srv_settings.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Settings service
"""
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Pango
from gi.repository.GdkPixbuf import Pixbuf
import json
from basico.core.mod_srv import Service
from basico.core.mod_env import FILE

class Settings(Service):

    def initialize(self):
        self.log.debug('Basico config file: %s' % FILE['CNF'])
        config = self.load()

    def get(self, section, key):
        config = self.load()
        try:
            return config[section][key]
        except Exception as error:
            self.log.error(error)
            return

    def set(self, section, key, value):
        config = self.load()
        try:
            config[section][key] = value
            self.log.debug('[%s][%s] = %s' % (section, key, value))
            self.save(config)
        except:
            self.log.error('Setting not saved')
            self.log.error(self.get_traceback())

    def load(self):
        try:
            with open(FILE['CNF'], 'r') as (fp):
                config = json.load(fp)
        except Exception as error:
            self.log.debug('Config file not found. Creating a new one')
            config = {}
            self.save(config)

        return config

    def save(self, config=None):
        if config is None:
            self.log.error('A dictionary with all settings must be provided')
            return
        with open(FILE['CNF'], 'w') as (fp):
            json.dump(config, fp)
        self.log.debug('Settings saved successfully')