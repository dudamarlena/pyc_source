# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/VerticalLayoutBasic.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.vertical_layout import VerticalLayout
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class VerticalLayoutBasic(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Vertical layout'

    def getDescription(self):
        return 'The VerticalLayout arranges components vertically. It is 100% wide by default, which is nice in many cases, but something to be aware of if trouble arises.<br/>It supports all basic features, plus some advanced stuff - including spacing, margin, alignment, and expand ratios.'

    def getRelatedAPI(self):
        return [
         APIResource(VerticalLayout)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.layouts.LayoutSpacing import LayoutSpacing
        from muntjac.demo.sampler.features.layouts.HorizontalLayoutBasic import HorizontalLayoutBasic
        from muntjac.demo.sampler.features.layouts.LayoutAlignment import LayoutAlignment
        return [
         HorizontalLayoutBasic, LayoutSpacing, LayoutAlignment]

    def getRelatedResources(self):
        return