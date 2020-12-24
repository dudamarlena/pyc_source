# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/NativeSelection.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.ui.native_select import NativeSelect

class NativeSelection(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Native select'

    def getDescription(self):
        return 'A NativeSelect is a a simple drop-down list for selecting one item. It is called <i>native</i> because it uses the look and feel from the browser in use.<br/>The ComboBox component is a much more versatile variant, but without the native look and feel.<br/>From a usability standpoint, you might also want to consider using a ListSelect in single-select-mode, so that the user can see all options right away.'

    def getRelatedAPI(self):
        return [
         APIResource(NativeSelect)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.selects.ComboBoxPlain import ComboBoxPlain
        from muntjac.demo.sampler.FeatureSet import Selects
        from muntjac.demo.sampler.features.selects.ListSelectSingle import ListSelectSingle
        return [
         ComboBoxPlain, ListSelectSingle, Selects]

    def getRelatedResources(self):
        return