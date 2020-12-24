# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/blackdog/plugin.py
# Compiled at: 2014-07-24 15:50:38
# Size of source mod 2**32: 5121 bytes
"""
BlackDog

Copyright (C) 2014 Snaipe, Therozin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import hashlib, re
from configparser import ConfigParser
from enum import Enum
from string import Template
from blackdog import NoSuchPluginVersionException
from blackdog.config import load, save, config_node

class PluginStage(Enum):
    planning = 'p'
    alpha = 'a'
    beta = 'b'
    release = 'r'
    mature = 'm'
    inactive = 'i'
    abandoned = 'x'
    deleted = 'd'

    @classmethod
    def from_string(cls, string):
        if string:
            return getattr(PluginStage, string.lower(), None)


class Plugin(object):

    def __init__(self, name):
        self.name = name
        self.path_name = re.sub('[^a-zA-Z0-9_\\-]', '_', name)
        self.versions = {}

    @config_node('summary')
    def summary(self):
        pass

    @config_node('display-name')
    def display_name(self):
        return self.name

    @config_node('stage')
    def stage(self):
        pass

    @config_node('exists', type=bool)
    def exists(self):
        pass

    def add_version(self, version):
        self.versions[version.get_version()] = version

    def get_version(self, version):
        try:
            return self.versions[version]
        except KeyError as e:
            raise NoSuchPluginVersionException(e.args[0])

    def has_version(self, version):
        return version in self.versions

    def _get_config(self, directory):
        from os.path import join
        return join(directory, self.path_name + '.data')

    def load(self, directory):
        """
        Loads all available plugin metadata from cache
        :param directory: the cache root directory
        :return: the plugin itself
        """
        config = ConfigParser()
        config.read(self._get_config(directory))
        load(config, self, 'plugin')
        for section in [s for s in config.sections() if s != 'plugin']:
            version = PluginVersion(self, section)
            load(config, version, section)
            self.versions[section] = version

        return self

    def save(self, directory):
        """
        Saves all available plugin metadata to cache
        :param directory: the cache root directory
        :return: the plugin itself
        """
        config = ConfigParser()
        save(config, self, 'plugin')
        for vstr, version in self.versions.items():
            save(config, version, vstr)

        with open(self._get_config(directory), 'w') as (fd):
            config.write(fd)
        return self


class PluginVersion(object):
    _PluginVersion__POM_BASE = '<?xml version="1.0" encoding="UTF-8"?>\n<project xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"\n    xmlns="http://maven.apache.org/POM/4.0.0"\n    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n    <modelVersion>4.0.0</modelVersion>\n    <groupId>${groupid}</groupId>\n    <artifactId>${artifactid}</artifactId>\n    <version>${version}</version>\n</project>'

    def __init__(self, plugin: Plugin, version):
        if not version or not plugin:
            raise ValueError('plugin or version cannot be None')
        self._PluginVersion__plugin = plugin
        self._PluginVersion__version = version

    @config_node('url')
    def url(self):
        pass

    @config_node('sha1')
    def sha1(self):
        pass

    @config_node('md5')
    def md5(self):
        pass

    @config_node('date')
    def date(self):
        pass

    @config_node('stage', type=PluginStage)
    def stage(self):
        pass

    @config_node('game-versions', type=list)
    def game_versions(self):
        pass

    def can_download(self):
        return self.url() and self.md5()

    def get_version(self):
        return self._PluginVersion__version

    def get_plugin(self):
        return self._PluginVersion__plugin

    def get_pom(self, groupid):
        return Template(PluginVersion._PluginVersion__POM_BASE).substitute(groupid=groupid, artifactid=self._PluginVersion__plugin.name, version=self._PluginVersion__version)

    def __get_pom_hash(self, groupid, hash):
        hash.update(self.get_pom(groupid).encode('ascii'))
        return hash.hexdigest()

    def get_pom_md5(self, groupid):
        return self._PluginVersion__get_pom_hash(groupid, hashlib.md5())

    def get_pom_sha1(self, groupid):
        return self._PluginVersion__get_pom_hash(groupid, hashlib.sha1())