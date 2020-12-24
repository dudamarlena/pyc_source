# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/panels/PanelLight.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Panel
from muntjac.ui.layout import ILayout
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class PanelLight(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Panel, light style'

    def getDescription(self):
        return "The 'light' panel has less decorations than the regular Panel style."

    def getRelatedAPI(self):
        return [
         APIResource(Panel), APIResource(ILayout)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.panels.PanelBasic import PanelBasic
        from muntjac.demo.sampler.FeatureSet import Layouts
        return [
         PanelBasic, Layouts]

    def getRelatedResources(self):
        return