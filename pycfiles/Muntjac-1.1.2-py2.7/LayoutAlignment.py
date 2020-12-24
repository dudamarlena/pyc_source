# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/LayoutAlignment.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, HorizontalLayout, GridLayout
from muntjac.demo.sampler.features.layouts.HorizontalLayoutBasic import HorizontalLayoutBasic
from muntjac.demo.sampler.features.layouts.VerticalLayoutBasic import VerticalLayoutBasic
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class LayoutAlignment(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Component alignment'

    def getDescription(self):
        return 'GridLayout, VerticalLayout, and HorizontalLayout, which are tabular layouts consisting of cells, support alignment of components within the layout cells. The alignment of a component within its respective cell is set with setComponentAlignment().'

    def getRelatedAPI(self):
        return [
         APIResource(VerticalLayout),
         APIResource(HorizontalLayout),
         APIResource(GridLayout)]

    def getRelatedFeatures(self):
        return [
         HorizontalLayoutBasic, VerticalLayoutBasic]

    def getRelatedResources(self):
        return