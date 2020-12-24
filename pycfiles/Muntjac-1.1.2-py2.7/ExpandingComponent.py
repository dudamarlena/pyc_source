# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/ExpandingComponent.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.api import HorizontalLayout

class ExpandingComponent(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Expanding components'

    def getDescription(self):
        return 'You can <i>expand</i> components to make them occupy the space left over by other components.<br/> If more than one component is expanded, the <i>ratio</i> determines how the leftover space is shared between the expanded components.<br/>Mousover each component for a description (tooltip).<br/>Also try resizing the window.'

    def getRelatedAPI(self):
        return [
         APIResource(HorizontalLayout)]

    def getRelatedFeatures(self):
        return []

    def getRelatedResources(self):
        return