# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/tabsheets/TabSheetIcons.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.tab_sheet import TabSheet
from muntjac.demo.sampler.features.tabsheets.TabSheetScrolling import TabSheetScrolling
from muntjac.demo.sampler.features.tabsheets.TabSheetDisabled import TabSheetDisabled
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TabSheetIcons(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tabsheet with icons'

    def getDescription(self):
        return 'Each tab can have an Icon in addition to the caption.'

    def getRelatedAPI(self):
        return [
         APIResource(TabSheet)]

    def getRelatedFeatures(self):
        return [
         TabSheetScrolling, TabSheetDisabled]

    def getRelatedResources(self):
        return