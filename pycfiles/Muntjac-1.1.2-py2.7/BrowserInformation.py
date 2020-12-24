# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/BrowserInformation.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.terminal.gwt.server.web_browser import WebBrowser

class BrowserInformation(Feature):

    def getDescription(self):
        return 'Browser differences are mostly hidden by Muntjac but in some cases it is valuable to get information on the browser the user is using. In themes special CSS rules are used but it is also possible to get information about the browser in the application code. This sample displays the browser name, ip address and the screen size you are using, and your TimeZone offset. The information is available on server side.'

    def getName(self):
        return 'Browser information'

    def getSinceVersion(self):
        return Version.V63

    def getRelatedAPI(self):
        return [
         APIResource(WebBrowser)]

    def getRelatedFeatures(self):
        return

    def getRelatedResources(self):
        return