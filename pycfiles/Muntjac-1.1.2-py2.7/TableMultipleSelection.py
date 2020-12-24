# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/table/TableMultipleSelection.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.table import Table
from muntjac.demo.sampler.features.table.TableMainFeaturesExample import TableMainFeaturesExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TableMultipleSelection(Feature):

    def getDescription(self):
        return 'When the table is in multiselect mode you can use the Ctrl (or Meta key) to select or unselect multiple items. You can also use the Shift key to select a range of items and Ctrl+Shift key to select multiple ranges.'

    def getName(self):
        return 'Table, multiple selection'

    def getRelatedAPI(self):
        return [
         APIResource(Table)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tables
        return [
         Tables]

    def getRelatedResources(self):
        return

    def getSinceVersion(self):
        return Version.V64

    def getExample(self):
        return TableMainFeaturesExample()