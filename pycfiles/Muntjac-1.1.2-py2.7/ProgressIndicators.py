# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/progressindicator/ProgressIndicators.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.api import ProgressIndicator

class ProgressIndicators(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'Progress indication'

    def getDescription(self):
        return 'The ProgressIndicator component can be used to inform the user of actions that take a long time to finish, such as file uploads or search queries.<br /><br />Updates to the indicator happen via polling, and the default polling interval is 1 second.'

    def getRelatedAPI(self):
        return [
         APIResource(ProgressIndicator)]

    def getRelatedFeatures(self):
        return

    def getRelatedResources(self):
        return