# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/extfile/namechooser/config.py
# Compiled at: 2012-06-20 11:22:54
__docformat__ = 'restructuredtext'
import os
from ztfy.extfile.namechooser.interfaces import IExtFileNameChooserConfig
from zope.component import queryUtility, getAllUtilitiesRegisteredFor
from zope.interface import implements
DEFAULT_TEMP_DIR = '/var/tmp'
DEFAULT_BASE_DIR = '/var/local/zope/extfiles'

class ExtFileConfig(object):
    """Global utility used to configure chooser of external file's name"""
    implements(IExtFileNameChooserConfig)
    name = ''
    chooser = None
    _temp_path = DEFAULT_TEMP_DIR
    _base_path = DEFAULT_BASE_DIR

    def _getTempPath(self):
        return self._temp_path

    def _setTempPath(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self._temp_path = path

    temp_path = property(_getTempPath, _setTempPath)

    def _getBasePath(self):
        return self._base_path

    def _setBasePath(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        self._base_path = path

    base_path = property(_getBasePath, _setBasePath)


def getConfigs():
    """Get list of available name choosers"""
    return getAllUtilitiesRegisteredFor(IExtFileNameChooserConfig)


def getConfig(name=''):
    """Get configuration for a given name chooser"""
    config = queryUtility(IExtFileNameChooserConfig, name)
    if config is None and name:
        config = queryUtility(IExtFileNameChooserConfig)
    return config


def getTempPath(config_name=''):
    """Get temp path for given name chooser"""
    config = getConfig(config_name)
    if config is not None:
        return config.temp_path
    else:
        return DEFAULT_TEMP_DIR


def getBasePath(config_name=''):
    """Get base path for given name chooser"""
    config = getConfig(config_name)
    if config is not None:
        return config.base_path
    else:
        return DEFAULT_BASE_DIR


def getFullPath(parent, extfile, name, config_name=''):
    """Get full path for specified extfile"""
    config = getConfig(config_name)
    if config is not None:
        base_path = config.base_path
        file_path = config.chooser.getName(parent, extfile, name)
        if file_path.startswith(os.path.sep):
            file_path = file_path[1:]
        return os.path.join(base_path, file_path)
    else:
        return