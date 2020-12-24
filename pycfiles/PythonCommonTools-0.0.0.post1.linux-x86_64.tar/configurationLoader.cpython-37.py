# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/pythoncommontools/configurationLoader/configurationLoader.py
# Compiled at: 2019-05-03 20:34:21
# Size of source mod 2**32: 921 bytes
from configparser import ConfigParser

def loadConfiguration(configurationFilePath):
    loadedConfiguration = ConfigParser()
    loadedConfiguration.read(configurationFilePath)
    return loadedConfiguration