# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/tabsheets/TabSheetScrolling.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.tab_sheet import TabSheet
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TabSheetScrolling(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tabsheet, scrolling tabs'

    def getDescription(self):
        return 'If the tabs are to many to be shown at once, a scrolling control will appear automatically.'

    def getRelatedAPI(self):
        return [
         APIResource(TabSheet)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.tabsheets.TabSheetIcons import TabSheetIcons
        from muntjac.demo.sampler.features.tabsheets.TabSheetDisabled import TabSheetDisabled
        return [
         TabSheetIcons, TabSheetDisabled]

    def getRelatedResources(self):
        return