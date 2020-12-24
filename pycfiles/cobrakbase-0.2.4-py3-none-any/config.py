# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/utils/config.py
# Compiled at: 2016-08-05 01:23:17
import os, ConfigParser

class Config:

    def __init__(self, level1=None, level2=None):
        self.project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        if level1 is None and level2 is None:
            return
        else:
            config = ConfigParser.ConfigParser()
            config_file = os.path.join(self.project_directory, 'config')
            config.read(config_file)
            self.value = config.get(level1, level2)
            return