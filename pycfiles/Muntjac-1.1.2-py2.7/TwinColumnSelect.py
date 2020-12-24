# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/TwinColumnSelect.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.twin_col_select import TwinColSelect
from muntjac.demo.sampler.features.selects.NativeSelection import NativeSelection
from muntjac.demo.sampler.features.selects.ListSelectMultiple import ListSelectMultiple
from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.selects.ListSelectSingle import ListSelectSingle
from muntjac.demo.sampler.Feature import Feature, Version

class TwinColumnSelect(Feature):

    def getSinceVersion(self):
        return Version.V65

    def getName(self):
        return 'Twin column select (list builder)'

    def getDescription(self):
        return 'The TwinColumnSelect is a multiple selection component that shows two lists side by side. The list on the left shows the available items and the list on the right shows the selected items. <br><br/>You can select items from the list on the left and either click on the >> button or press Enter to move them to the list on the right. Items can be moved back by selecting them and either click on the << button or press Enter.<br/>'

    def getRelatedAPI(self):
        return [
         APIResource(TwinColSelect)]

    def getRelatedFeatures(self):
        return [
         NativeSelection, ListSelectMultiple, ListSelectSingle]

    def getRelatedResources(self):
        return [
         NamedExternalResource('Open Source Design Pattern Library; List Builder', 'http://www.uidesignpatterns.org/designPatterns/List-Builder')]