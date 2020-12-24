# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/dates/DateLocale.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import DateField, InlineDateField
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class DateLocale(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Date selection, locale'

    def getDescription(self):
        return 'In this example, you can select a different locale from the combo box and see how the calendar component is localized.'

    def getRelatedAPI(self):
        return [
         APIResource(DateField),
         APIResource(InlineDateField)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.dates.DatePopupInputPrompt import DatePopupInputPrompt
        from muntjac.demo.sampler.features.dates.DateInline import DateInline
        from muntjac.demo.sampler.features.dates.DatePopup import DatePopup
        from muntjac.demo.sampler.features.dates.DateResolution import DateResolution
        return [
         DateInline,
         DatePopup,
         DatePopupInputPrompt,
         DateResolution]

    def getRelatedResources(self):
        return