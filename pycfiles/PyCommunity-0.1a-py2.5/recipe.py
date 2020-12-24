# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/recipe.py
# Compiled at: 2007-02-12 09:02:44
""" recipe creators
"""
import os
from generator import registerTask
from resttask import RestTask

class RecipeTask(RestTask):
    """creates the recipes"""

    def _getTemplateFile(self, configuration):
        """returns the template"""
        return configuration.templates['recipe']

    def _getTemplateListFile(self, configuration):
        """returns the template list"""
        return configuration.templates['recipelist']

    def _getName(self):
        """returns the task name"""
        return 'recipe'

    def _getFolders(self, configuration):
        """returns recipes folders"""
        return configuration.recipes.values()


registerTask(RecipeTask)