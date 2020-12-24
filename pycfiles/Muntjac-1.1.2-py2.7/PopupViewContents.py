# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/popupviews/PopupViewContents.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.popup_view import PopupView
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class PopupViewContents(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'PopupView content modes'

    def getDescription(self):
        return 'The PopupView supports both static and dynamically generated HTML content for the minimized view.'

    def getRelatedAPI(self):
        return [
         APIResource(PopupView)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.popupviews.PopupViewClosing import PopupViewClosing
        return [
         PopupViewClosing]

    def getRelatedResources(self):
        return