# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_apps/tethys_apps/app_harvester.py
# Compiled at: 2014-11-19 18:34:09
"""
********************************************************************************
* Name: app_harvester
* Author: Nathan Swain and Scott Christensen
* Created On: August 19, 2013
* Copyright: (c) Brigham Young University 2013
* License: BSD 2-Clause
********************************************************************************
"""
import os, inspect
from tethys_apps.base import TethysAppBase
from terminal_colors import TerminalColors

class SingletonAppHarvester(object):
    """
    Collects information for initiating apps
    """
    apps = []
    _instance = None

    def harvest_apps(self):
        """
        Searches the apps package for apps
        """
        print TerminalColors.BLUE + 'Loading Tethys Apps...' + TerminalColors.ENDC
        apps_dir = os.path.join(os.path.dirname(__file__), 'tethysapp')
        app_packages_list = os.listdir(apps_dir)
        self._harvest_app_instances(app_packages_list)

    def __new__(self):
        """
        Make App Harvester a Singleton
        """
        if not self._instance:
            self._instance = super(SingletonAppHarvester, self).__new__(self)
        return self._instance

    @staticmethod
    def _validate_app(app):
        """
        Validate the app data that needs to be validated. Returns either the app if valid or None if not valid.
        """
        if app.icon != '' and app.icon[0] == '/':
            app.icon = app.icon[1:]
        if app.color != '' and app.color[0] != '#':
            app.color = ('#{0}').format(app.color)
        if len(app.color) != 7 and len(app.color) != 4:
            app.color = ''
        return app

    def _harvest_app_instances(self, app_packages_list):
        """
        Search each app package for the app.py module. Find the AppBase class in the app.py
        module and instantiate it. Save the list of instantiated AppBase classes.
        """
        valid_app_instance_list = []
        loaded_apps = []
        for app_package in app_packages_list:
            if app_package not in ('__init__.py', '__init__.pyc', '.gitignore', '.DS_Store'):
                app_module_name = ('.').join(['tethys_apps.tethysapp', app_package, 'app'])
                app_module = __import__(app_module_name, fromlist=[''])
                for name, obj in inspect.getmembers(app_module):
                    try:
                        if issubclass(obj, TethysAppBase) and obj is not TethysAppBase:
                            _appClass = getattr(app_module, name)
                            app_instance = _appClass()
                            validated_app_instance = self._validate_app(app_instance)
                            if validated_app_instance:
                                valid_app_instance_list.append(validated_app_instance)
                                loaded_apps.append(app_package)
                    except TypeError:
                        pass
                    except:
                        raise

        self.apps = valid_app_instance_list
        print ('Tethys Apps Loaded: {0}').format((' ').join(loaded_apps))