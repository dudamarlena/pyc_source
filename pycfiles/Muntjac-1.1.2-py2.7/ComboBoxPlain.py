# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/selects/ComboBoxPlain.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.combo_box import ComboBox
from muntjac.demo.sampler.features.selects.ComboBoxInputPrompt import ComboBoxInputPrompt
from muntjac.demo.sampler.features.selects.ComboBoxContains import ComboBoxContains
from muntjac.demo.sampler.features.selects.ComboBoxStartsWith import ComboBoxStartsWith
from muntjac.demo.sampler.features.selects.ComboBoxNewItems import ComboBoxNewItems
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class ComboBoxPlain(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Combobox'

    def getDescription(self):
        return 'A drop-down selection component with single item selection. Shown here is the most basic variant, which basically provides the same functionality as a NativeSelect with added lazy-loading if there are many options.<br/>See related examples for more advanced features.'

    def getRelatedAPI(self):
        return [
         APIResource(ComboBox)]

    def getRelatedFeatures(self):
        return [
         ComboBoxInputPrompt,
         ComboBoxStartsWith,
         ComboBoxContains,
         ComboBoxNewItems]

    def getRelatedResources(self):
        return