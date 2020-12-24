# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dates/DatePopupInputPrompt.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import PopupDateField
from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class DatePopupInputPrompt(Feature):

    def getSinceVersion(self):
        return Version.V64

    def getName(self):
        return 'Pop-up date selection with input prompt'

    def getDescription(self):
        return ' The PopupDateField can have an <i>input prompt</i> - a textual hint that is shown within the field when the field is otherwise empty.<br/> You can use an input prompt instead of a caption to save space, but only do so if the function of the PopupDateField is still clear when a value has been entered and the prompt is no longer visible.'

    def getRelatedAPI(self):
        return [
         APIResource(PopupDateField)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.dates.DateInline import DateInline
        from muntjac.demo.sampler.features.dates.DateLocale import DateLocale
        from muntjac.demo.sampler.features.dates.DateResolution import DateResolution
        from muntjac.demo.sampler.features.selects.ComboBoxInputPrompt import ComboBoxInputPrompt
        from muntjac.demo.sampler.features.text.TextFieldInputPrompt import TextFieldInputPrompt
        return [
         DateInline,
         DateLocale,
         DateResolution,
         TextFieldInputPrompt,
         ComboBoxInputPrompt]

    def getRelatedResources(self):
        return [
         NamedExternalResource('UI Patterns, Input Prompt', 'http://ui-patterns.com/pattern/InputPrompt')]