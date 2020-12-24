# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/popupviews/PopupViewClosing.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.popup_view import PopupView
from muntjac.demo.sampler.features.popupviews.PopupViewContents import PopupViewContents
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class PopupViewClosing(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'PopupView close events'

    def getDescription(self):
        return 'By default the popup will close as soon as the user moves the mouse out of the popup area, but you can set it to close only when the user clicks the mouse outside the popup area. You can also attach open and close listeners for these events.'

    def getRelatedAPI(self):
        return [
         APIResource(PopupView)]

    def getRelatedFeatures(self):
        return [
         PopupViewContents]

    def getRelatedResources(self):
        return