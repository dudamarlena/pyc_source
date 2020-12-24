# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/fragments/config.py
# Compiled at: 2012-11-06 05:50:09
from __future__ import unicode_literals
import os, sys, json
from . import FragmentsError, __version__
configuration_file_name = b'config.json'
configuration_directory_name = b'_fragments'

class ConfigurationError(FragmentsError):
    pass


class ConfigurationDirectoryNotFound(ConfigurationError):
    pass


class ConfigurationFileNotFound(ConfigurationError):
    pass


class ConfigurationFileCorrupt(ConfigurationError):
    pass


def find_configuration(current=None):
    current = current or os.getcwd()
    path = current
    while True:
        configuration_path = os.path.join(path, configuration_directory_name)
        if os.path.exists(path) and os.path.exists(configuration_path):
            return configuration_path
        path, oldpath = os.path.split(path)[0], path
        if oldpath == path:
            raise ConfigurationDirectoryNotFound(b'Could not find fragments configuration directory in %r or any parent directories' % current)


class FragmentsConfig(dict):
    defaults = {b'files': {}, b'version': __version__}

    def __init__(self, directory=None, autoload=True):
        if directory is None:
            directory = find_configuration()
        self.directory = directory
        self.path = os.path.join(self.directory, configuration_file_name)
        self.root = os.path.split(self.directory)[0]
        self.update(FragmentsConfig.defaults)
        if autoload:
            self.load()
        return

    def load(self):
        if os.access(self.path, os.R_OK | os.W_OK):
            with open(self.path, b'r') as (config_file):
                file_contents = config_file.read()
            try:
                parsed_json = json.loads(file_contents)
            except Exception as exc:
                raise ConfigurationFileCorrupt(exc.args[0])

            self.update(parsed_json)
            self[b'version'] = tuple(self[b'version'])
        else:
            raise ConfigurationFileNotFound(b'Could not access %r, if the file exists, check its permissions' % self.path)

    def dump(self):
        self[b'version'] = __version__
        with open(self.path, b'w') as (config):
            config.write(json.dumps(self, sort_keys=True, indent=4))