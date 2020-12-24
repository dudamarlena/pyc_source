# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/link/LinkNoDecorations.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.demo.sampler.APIResource import APIResource
from muntjac.demo.sampler.Feature import Feature, Version
from muntjac.api import Link

class LinkNoDecorations(Feature):

    def getSinceVersion(self):
        return Version.OLD

    def getName(self):
        return 'Link, configure window'

    def getDescription(self):
        return 'Links can open new browser windows, and configure the amount of browser features shown, such as toolbar and addressbar.<br/>These links open a browser window without decorations.'

    def getRelatedAPI(self):
        return [
         APIResource(Link)]

    def getRelatedFeatures(self):
        from muntjac.demo.sampler.features.buttons.ButtonLink import ButtonLink
        from muntjac.demo.sampler.features.link.LinkCurrentWindow import LinkCurrentWindow
        from muntjac.demo.sampler.features.link.LinkSizedWindow import LinkSizedWindow
        return [
         LinkCurrentWindow, LinkSizedWindow, ButtonLink]

    def getRelatedResources(self):
        return