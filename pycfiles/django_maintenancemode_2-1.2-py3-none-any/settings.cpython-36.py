# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/btaylor/work/python-projects/django-maintenancemode-2/maintenancemode/utils/settings.py
# Compiled at: 2019-12-22 19:32:47
# Size of source mod 2**32: 4608 bytes
from inspect import getmembers
from django import get_version
from django.conf import settings
from distutils.version import StrictVersion
DJANGO_VERSION = StrictVersion(get_version())
MAINTENANCE_503_TEMPLATE = getattr(settings, 'MAINTENANCE_503_TEMPLATE', '503.html')
MAINTENANCE_ADMIN_IGNORED_URLS = getattr(settings, 'MAINTENANCE_ADMIN_IGNORED_URLS', [
 '^admin'])
MAINTENANCE_BLOCK_STAFF = getattr(settings, 'MAINTENANCE_BLOCK_STAFF', False)

class AppSettings(object):
    __doc__ = '\n    An app setting object to be used for handling app setting defaults\n    gracefully and providing a nice API for them. Say you have an app\n    called ``myapp`` and want to define a few defaults, and refer to the\n    defaults easily in the apps code. Add a ``settings.py`` to your app::\n\n        from path.to.utils import AppSettings\n\n        class MyAppSettings(AppSettings):\n            SETTING_1 = "one"\n            SETTING_2 = (\n                "two",\n            )\n\n    Then initialize the setting with the correct prefix in the location of\n    of your choice, e.g. ``conf.py`` of the app module::\n\n        settings = MyAppSettings(prefix="MYAPP")\n\n    The ``MyAppSettings`` instance will automatically look at Django\'s\n    global setting to determine each of the settings and respect the\n    provided ``prefix``. E.g. adding this to your site\'s ``settings.py``\n    will set the ``SETTING_1`` setting accordingly::\n\n        MYAPP_SETTING_1 = "uno"\n\n    Usage\n    -----\n\n    Instead of using ``from django.conf import settings`` as you would\n    usually do, you can switch to using your apps own settings module\n    to access the app settings::\n\n        from myapp.conf import settings\n\n        print myapp_settings.MYAPP_SETTING_1\n\n    ``AppSettings`` instances also work as pass-throughs for other\n    global settings that aren\'t related to the app. For example the\n    following code is perfectly valid::\n\n        from myapp.conf import settings\n\n        if "myapp" in settings.INSTALLED_APPS:\n            print "yay, myapp is installed!"\n\n    Custom handling\n    ---------------\n\n    Each of the settings can be individually configured with callbacks.\n    For example, in case a value of a setting depends on other settings\n    or other dependencies. The following example sets one setting to a\n    different value depending on a global setting::\n\n        from django.conf import settings\n\n        class MyCustomAppSettings(AppSettings):\n            ENABLED = True\n\n            def configure_enabled(self, value):\n                return value and not self.DEBUG\n\n        custom_settings = MyCustomAppSettings("MYAPP")\n\n    The value of ``custom_settings.MYAPP_ENABLED`` will vary depending on the\n    value of the global ``DEBUG`` setting.\n\n    Each of the app settings can be customized by providing\n    a method ``configure_<lower_setting_name>`` that takes the default\n    value as defined in the class attributes as the only parameter.\n    The method needs to return the value to be use for the setting in\n    question.\n    '

    def __dir__(self):
        return sorted(list(set(self.__dict__.keys() + dir(settings))))

    __members__ = lambda self: self.__dir__()

    def __getattr__(self, name):
        if name.startswith(self._prefix):
            raise AttributeError('{0} object has no attribute {1}'.format((
             self.__class__.__name__, name)))
        return getattr(settings, name)

    def __setattr__(self, name, value):
        super(AppSettings, self).__setattr__(name, value)
        if name in dir(settings):
            setattr(settings, name, value)

    def __init__(self, prefix):
        super(AppSettings, self).__setattr__('_prefix', prefix)
        for setting, class_value in getmembers(self.__class__):
            if setting == setting.upper():
                prefixed = '{0}_{1}'.format(prefix.upper(), setting.upper())
                configured_value = getattr(settings, prefixed, class_value)
                callback_name = 'configure_{}'.format(setting.lower())
                callback = getattr(self, callback_name, None)
                if callable(callback):
                    configured_value = callback(configured_value)
                delattr(self.__class__, setting)
                setattr(self, prefixed, configured_value)