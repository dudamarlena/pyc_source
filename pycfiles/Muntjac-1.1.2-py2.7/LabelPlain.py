# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/LabelPlain.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.label import Label
from muntjac.demo.sampler.features.text.RichTextEditor import RichTextEditor
from muntjac.demo.sampler.features.text.TextArea import TextArea
from muntjac.demo.sampler.features.text.LabelPreformatted import LabelPreformatted
from muntjac.demo.sampler.features.text.TextFieldSingle import TextFieldSingle
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.text.LabelRich import LabelRich
from muntjac.demo.sampler.Feature import Feature, Version

class LabelPlain(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Label, plain text'

    def getDescription(self):
        return 'In this example the content mode is set to CONTENT_TEXT, meaning that the label will contain only plain text.'

    def getRelatedAPI(self):
        return [
         APIResource(Label)]

    def getRelatedFeatures(self):
        return [
         LabelPreformatted,
         LabelRich,
         TextFieldSingle,
         TextArea,
         RichTextEditor]

    def getRelatedResources(self):
        return