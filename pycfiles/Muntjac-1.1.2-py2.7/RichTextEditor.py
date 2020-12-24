# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/RichTextEditor.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.rich_text_area import RichTextArea
from muntjac.demo.sampler.features.text.LabelRichExample import LabelRichExample
from muntjac.demo.sampler.features.text.TextArea import TextArea
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.features.text.LabelRich import LabelRich
from muntjac.demo.sampler.Feature import Feature, Version

class RichTextEditor(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Rich text area'

    def getDescription(self):
        return "The RichTextArea allows 'rich' formatting of the input.<br/>Click the <i>Edit</i> button to edit the label content with the RichTextArea."

    def getRelatedAPI(self):
        return [
         APIResource(RichTextArea)]

    def getRelatedFeatures(self):
        return [
         TextArea, LabelRich]

    def getRelatedResources(self):
        return

    def getExample(self):
        return LabelRichExample()