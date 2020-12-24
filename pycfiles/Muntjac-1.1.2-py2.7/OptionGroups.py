# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/OptionGroups.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.option_group import OptionGroup
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class OptionGroups(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Option group'

    def getDescription(self):
        return 'OptionGroup component present a group of selections with either radio buttons or checkboxes.'

    def getRelatedAPI(self):
        return [
         APIResource(OptionGroup)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.selects.OptionGroupDisabledItems import OptionGroupDisabledItems
        from muntjac.demo.sampler.features.selects.TwinColumnSelect import TwinColumnSelect
        from muntjac.demo.sampler.features.selects.NativeSelection import NativeSelection
        from muntjac.demo.sampler.features.selects.ListSelectMultiple import ListSelectMultiple
        return [
         OptionGroupDisabledItems,
         NativeSelection,
         ListSelectMultiple,
         TwinColumnSelect]

    def getRelatedResources(self):
        return