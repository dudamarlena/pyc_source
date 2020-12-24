# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/TextFieldSecret.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.text_field import TextField
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TextFieldSecret(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Text field, secret (password)'

    def getDescription(self):
        return 'For sensitive data input, such as passwords, the text field can also be set into secret mode where the input will not be echoed to display.'

    def getRelatedAPI(self):
        return [
         APIResource(TextField)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Texts
        from muntjac.demo.sampler.features.selects.ComboBoxNewItems import ComboBoxNewItems
        from muntjac.demo.sampler.features.text.TextFieldSingle import TextFieldSingle
        return [
         TextFieldSingle, ComboBoxNewItems, Texts]

    def getRelatedResources(self):
        return