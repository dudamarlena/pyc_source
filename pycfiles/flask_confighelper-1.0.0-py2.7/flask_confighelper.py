# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/flask_confighelper.py
# Compiled at: 2017-05-08 01:15:24
from os import environ

class FlaskConfigHelper(object):

    def __init__(self, app=None, config_module=None):
        self.error_count = 0
        self.app = app
        if app is not None:
            self.init_app(app, config_module)
        return

    def init_app(self, app, config_module):
        try:
            app.config['environment'] = environ['ENVIRONMENT']
        except KeyError:
            print 'ENVIRONMENT configuration not found, using default Config'
            app.config['environment'] = ''

        if config_module is None:
            app.config['config_module'] = 'config'
        else:
            app.config['config_module'] = config_module
        self.load_config()
        return

    def load_config(self):
        cfg = self.app.config['config_module']
        try:
            module = __import__(cfg)
        except NameError:
            print ('No module named {}').format(cfg)
            exit(1)

        mod = self.app.config['environment'].capitalize() + 'Config'
        obj = getattr(module, mod)
        for item in dir(obj):
            if item[0:2] != '__':
                var = getattr(obj, item)
                if var == 'required':
                    self.load_required(item)
                else:
                    self.load_optional(item)

        if self.error_count > 0:
            exit(1)

    def load_required(self, item):
        try:
            environ[item]
            self.set_config(item)
        except KeyError:
            print ('Error. {} is required, and was not found.').format(item)
            self.error_count += 1

    def load_optional(self, item):
        try:
            environ[item]
            self.set_config(item)
        except KeyError:
            pass

    def set_config(self, var):
        self.app.config[var] = environ[var]