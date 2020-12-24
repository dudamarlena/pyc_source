# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/configuration.py
# Compiled at: 2007-02-25 12:00:10
__doc__ = ' Configuration reader\n'
import os
from ConfigParser import ConfigParser

class Configuration(object):
    """loads a config file"""

    def __init__(self, filename):
        self._filename = filename
        self._config = ConfigParser()
        self._config.read([filename])

    def _getItems(self, name):
        """return a mapping for a given section"""
        result = {}
        for (name, value) in self._config.items(name):
            result[name] = value

        return result

    def _getRecipes(self):
        """returns recipe list"""
        return self._getItems('recipes')

    recipes = property(_getRecipes)

    def _getPackages(self):
        """returns packages list"""
        return self._getItems('packages')

    packages = property(_getPackages)

    def _getTutorials(self):
        """returns tutorial list"""
        return self._getItems('tutorials')

    tutorials = property(_getTutorials)

    def _getGlossary(self):
        """returns glossary"""
        return self._getItems('options')['glossary']

    glossary = property(_getGlossary)

    def _getMedia(self):
        """returns media"""
        return self._getItems('options')['media']

    media = property(_getMedia)

    def _getTargets(self):
        """returns targets"""
        return self._getItems('targets')

    targets = property(_getTargets)

    def _getTemplates(self):
        """returns templates"""
        return self._getItems('templates')

    templates = property(_getTemplates)

    def _getOptions(self):
        """returns options"""
        return self._getItems('options')

    options = property(_getOptions)