# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/tabsheets/TabSheetClosing.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.tab_sheet import TabSheet
from muntjac.demo.sampler.features.tabsheets.TabSheetIcons import TabSheetIcons
from muntjac.demo.sampler.features.tabsheets.TabSheetScrolling import TabSheetScrolling
from muntjac.demo.sampler.features.tabsheets.TabSheetDisabled import TabSheetDisabled
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TabSheetClosing(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Tabsheet, closable tabs'

    def getDescription(self):
        return 'Individual tabs can be set closable. You can also add a handler to perform additional tasks when a user closes a tab, or even prevent closing if for instance the tab contains unsaved data.'

    def getRelatedAPI(self):
        return [
         APIResource(TabSheet)]

    def getRelatedFeatures(self):
        return [
         TabSheetScrolling, TabSheetIcons, TabSheetDisabled]

    def getRelatedResources(self):
        return