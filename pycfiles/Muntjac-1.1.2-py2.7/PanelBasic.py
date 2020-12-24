# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/panels/PanelBasic.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.api import Panel
from muntjac.ui.layout import ILayout

class PanelBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Panel'

    def getDescription(self):
        return ''

    def getRelatedAPI(self):
        return [
         APIResource(Panel), APIResource(ILayout)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Layouts
        from muntjac.demo.sampler.features.panels.PanelLight import PanelLight
        return [
         PanelLight, Layouts]

    def getRelatedResources(self):
        return