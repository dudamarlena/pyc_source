# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/ClickableLayoutBasic.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.demo.sampler.NamedExternalResource import NamedExternalResource
from muntjac.api import CssLayout, AbsoluteLayout, VerticalLayout, HorizontalLayout, GridLayout, Panel

class ClickableLayoutBasic(Feature):

    def getSinceVersion(self):
        return Version.V63

    def getDescription(self):
        return 'You can listen for click events by attaching a LayoutClickListener to your layout.'

    def getName(self):
        return 'Clickable layouts'

    def getRelatedAPI(self):
        return [
         APIResource(CssLayout),
         APIResource(AbsoluteLayout),
         APIResource(VerticalLayout),
         APIResource(HorizontalLayout),
         APIResource(GridLayout),
         APIResource(Panel)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Layouts
        return [
         Layouts]

    def getRelatedResources(self):
        return [
         NamedExternalResource('CSS for the layout', self.getThemeBase() + 'layouts/clickableexample.css')]