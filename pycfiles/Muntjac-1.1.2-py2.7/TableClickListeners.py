# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/table/TableClickListeners.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.table import Table
from muntjac.demo.sampler.features.table.TableClickListenersExample import TableClickListenersExample
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TableClickListeners(Feature):

    def getDescription(self):
        return 'You can assign a click listener to the column headers and footers to handle user mouse clicks.'

    def getName(self):
        return 'Table, click listeners'

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
        return TableClickListenersExample()