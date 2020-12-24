# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/windows/SubwindowPositioned.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.window import Window
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class SubwindowPositioned(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Window position'

    def getDescription(self):
        return 'The position of a window can be specified, or it can be centered.'

    def getRelatedAPI(self):
        return [
         APIResource(Window)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Windows
        return [
         Windows]

    def getRelatedResources(self):
        return