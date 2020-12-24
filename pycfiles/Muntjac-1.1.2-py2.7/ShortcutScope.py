# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/shortcuts/ShortcutScope.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.Feature import Feature, Version

class ShortcutScope(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getName(self):
        return 'Shortcuts, scope'

    def getDescription(self):
        return 'Here, identical shortcuts work independently within each panel; they are <i>scoped</i> to the panel.<p>ALT-SHIFT-1 focuses the first panel, ALT-SHIFT-2 the second, and within the panels arrow-down advances and ALT-SHIFT-F/ALT-SHIFT-L focuses firstname/lastname respectively. ALT-SHIFT-S saves each panel.'

    def getRelatedAPI(self):
        return []

    def getRelatedFeatures(self):
        return []

    def getRelatedResources(self):
        return