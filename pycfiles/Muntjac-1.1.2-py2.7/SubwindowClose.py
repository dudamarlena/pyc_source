# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/windows/SubwindowClose.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.window import Window
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class SubwindowClose(Feature):

    def getName(self):
        return 'Window closing'

    def getDescription(self):
        return 'Using a <i>CloseListener</i> one can detect when a window is closed.'

    def getRelatedAPI(self):
        return [
         APIResource(Window)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Windows
        return [
         Windows]

    def getRelatedResources(self):
        return

    def getSinceVersion(self):
        return Version.V62