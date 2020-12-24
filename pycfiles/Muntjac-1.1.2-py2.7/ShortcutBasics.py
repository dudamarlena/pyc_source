# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/shortcuts/ShortcutBasics.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.Feature import Feature, Version

class ShortcutBasics(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getName(self):
        return 'Shortcuts, basics'

    def getDescription(self):
        return "A simple example of shorcuts attached directly to fields.<br/>Such a shortcut is window-global, and is conveniently removed if the component is removed.<br/><br/>Note, that all browsers don't work well with all keyboard shortcuts. This is a problem for the whole web application industry. Opera is the most intolerant on them and basically only ALT-SHIFT based shortcuts are working. Shortcuts here are chosen so that they should work on most common browsers."

    def getRelatedAPI(self):
        return []

    def getRelatedFeatures(self):
        return []

    def getRelatedResources(self):
        return