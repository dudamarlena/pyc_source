# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/settings.py
# Compiled at: 2015-06-18 14:53:29
# Size of source mod 2**32: 992 bytes
from morfdict import Factory

class SettingsFactory(object):
    __doc__ = '\n    This class will generate settings for different endpoints.\n    '
    ENDPOINTS = {'uwsgi': [('local', False)], 
     'tests': [('tests', False)], 
     'shell': [('shell', False), ('local_shell', False)], 
     'command': [('command', False), ('local_command', False)]}

    def __init__(self, module, settings=None, paths=None):
        self.module = module
        self.settings = settings or {}
        self.paths = paths or {}

    def get_for(self, endpoint):
        files = self.ENDPOINTS[endpoint]
        return self._generate_settings(files)

    def _generate_settings(self, files=None):
        files = files or []
        factory = Factory(self.module)
        settings, paths = factory.make_settings(settings=self.settings, paths=self.paths, additional_modules=files)
        settings['paths'] = paths
        return (settings, paths)