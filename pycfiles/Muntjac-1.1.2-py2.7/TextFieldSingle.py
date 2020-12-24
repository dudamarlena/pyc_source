# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/TextFieldSingle.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.text_field import TextField
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TextFieldSingle(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Text field'

    def getDescription(self):
        return "A single-line TextField is a fundamental UI building blocks with numerous uses.<br/>If the input would benefit from remembering previous values, you might want to consider using a ComboBox it it's  'suggesting mode' instead."

    def getRelatedAPI(self):
        return [
         APIResource(TextField)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Texts
        from muntjac.demo.sampler.features.text.TextFieldSecret import TextFieldSecret
        from muntjac.demo.sampler.features.selects.ComboBoxNewItems import ComboBoxNewItems
        return [
         TextFieldSecret, ComboBoxNewItems, Texts]

    def getRelatedResources(self):
        return