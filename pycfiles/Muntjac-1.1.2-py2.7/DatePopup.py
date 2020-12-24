# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dates/DatePopup.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import DateField, PopupDateField
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class DatePopup(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Pop-up date selection'

    def getDescription(self):
        return 'In this example, the resolution is set to be one day and the DateField component is shown as a calendar pop-up.'

    def getRelatedAPI(self):
        return [
         APIResource(DateField), APIResource(PopupDateField)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.dates.DateInline import DateInline
        from muntjac.demo.sampler.features.dates.DateLocale import DateLocale
        from muntjac.demo.sampler.features.dates.DateResolution import DateResolution
        from muntjac.demo.sampler.features.dates.DatePopupInputPrompt import DatePopupInputPrompt
        return [
         DatePopupInputPrompt, DateInline, DateLocale, DateResolution]

    def getRelatedResources(self):
        return