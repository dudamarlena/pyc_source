# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/Tooltips.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class Tooltips(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Tooltips'

    def getDescription(self):
        return 'Most components can have a <i>description</i>, which is usually shown as a <i>"tooltip"</i>. In the Form component, the description is shown at the top of the form. Descriptions can have HTML formatted (\'rich\') content.<br/>'

    def getRelatedAPI(self):
        return [
         APIResource(AbstractComponent)]

    def getRelatedFeatures(self):
        return

    def getRelatedResources(self):
        return