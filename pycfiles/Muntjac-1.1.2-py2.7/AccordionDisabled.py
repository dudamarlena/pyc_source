# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/accordions/AccordionDisabled.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Accordion
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class AccordionDisabled(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Accordion, disabled tabs'

    def getDescription(self):
        return "You can disable, enable, hide and show accordion 'tabs'."

    def getRelatedAPI(self):
        return [
         APIResource(Accordion)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tabsheets
        from muntjac.demo.sampler.features.accordions.AccordionIcons import AccordionIcons
        return [
         AccordionIcons, Tabsheets]

    def getRelatedResources(self):
        return