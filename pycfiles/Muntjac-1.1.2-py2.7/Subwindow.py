# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/windows/Subwindow.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.window import Window
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class Subwindow(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Subwindow'

    def getDescription(self):
        return 'A <i>Subwindow</i> is a popup-window within the browser window. There can be multiple subwindows in one (native) browser window.'

    def getRelatedAPI(self):
        return [
         APIResource(Window)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.windows.NativeWindowExample import NativeWindow
        from muntjac.demo.sampler.FeatureSet import Windows
        return [
         NativeWindow, Windows]

    def getRelatedResources(self):
        return