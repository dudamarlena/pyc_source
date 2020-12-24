# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/JSApi.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Window
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version

class JSApi(Feature):

    def getSinceVersion(self):
        return Version.V62

    def getName(self):
        return 'JavaScript API'

    def getDescription(self):
        return '<p>You can inject JavaScript in a Muntjac application page' + ' using the server-side JavaScript API.' + ' This is especially useful for integration with ' + 'third-party libraries and components.</p>'

    def getRelatedAPI(self):
        return [
         APIResource(Window)]

    def getRelatedFeatures(self):
        return

    def getRelatedResources(self):
        return