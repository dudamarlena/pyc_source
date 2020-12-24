# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/TextFieldTextChangeEvent.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.text_field import TextField
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class TextFieldTextChangeEvent(Feature):

    def getName(self):
        return 'Instant text field'

    def getDescription(self):
        return 'You can react to the text input in a text field as the user is writing. This allows for easy implementation of for instance as-you-type filtering.'

    def getRelatedResources(self):
        return

    def getRelatedAPI(self):
        return [
         APIResource(TextField)]

    def getRelatedFeatures(self):
        return

    def getSinceVersion(self):
        return Version.V65