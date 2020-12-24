# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/LabelPreformatted.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.label import Label
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class LabelPreformatted(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Label, preformatted'

    def getDescription(self):
        return 'In this example the content mode is set to CONTENT_PREFORMATTED. The text for this content type is by default rendered with fixed-width font. Line breaks can be inserted with \\n and tabulator characters with \\t.'

    def getRelatedAPI(self):
        return [
         APIResource(Label)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.text.RichTextEditor import RichTextEditor
        from muntjac.demo.sampler.features.text.TextArea import TextArea
        from muntjac.demo.sampler.features.text.LabelPlain import LabelPlain
        from muntjac.demo.sampler.features.text.TextFieldSingle import TextFieldSingle
        from muntjac.demo.sampler.features.text.LabelRich import LabelRich
        return [
         LabelPlain,
         LabelRich,
         TextFieldSingle,
         TextArea,
         RichTextEditor]

    def getRelatedResources(self):
        return