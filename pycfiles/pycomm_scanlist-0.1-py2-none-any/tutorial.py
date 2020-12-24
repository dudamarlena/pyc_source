# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/tutorial.py
# Compiled at: 2007-02-12 09:02:44
__doc__ = ' tutorial creators\n'
import os
from generator import registerTask
from resttask import RestTask

class TutorialTask(RestTask):
    """creates the recipes"""

    def _getTemplateFile(self, configuration):
        """returns the template"""
        return configuration.templates['tutorial']

    def _getTemplateListFile(self, configuration):
        """returns the template list"""
        return configuration.templates['tutoriallist']

    def _getName(self):
        """returns the task name"""
        return 'tutorial'

    def _getFolders(self, configuration):
        """returns recipes folders"""
        return configuration.tutorials.values()


registerTask(TutorialTask)