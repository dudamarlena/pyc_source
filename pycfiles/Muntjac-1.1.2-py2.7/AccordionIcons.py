# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/accordions/AccordionIcons.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Accordion
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class AccordionIcons(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Accordion with icons'

    def getDescription(self):
        return "The accordion 'tabs' can contain icons in addition to the caption."

    def getRelatedAPI(self):
        return [
         APIResource(Accordion)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.FeatureSet import Tabsheets
        from muntjac.demo.sampler.features.accordions.AccordionDisabled import AccordionDisabled
        return [
         AccordionDisabled, Tabsheets]

    def getRelatedResources(self):
        return