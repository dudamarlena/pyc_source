# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/slider/SliderVertical.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.slider import Slider
from muntjac.demo.sampler.features.slider.SliderHorizontal import SliderHorizontal
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class SliderVertical(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Vertical slider'

    def getDescription(self):
        return

    def getRelatedAPI(self):
        return [
         APIResource(Slider)]

    def getRelatedFeatures(self):
        return [
         SliderHorizontal]

    def getRelatedResources(self):
        return