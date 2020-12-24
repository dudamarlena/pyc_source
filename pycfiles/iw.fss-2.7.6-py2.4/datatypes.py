# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/configuration/datatypes.py
# Compiled at: 2008-10-23 05:55:16
"""
Configuration schema resources
$Id: datatypes.py 66391 2008-06-09 17:38:35Z glenfant $
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import os, types
from ZConfig.datatypes import stock_datatypes
from ZConfig.substitution import substitute

def existingStoragePath(value):
    """Validating/converting a storage path
    @param value: a storage path
    @return: valid (translated?) storage path
    """
    return _existingPath(value, 'fss_storage')


def existingBackupPath(value):
    """Validating/converting a backup path
    @param value: a backup path
    @return: valid (translated?) storage path
    """
    return _existingPath(value, 'fss_backup')


_environ = dict([ (k.lower(), v) for (k, v) in os.environ.items() ])
_paths = []

def _existingPath(value, default):
    global _environ
    global _paths
    if not value:
        value = os.path.join(os.environ['INSTANCE_HOME'], 'var', default)
    else:
        value = substitute(value, _environ)
    existing_directory = stock_datatypes['existing-directory']
    value = existing_directory(value)
    if not os.access(value, os.R_OK | os.W_OK):
        raise ValueError, 'Zope process user cannot read+write in %s.' % value
    if value in _paths:
        raise ValueError, 'Path %s is used twice' % value
    _paths.append(value)
    return value


def default_strategy(value):
    """Validating/converting a default storage strategy
    @param value: as sent from ZConfig
    @return: valid strategy name
    """
    possible_values = ('flat', 'directory')
    value = str(value).lower()
    if value not in possible_values:
        raise ValueError("'%s' is not a valid storage strategy" % value)
    return value


def strategy(value):
    """Validating/converting a storage strategy
    @param value: as sent from ZConfig
    @return: valid strategy name
    """
    possible_values = ('flat', 'directory', 'site1', 'site2')
    value = str(value).lower()
    if value not in possible_values:
        raise ValueError("'%s' is not a valid storage strategy" % value)
    return value


class BaseConfig(object):
    """Configuration section
    """
    __module__ = __name__

    def __init__(self, section):
        """New (Plone) site config
        @param section: ZConfig.matcher.SectionValue obj
        """
        self._section = section
        self.name = section.getSectionName()
        self._section_attr_names = section.getSectionAttributes()

    def __getattr__(self, attrname):
        """attributes are found in self.section"""
        if attrname in self._section_attr_names:
            return getattr(self._section, attrname)
        else:
            raise AttributeError, attrname


class GlobalConfig(BaseConfig):
    """Instance wide zconfig object"""
    __module__ = __name__
    _is_global = True

    def usesGlobalConfig(self, site_or_path):
        """Does site use the global configuration (true)
        @param site_or_path: Plone site obje or its path
        @return: backup path
        """
        return self._configForPath(site_or_path)._is_global

    def storagePathForSite(self, site_or_path):
        """Specific or global storage path
        @param site_or_path: Plone site obje or its path
        @return: storage path
        """
        return self._configForPath(site_or_path).storage_path

    def backupPathForSite(self, site_or_path):
        """Specific or global backup path
        @param site_or_path: Plone site obje or its path
        @return: backup path
        """
        return self._configForPath(site_or_path).backup_path

    def storageStrategyForSite(self, site_or_path):
        """Specific or global storage strategy
        @param site_or_path: Plone site obje or its path
        @return: storage policy
        """
        return self._configForPath(site_or_path).storage_strategy

    def _configForPath(self, site_or_path):
        """A configuration obj suitable to the site or path
        @param site_or_path: Plone site object or path to a Plone site
        This should be a decorator func but we need to run with Python 2.3
        """
        if type(site_or_path) is types.StringType:
            path = site_or_path.lower()
        else:
            path = ('/').join(site_or_path.getPhysicalPath()).lower()
        if not hasattr(self, '__path_conf_map__'):
            self.__path_conf_map__ = dict([ (site.name, site) for site in self.sites ])
        return self.__path_conf_map__.get(path, self)


class SiteConfig(BaseConfig):
    """Site wide zconfig object"""
    __module__ = __name__
    _is_global = False