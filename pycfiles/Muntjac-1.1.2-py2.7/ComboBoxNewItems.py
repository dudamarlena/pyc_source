# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/ComboBoxNewItems.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.combo_box import ComboBox
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class ComboBoxNewItems(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Combobox, enter new items'

    def getDescription(self):
        return 'A drop-down selection component with single item selection.<br/>This example also allows you to input your own choice - your input will be added to the selection of available choices. This behavior is built-in and can be enabled with one method call. Note that by using this feature, one can easily create <i>suggestion box</i> -type inputs that for example remembers the users previous input, or provides suggestions from a list of popular choices. Configured like this (and optionally with a filter), the ComboBox can be a powerful alternative to TextField.'

    def getRelatedAPI(self):
        return [
         APIResource(ComboBox)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.selects.ComboBoxPlain import ComboBoxPlain
        from muntjac.demo.sampler.features.selects.ComboBoxContains import ComboBoxContains
        from muntjac.demo.sampler.features.selects.ComboBoxStartsWith import ComboBoxStartsWith
        return [
         ComboBoxPlain, ComboBoxStartsWith, ComboBoxContains]

    def getRelatedResources(self):
        return