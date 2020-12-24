# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/ComboBoxStartsWith.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.combo_box import ComboBox
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class ComboBoxStartsWith(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Combobox, suggesting (starts-with)'

    def getDescription(self):
        return 'A drop-down selection component with single item selection.<br/>A \'starts-with\' filter has been used in this example, so you can key in some text and only the options beginning with your input will be shown.<br/>Because there are so many options, they are loaded on-demand ("lazy-loading") from the server when paging or filtering. This behavior is built-in and requires no extra code.'

    def getRelatedAPI(self):
        return [
         APIResource(ComboBox)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.selects.ComboBoxPlain import ComboBoxPlain
        from muntjac.demo.sampler.features.selects.ComboBoxContains import ComboBoxContains
        from muntjac.demo.sampler.features.selects.ComboBoxNewItems import ComboBoxNewItems
        return [
         ComboBoxPlain, ComboBoxContains, ComboBoxNewItems]

    def getRelatedResources(self):
        return